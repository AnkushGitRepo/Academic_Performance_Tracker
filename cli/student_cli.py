import matplotlib.pyplot as plt
import re
import os
import pandas as pd
import numpy as np
from utils.input_validation import validate_enrolment_id
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import KeepTogether
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from database.db_operations import DBOperations
from rich.console import Console
from utils.input_validation import get_acronym


console = Console()


def get_acronym(subject: str) -> str:
    """
    Extract the acronym from the subject name, assuming it's in parentheses.
    E.g., 'Introduction to Probability Theory (IPT)' -> 'IPT'.
    If no parentheses are found, fallback to first three uppercase letters.
    """
    # Special handling for JAVA subjects
    upper_sub = subject.upper()
    if 'JAVA-I' in upper_sub:
        return 'JAVA-I'
    elif 'JAVA-II' in upper_sub:
        return 'JAVA-II'

    # Try to extract from parentheses
    match = re.search(r'\((.*?)\)', subject)
    if match:
        return match.group(1).strip()
    else:
        # Fallback: first three uppercase letters of the subject
        return subject[:3].upper()

def get_color(mark: float) -> str:
    """
    Return the bar color based on the mark range.
    """
    if mark < 9:
        return 'red'
    elif mark <= 15:
        return 'orange'
    elif mark <= 20:
        return 'lightgreen'
    else:
        return 'green'

def compute_percentile(user_score, all_scores):
    """
    Given a list of all_scores (ints/floats) and the user's score,
    compute the percentile rank of the user.
    E.g., 90 means the user is at or above 90% of the class.
    """
    sorted_scores = sorted(all_scores)
    rank = sum(score <= user_score for score in sorted_scores)
    percentile = (rank / len(sorted_scores)) * 100
    return percentile

def select_subject(db, enrolment_id, semester):
    """
    1) Fetch all distinct subjects for this student & semester.
    2) Display them in a numbered list with acronyms.
    3) Prompt the user to select by number, acronym, or partial/full name.
    4) Return the matching subject string, or None if no match.
    """
    subjects = db.fetch_subjects_for_semester(enrolment_id, semester)
    if not subjects:
        console.print(f"[yellow]No subjects found for semester {semester}.[/yellow]")
        return None

    # Build a list of (subject_name, acronym)
    sub_list = [(sub, get_acronym(sub)) for sub in subjects]

    console.print(f"[bold]Subjects for Semester {semester}:[/bold]")
    for i, (sub, acr) in enumerate(sub_list, start=1):
        console.print(f"{i}. {sub} [dim]({acr})[/dim]")

    user_input = input("\nEnter subject number, acronym, or name: ").strip()
    if not user_input:
        console.print("[red]No input provided.[/red]")
        return None

    # 1) Try interpreting input as a number
    try:
        choice_num = int(user_input)
        if 1 <= choice_num <= len(sub_list):
            return sub_list[choice_num - 1][0]  # Return the full subject name
    except ValueError:
        pass  # Not a number, proceed

    # Convert input to lower for case-insensitive matching
    user_input_lower = user_input.lower()

    # 2) Check for exact acronym match or exact subject match
    for (sub, acr) in sub_list:
        if user_input_lower == acr.lower():
            return sub
        if user_input_lower == sub.lower():
            return sub

    # 3) Check for partial match in acronym or subject name
    for (sub, acr) in sub_list:
        if user_input_lower in acr.lower():
            return sub
        if user_input_lower in sub.lower():
            return sub

    console.print("[red]No matching subject found. Please try again.[/red]")
    return None

def view_individual_scores(enrolment_id):
    db = DBOperations()

    # Prompt the student for the semester
    sem_input = input("Enter semester to view scores (1-3): ").strip()
    try:
        semester = int(sem_input)
        if semester not in [1, 2, 3]:
            console.print("[red]Invalid semester. Please enter 1, 2, or 3.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid input. Please enter a numeric semester.[/red]")
        return

    # Fetch the scores for the requested semester
    scores = db.fetch_student_scores(enrolment_id, semester)
    if not scores:
        console.print(f"[red]No scores found for semester {semester}.[/red]")
        return

    # Generate a separate figure for each subject
    for row in scores:
        subject, T1, T2, T3, T4, total_score = row
        tests = ['T1', 'T2', 'T3', 'T4']
        marks = [T1, T2, T3, T4]

        acronym = get_acronym(subject)
        colors = [get_color(m) for m in marks]

        # Create a new figure for each subject
        plt.figure(figsize=(12, 5))

        # Bar Chart (left subplot)
        plt.subplot(1, 2, 1)
        plt.bar(tests, marks, color=colors)
        plt.xlabel("Tests")
        plt.ylabel("Marks")
        plt.ylim(0, 25)  # each test out of 25
        plt.title(f"{acronym} - Test Scores")
        plt.grid(axis='y')   # Enable grid lines

        # Pie Chart (right subplot)
        plt.subplot(1, 2, 2)
        plt.pie(marks, labels=tests, autopct='%1.1f%%', startangle=90)
        plt.title(f"{acronym} - Contribution")

        # Overall figure title
        plt.suptitle(f"Subject: {subject}")

        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()


def view_semester_performance(enrolment_id):
    """
    Displays:
      1) A line graph of total scores across available semesters.
      2) A heatmap of acronym vs. semester total scores.
    """
    db = DBOperations()
    results = db.fetch_all_semester_scores(enrolment_id)

    # If there's no data, inform the user and return
    if not results:
        console.print("[red]No semester data found for this student.[/red]")
        return

    # Convert raw tuples into a DataFrame for easier manipulation
    # Each tuple is (semester, subject, T1, T2, T3, T4, total_score)
    data = []
    for row in results:
        semester, subject, T1, T2, T3, T4, total_score = row
        # Apply acronym transformation
        acronym = get_acronym(subject)
        data.append({
            'semester': semester,
            'subject': subject,
            'acronym': acronym,
            'total_score': total_score
        })

    df = pd.DataFrame(data)  # columns: semester, subject, acronym, total_score

    # ---------------------------
    # 1. LINE GRAPH: Semester vs. Sum of total_scores
    # ---------------------------
    semester_summary = df.groupby('semester')['total_score'].sum().reset_index().sort_values('semester')

    # ---------------------------
    # 2. HEATMAP: acronym vs. Semester
    # ---------------------------
    # Create a pivot table with acronym as rows and semesters as columns
    pivot = df.pivot_table(
        index='acronym',
        columns='semester',
        values='total_score',
        aggfunc='sum'
    ).fillna(0)

    # -------------
    # Plotting
    # -------------
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))

    # LINE GRAPH on ax1
    ax1.plot(
        semester_summary['semester'],
        semester_summary['total_score'],
        marker='o',
        color='blue',
        linestyle='-'
    )
    ax1.set_xlabel("Semester")
    ax1.set_ylabel("Total Score")
    ax1.set_title("Semester-wise Total Scores")
    ax1.grid(True)

    # HEATMAP on ax2
    heatmap_data = pivot.values
    acronyms = pivot.index.tolist()
    semesters = pivot.columns.tolist()

    cax = ax2.imshow(heatmap_data, cmap='Blues', aspect='auto')
    ax2.set_title("Subjects vs. Semester Heatmap")

    # Configure the ticks to show semester numbers and acronym labels
    ax2.set_xticks(range(len(semesters)))
    ax2.set_yticks(range(len(acronyms)))
    ax2.set_xticklabels([f"Sem {s}" for s in semesters], rotation=45)
    ax2.set_yticklabels(acronyms)

    # Add a colorbar
    fig.colorbar(cax, ax=ax2, orientation='vertical', label='Total Score')

    plt.tight_layout()
    plt.show()


def view_comparative_analysis(enrolment_id):
    """
    1) Asks the student which semester to analyze.
    2) Fetches all scores for that semester (all students).
    3) Compares the student's total score to the class average per acronym (subject).
    4) Computes the student's percentile rank for each acronym.
    5) Displays a grouped bar chart with 'Your Score' vs. 'Class Avg'
       and annotates the percentile rank above the user's bar.
    """
    db = DBOperations()

    # Prompt for semester
    sem_input = input("Enter semester for comparative analysis (1-3): ").strip()
    try:
        semester = int(sem_input)
        if semester not in [1, 2, 3]:
            console.print("[red]Invalid semester. Please enter 1, 2, or 3.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid input. Please enter a numeric semester.[/red]")
        return

    # Fetch all student scores for the chosen semester
    results = db.fetch_semester_scores_all_students(semester)
    if not results:
        console.print(f"[red]No scores found for semester {semester}.[/red]")
        return

    # Convert results to a DataFrame for easy grouping and analysis
    # results -> list of (enrolment_id, subject, total_score)
    df = pd.DataFrame(results, columns=['enrolment_id', 'subject', 'total_score'])

    # Apply acronym transformation to each row
    from utils.input_validation import get_acronym  # or wherever get_acronym is defined
    df['acronym'] = df['subject'].apply(get_acronym)

    # Filter rows for the logged-in student
    user_df = df[df['enrolment_id'] == enrolment_id].copy()
    if user_df.empty:
        console.print(f"[yellow]You have no scores recorded in semester {semester}.[/yellow]")
        return

    # Compute class average per acronym
    class_avg = df.groupby('acronym')['total_score'].mean().reset_index(name='avg_score')

    # Merge user scores with class averages on acronym
    # user_df has columns: enrolment_id, subject, total_score, acronym
    # class_avg has columns: acronym, avg_score
    merged = pd.merge(
        user_df[['acronym', 'total_score']],
        class_avg,
        on='acronym',
        how='left'
    )

    # Compute percentile rank for each acronym
    percentile_ranks = []
    for idx, row in merged.iterrows():
        acr = row['acronym']
        user_score = row['total_score']
        # All scores in this acronym
        acr_scores = df[df['acronym'] == acr]['total_score'].tolist()
        percentile = compute_percentile(user_score, acr_scores)
        percentile_ranks.append(percentile)

    merged['percentile'] = percentile_ranks

    # Sort by acronym for consistent plotting
    merged = merged.sort_values('acronym')

    # Prepare data for grouped bar chart
    acronyms = merged['acronym'].tolist()
    user_scores = merged['total_score'].tolist()
    avg_scores = merged['avg_score'].tolist()
    percentiles = merged['percentile'].tolist()

    x = np.arange(len(acronyms))
    width = 0.4

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot "Your Score" bars
    bars_user = ax.bar(x - width/2, user_scores, width, label='Your Score', color='skyblue')
    # Plot "Class Avg" bars
    bars_avg = ax.bar(x + width/2, avg_scores, width, label='Class Avg', color='orange')

    # Annotate percentile rank above the user's bar
    for i, bar in enumerate(bars_user):
        percentile_text = f"{percentiles[i]:.1f}%"
        ax.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            percentile_text,
            ha='center',
            va='bottom',
            fontsize=8,
            color='blue'
        )

    ax.set_xticks(x)
    ax.set_xticklabels(acronyms, rotation=45, ha='right')
    ax.set_ylabel('Total Score')
    ax.set_title(f'Comparative Analysis - Semester {semester}')
    ax.legend()

    plt.tight_layout()
    plt.show()


def view_trend_insights(enrolment_id):
    """
    1. Prompt the user for a semester and subject.
    2. Fetch T1–T4 scores for that subject.
    3. Compute a rolling average over the test scores (moving average).
    4. Ask the user for a goal score and plot a horizontal line representing it.
    5. Display a line chart with:
       - Actual scores
       - Rolling average
       - Goal line
       - Alerts if below goal
    """

    db = DBOperations()

    # Prompt for semester
    sem_input = input("Enter semester for trend insights (1-3): ").strip()
    try:
        semester = int(sem_input)
        if semester not in [1, 2, 3]:
            console.print("[red]Invalid semester. Please enter 1, 2, or 3.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid input. Please enter a numeric semester.[/red]")
        return

    # Use our new helper to let the user pick a subject
    chosen_subject = select_subject(db, enrolment_id, semester)
    if not chosen_subject:
        return  # user gave invalid input or no subjects available

    # Now we have the exact subject string the user chose
    row = db.fetch_test_scores_for_subject(enrolment_id, semester, chosen_subject)
    if not row:
        console.print(f"[yellow]No scores found for '{chosen_subject}' in semester {semester}.[/yellow]")
        return

    # row -> (T1, T2, T3, T4)
    scores = list(row)
    tests = ['T1', 'T2', 'T3', 'T4']

    # Create a small DataFrame for easier rolling calculation
    df = pd.DataFrame({'test': tests, 'score': scores})

    # Compute a rolling average with a chosen window size (e.g., 2)
    # Because we only have 4 tests, a small window is typical
    df['moving_avg'] = df['score'].rolling(window=2, min_periods=1).mean()

    # Prompt for goal (target) score
    goal_input = input("Set a goal (target) score [0-25]: ").strip()
    try:
        goal_score = float(goal_input)
    except ValueError:
        console.print("[red]Invalid goal score. Defaulting to 25.[/red]")
        goal_score = 25.0

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot actual scores
    ax.plot(df['test'], df['score'], marker='o', label='Score', color='blue')

    # Plot moving average
    ax.plot(df['test'], df['moving_avg'], marker='o', linestyle='--', label='Moving Avg', color='green')

    # Plot goal line
    ax.axhline(y=goal_score, color='red', linestyle='-', label=f'Goal = {goal_score}')

    ax.set_title(f"Trend Insights for '{chosen_subject}' - Semester {semester}")
    ax.set_xlabel("Test")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 25)  # each test out of 25

    # Check if below goal
    # We'll highlight points that are below the goal
    for i, score in enumerate(df['score']):
        if score < goal_score:
            ax.text(i, score + 0.5, "Below Goal", ha='center', color='red', fontsize=8)

    ax.legend()
    plt.tight_layout()
    plt.show()

def get_bar_color(mark):
    """Return bar color based on score range."""
    if mark < 9:
        return 'red'
    elif mark <= 15:
        return 'orange'
    elif mark <= 20:
        return 'lightgreen'
    else:
        return 'green'


def generate_subject_figure(subject, T1, T2, T3, T4):
    """
    Generate a side-by-side bar chart (with color-coded bars) and pie chart
    for the given subject/test scores, then save as a PNG.
    Returns the filename of the saved figure.
    """
    tests = ['T1', 'T2', 'T3', 'T4']
    marks = [T1, T2, T3, T4]
    colors = [get_bar_color(m) for m in marks]
    acronym = get_acronym(subject)

    plt.figure(figsize=(10, 4))

    # Bar Chart (left subplot)
    plt.subplot(1, 2, 1)
    plt.bar(tests, marks, color=colors)
    plt.xlabel("Tests")
    plt.ylabel("Marks")
    plt.ylim(0, 25)  # each test is out of 25
    plt.title(f"{acronym} - Test Scores")
    plt.grid(True)

    # Pie Chart (right subplot)
    plt.subplot(1, 2, 2)
    plt.pie(marks, labels=tests, autopct='%1.1f%%', startangle=90)
    plt.title(f"{acronym} - Contribution")

    # Overall figure title
    plt.suptitle(f"Subject: {subject}", y=1.05)
    plt.tight_layout()

    filename = f"subject_{acronym}.png"
    plt.savefig(filename)
    plt.close()
    return filename

def generate_student_report(enrolment_id):
    """
    Generates a detailed PDF performance report for a student,
    including:
      1) Semester-wise table of test scores
      2) Subject-wise bar & pie charts (two graphs on the same page)
      3) Semester-wise Performance (line graph & heatmap)
      4) Comparative Analysis (grouped bar chart)
    """
    db = DBOperations()
    student = db.fetch_student_by_enrolment(enrolment_id)
    if not student:
        console.print("[red]Student record not found.[/red]")
        return

    pdf_file = f"student_report_{enrolment_id}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # -------------------------
    # Title & Student Details
    # -------------------------
    elements.append(Paragraph("Academic Performance Report", styles['Title']))
    elements.append(Spacer(1, 12))
    fullname = student[1]
    details_text = f"<b>Enrolment ID:</b> {enrolment_id}<br/><b>Name:</b> {fullname}"
    elements.append(Paragraph(details_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # -------------------------
    # Section 1: Semester-wise Tables & Subject-wise Graphs
    # -------------------------
    elements.append(Paragraph("1. Individual Subject & Test Scores", styles['Heading2']))
    elements.append(Spacer(1, 12))

    all_scores = db.fetch_all_semester_scores(enrolment_id)

    # Group data by semester
    from collections import defaultdict
    semester_dict = defaultdict(list)
    for row in all_scores:
        # row => (semester, subject, T1, T2, T3, T4, total_score)
        sem = row[0]
        semester_dict[sem].append(row)

    for sem in sorted(semester_dict.keys()):
        sem_data = semester_dict[sem]
        elements.append(Paragraph(f"Semester {sem} Performance", styles['Heading3']))

        # Table of test scores
        table_data = [["Subject", "T1", "T2", "T3", "T4", "Total Score"]]
        for row in sem_data:
            # row => (semester, subject, T1, T2, T3, T4, total_score)
            _, subject, T1, T2, T3, T4, total = row
            acronym = get_acronym(subject)
            table_data.append([acronym, T1, T2, T3, T4, total])

        t = Table(table_data, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # Subject-wise Graphs: bar & pie chart side by side
        elements.append(Paragraph(f"Subject-wise Graphs (Semester {sem})", styles['Heading3']))
        elements.append(Spacer(1, 6))

        for row in sem_data:
            _, subject, T1, T2, T3, T4, total = row
            # Generate bar+pie chart figure for this subject
            fig_file = generate_subject_figure(subject, T1, T2, T3, T4)
            # Insert into PDF
            elements.append(Image(fig_file, width=400, height=200))
            elements.append(Spacer(1, 24))

        # Optional: add a page break after each semester if desired
        # elements.append(PageBreak())

    # -------------------------
    # Helper functions to generate overall graphs (line & heatmap)
    # -------------------------
    def generate_line_graph():
        """Line graph of semester-wise total scores."""
        data = []
        for row in all_scores:
            sem, _, _, _, _, _, total_score = row
            data.append({'semester': sem, 'total_score': total_score})
        if not data:
            return None
        df = pd.DataFrame(data)
        sem_summary = df.groupby('semester')['total_score'].sum().reset_index()
        sem_summary = sem_summary.sort_values('semester')

        plt.figure(figsize=(6,4))
        plt.plot(sem_summary['semester'], sem_summary['total_score'], marker='o', color='blue', linestyle='-')
        plt.xlabel("Semester")
        plt.ylabel("Total Score")
        plt.title("Semester-wise Total Scores")
        plt.grid(True)
        out_file = "line_graph.png"
        plt.tight_layout()
        plt.savefig(out_file)
        plt.close()
        return out_file

    def generate_heatmap():
        """Heatmap: subject (acronym) vs. semester total scores."""
        data = []
        for row in all_scores:
            sem, subject, _, _, _, _, total_score = row
            acr = get_acronym(subject)
            data.append({'semester': sem, 'acronym': acr, 'total_score': total_score})
        if not data:
            return None
        df = pd.DataFrame(data)
        pivot = df.pivot_table(index='acronym', columns='semester', values='total_score', aggfunc='sum').fillna(0)

        plt.figure(figsize=(6,4))
        cax = plt.imshow(pivot.values, cmap='Blues', aspect='auto')
        plt.title("Heatmap: Subject vs. Semester")
        plt.xticks(ticks=np.arange(len(pivot.columns)), labels=[f"Sem {s}" for s in pivot.columns])
        plt.yticks(ticks=np.arange(len(pivot.index)), labels=pivot.index)
        plt.colorbar(cax, label='Total Score')
        out_file = "heatmap.png"
        plt.tight_layout()
        plt.savefig(out_file)
        plt.close()
        return out_file

    def generate_comparative_chart(compare_semester):
        """
        Grouped bar chart comparing the student's score vs. class avg, with percentile rank.
        """
        results = db.fetch_semester_scores_all_students(compare_semester)
        if not results:
            return None
        df = pd.DataFrame(results, columns=['enrolment_id', 'subject', 'total_score'])
        df['acronym'] = df['subject'].apply(get_acronym)

        user_df = df[df['enrolment_id'] == enrolment_id].copy()
        if user_df.empty:
            return None

        class_avg = df.groupby('acronym')['total_score'].mean().reset_index(name='avg_score')
        merged = pd.merge(user_df[['acronym','total_score']], class_avg, on='acronym', how='left')

        def compute_percentile(user_score, scores_list):
            sorted_scores = sorted(scores_list)
            rank = sum(s <= user_score for s in sorted_scores)
            return (rank / len(sorted_scores)) * 100

        percentile_ranks = []
        for acr in merged['acronym']:
            uscore = merged.loc[merged['acronym']==acr, 'total_score'].values[0]
            all_scores = df[df['acronym']==acr]['total_score'].tolist()
            percentile_ranks.append(compute_percentile(uscore, all_scores))

        merged['percentile'] = percentile_ranks
        merged = merged.sort_values('acronym')
        acronyms = merged['acronym'].tolist()
        user_scores = merged['total_score'].tolist()
        avg_scores = merged['avg_score'].tolist()
        percents = merged['percentile'].tolist()

        x = np.arange(len(acronyms))
        width = 0.4
        plt.figure(figsize=(6,4))
        bars_user = plt.bar(x - width/2, user_scores, width, label='Your Score', color='skyblue')
        bars_avg = plt.bar(x + width/2, avg_scores, width, label='Class Avg', color='orange')

        for i, bar in enumerate(bars_user):
            plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                     f"{percents[i]:.1f}%", ha='center', va='bottom', fontsize=8, color='blue')

        plt.xticks(x, acronyms, rotation=45, ha='right')
        plt.ylabel("Total Score")
        plt.title(f"Comparative Analysis - Semester {compare_semester}")
        plt.legend()
        plt.tight_layout()
        out_file = "comparative_analysis.png"
        plt.savefig(out_file)
        plt.close()
        return out_file

    # -------------------------
    # Section 2: Semester-Wise Performance (Line Graph & Heatmap)
    # -------------------------
    elements.append(Paragraph("2. Semester-Wise Performance", styles['Heading2']))
    elements.append(Spacer(1, 12))

    line_file = generate_line_graph()
    if line_file and os.path.exists(line_file):
        elements.append(Paragraph("Line Graph: Semester-wise Total Scores", styles['Heading3']))
        elements.append(Image(line_file, width=400, height=300))
        elements.append(Spacer(1, 12))

    heatmap_file = generate_heatmap()
    if heatmap_file and os.path.exists(heatmap_file):
        elements.append(Paragraph("Heatmap: Subject vs. Semester", styles['Heading3']))
        elements.append(Image(heatmap_file, width=400, height=300))
        elements.append(Spacer(1, 12))

    # -------------------------
    # Section 3: Comparative Analysis
    # -------------------------
    elements.append(Paragraph("3. Comparative Analysis (All Semesters)", styles['Heading2']))
    elements.append(Spacer(1, 12))

    comparative_files = []
    for sem in [1, 2, 3]:
        comp_file = generate_comparative_chart(sem)
        if comp_file and os.path.exists(comp_file):
            # Group heading, spacer, image, and final spacer in one flowable
            comp_flowables = []
            comp_flowables.append(Paragraph(f"Comparative Analysis - Semester {sem}", styles['Heading3']))
            comp_flowables.append(Spacer(1, 6))
            comp_flowables.append(Image(comp_file, width=400, height=300))
            comp_flowables.append(Spacer(1, 12))

            # Wrap them in KeepTogether
            elements.append(KeepTogether(comp_flowables))

            comparative_files.append(comp_file)
        else:
            # No data found for this semester
            elements.append(Paragraph(f"No comparative analysis data available for Semester {sem}.", styles['Normal']))
            elements.append(Spacer(1, 12))

    # Build the PDF
    try:
        doc.build(elements)
        console.print(f"[green]PDF report generated successfully: {pdf_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error generating PDF report: {e}[/red]")

    # Clean up temp images if desired
    temp_files = [line_file, heatmap_file] + comparative_files
    for f in temp_files:
        if f and os.path.exists(f):
            os.remove(f)

    # Also remove subject-wise images if you wish
    # (They were named "subject_{acronym}.png".)
    for sem in semester_dict:
        for row in semester_dict[sem]:
            _, subj, T1, T2, T3, T4, total = row
            acr = get_acronym(subj)
            sf = f"subject_{acr}.png"
            if os.path.exists(sf):
                os.remove(sf)

def student_menu():
    console.print("[bold blue]Student Panel[/bold blue]")
    enrolment_id = input("Enter Enrolment ID: ").strip()

    if not validate_enrolment_id(enrolment_id):
        console.print("[red]Invalid enrolment ID format.[/red]")
        return

    db = DBOperations()
    student = db.fetch_student_by_enrolment(enrolment_id)

    if not student:
        console.print("[red]Student not found.[/red]")
        return

    # Assuming student record is in the format: (enrolment_id, fullname, password, semester)
    fullname = student[1]
    first_word = fullname.split()[0]
    last_four = enrolment_id[-4:]
    expected_password = first_word + last_four

    password = input("Enter Password: ").strip()

    if password != expected_password:
        console.print("[red]Invalid credentials![/red]")
        return

    console.print("[green]Login successful![/green]")

    while True:
        console.print("\n[bold blue]Student Dashboard[/bold blue]")
        console.print("1. View Individual Subject & Test Scores")
        console.print("2. View Semester-Wise Performance")
        console.print("3. Comparative Analysis")
        console.print("4. Trend Insights & Alerts")
        console.print("5. Generate Performance Report")
        console.print("6. Logout")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_individual_scores(enrolment_id)
        elif choice == "2":
            view_semester_performance(enrolment_id)
        elif choice == "3":
            view_comparative_analysis(enrolment_id)
        elif choice == "4":
            view_trend_insights(enrolment_id)
        elif choice == "5":
            generate_student_report(enrolment_id)
        elif choice == "6":
            console.print("Logging out...")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
