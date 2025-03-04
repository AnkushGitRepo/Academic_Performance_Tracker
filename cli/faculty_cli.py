from auth.faculty_auth import faculty_login
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from rich.table import Table
from rich.console import Console
from database.db_operations import DBOperations
from utils.input_validation import get_acronym
from cli.student_cli import (
    view_individual_scores,
    view_semester_performance,
    view_comparative_analysis,
    view_trend_insights,
    generate_student_report
)
from utils.Stack_DSA import Stack_DSA

console = Console()


def select_subject(db, enrolment_id, semester):
    """
    Fetch all distinct subjects for a student in a given semester,
    display them in a numbered list, and let the user choose one.
    Returns the chosen subject (full string) or None if cancelled.
    """
    try:
        # Fetch student details to get full name
        student = db.fetch_student_by_enrolment(enrolment_id)
        if student:
            fullname = student[1]
        else:
            fullname = enrolment_id  # fallback if not found

        with db.conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT subject
                FROM student_scores
                WHERE enrolment_id = %s AND semester = %s
                ORDER BY subject
            """, (enrolment_id, semester))
            rows = cur.fetchall()
            if not rows:
                console.print(
                    f"[yellow]No subjects found for student {fullname} ({enrolment_id}) in semester {semester}.[/yellow]")
                return None
            subjects = [row[0] for row in rows]
            console.print()
            console.print(f"Subjects for student [green][bold]{fullname}[/bold][/green] ({enrolment_id}) in semester {semester}:")
            for idx, subj in enumerate(subjects, start=1):
                console.print(f"{idx}. {subj}")
            choice = input("Enter subject number (or type 'cancel' to abort): ").strip()
            if choice.lower() == "cancel":
                return None
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(subjects):
                    return subjects[choice_num - 1]
                else:
                    console.print("[red]Invalid choice number.[/red]")
                    return None
            except ValueError:
                console.print("[red]Invalid input. Expected a number.[/red]")
                return None
    except Exception as e:
        console.print(f"[red]Error selecting subject: {e}[/red]")
        return None


def comprehensive_student_overview():
    """
    Displays a summary table of all students, including
    their overall average score across all semesters & subjects.
    """
    db = DBOperations()

    # 1. Fetch all students
    students = db.fetch_all_students()
    if not students:
        console.print("[yellow]No students found in the database.[/yellow]")
        return

    # 2. Create a Rich table
    table = Table(title="Comprehensive Student Overview")
    table.add_column("Enrolment ID", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="magenta")
    table.add_column("Current Semester", style="green", justify="center")
    table.add_column("Overall Avg Score", style="blue", justify="center")

    # 3. For each student, compute overall average across all semesters
    for enrolment_id, fullname, current_sem in students:
        # Reuse method from student_cli (or DBOperations) to get all scores
        all_scores = db.fetch_all_semester_scores(enrolment_id)
        if not all_scores:
            overall_avg = "No Data"
        else:
            total_score_sum = 0
            total_count = 0
            for row in all_scores:
                # row => (semester, subject, T1, T2, T3, T4, total_score)
                total_score_sum += row[6]  # total_score is at index 6
                total_count += 1

            if total_count > 0:
                overall_avg = round(total_score_sum / total_count, 2)
            else:
                overall_avg = "No Data"

        # 4. Add a row for this student
        table.add_row(
            enrolment_id,
            fullname,
            str(current_sem),
            str(overall_avg)
        )

    # 5. Print the table
    console.print(table)


def individual_student_analysis():
    """
    Prompts the faculty member to enter a student's enrollment ID, displays
    the student's details, and then provides a sub-menu for detailed analysis.
    The analysis options reuse the functions defined in student_cli.py.
    """
    console.print("Enter the Enrollment ID of the student for analysis: ", end="")
    student_id = input().strip()

    db = DBOperations()
    student = db.fetch_student_by_enrolment(student_id)
    if not student:
        console.print("[red]Student not found.[/red]")
        return

    # Assuming student record is in the format: (enrolment_id, fullname, password, semester)
    console.print(
        f"[green]Student Found:[/green] {student[1]} (Enrollment: {student[0]}) - Current Semester: {student[3]}")

    while True:
        console.print("\n[bold blue]Individual Student Analysis Menu[/bold blue]")
        console.print("1. View Individual Subject & Test Scores")
        console.print("2. View Semester-Wise Performance")
        console.print("3. Comparative Analysis")
        console.print("4. Trend Insights & Alerts")
        console.print("5. Generate Performance Report")
        console.print("6. Back to Faculty Dashboard")

        console.print("Enter your choice: ", end="")
        choice = input().strip()
        if choice == "1":
            view_individual_scores(student_id)
        elif choice == "2":
            view_semester_performance(student_id)
        elif choice == "3":
            view_comparative_analysis(student_id)
        elif choice == "4":
            view_trend_insights(student_id)
        elif choice == "5":
            generate_student_report(student_id)
        elif choice == "6":
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")


def class_semester_trends():
    """
    Displays class-wide trends:
      1) A line graph of the average total score per semester across all students.
      2) A heatmap of the average total score per subject (acronym) per semester.
    """
    db = DBOperations()

    # Fetch all student scores from the database.
    # This method should return a list of tuples:
    # (enrolment_id, subject, T1, T2, T3, T4, total_score, semester)
    all_scores = db.fetch_all_student_scores()
    if not all_scores:
        console.print("[red]No class data available.[/red]")
        return

    # Convert data to a pandas DataFrame.
    df = pd.DataFrame(
        all_scores,
        columns=['enrolment_id', 'subject', 'T1', 'T2', 'T3', 'T4', 'total_score', 'semester']
    )

    # -------------------------------
    # 1. Line Graph: Average Total Score per Semester
    # -------------------------------
    sem_summary = df.groupby('semester')['total_score'].mean().reset_index().sort_values('semester')

    # -------------------------------
    # 2. Heatmap: Average Total Score by Subject (Acronym) and Semester
    # -------------------------------
    df['acronym'] = df['subject'].apply(get_acronym)
    pivot = df.pivot_table(index='acronym', columns='semester', values='total_score', aggfunc='mean').fillna(0)

    # Create subplots: one for the line graph and one for the heatmap
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))

    # Plot the line graph on ax1.
    ax1.plot(sem_summary['semester'], sem_summary['total_score'], marker='o', color='blue', linestyle='-')
    ax1.set_xlabel("Semester")
    ax1.set_ylabel("Average Total Score")
    ax1.set_title("Class Average Total Score by Semester")
    ax1.grid(True)

    # Plot the heatmap on ax2.
    cax = ax2.imshow(pivot.values, cmap='Blues', aspect='auto')
    ax2.set_title("Heatmap: Avg Total Score by Subject and Semester")
    ax2.set_xticks(range(len(pivot.columns)))
    ax2.set_xticklabels([f"Sem {s}" for s in pivot.columns], rotation=45)
    ax2.set_yticks(range(len(pivot.index)))
    ax2.set_yticklabels(pivot.index)
    fig.colorbar(cax, ax=ax2, orientation='vertical', label='Avg Total Score')

    plt.tight_layout()
    plt.show()


def audit_log_data(faculty_id):
    """
    Fetches audit logs for the given faculty_id, stores them in a stack,
    and then displays the logs in LIFO order.
    """
    db = DBOperations()
    logs = db.fetch_faculty_logs(faculty_id)
    if not logs:
        console.print("[yellow]No audit logs found for your account.[/yellow]")
        return

    # Create a stack and push all log entries onto it.
    log_stack = Stack_DSA()
    for log_entry in logs:
        log_stack.push(log_entry)

    console.print("[bold blue]Audit Log Data (Most Recent on Top):[/bold blue]")
    while not log_stack.is_empty():
        log_entry = log_stack.pop()
        # log_entry format: (log_id, faculty_id, enrolment_id, action, old_value, new_value, timestamp)
        log_text = (
            f"[cyan]Log ID:[/cyan] {log_entry[0]} | "
            f"[cyan]Student:[/cyan] {log_entry[2]} | "
            f"[cyan]Action:[/cyan] {log_entry[3]} | "
            f"[cyan]Old Value:[/cyan] {log_entry[4]} | "
            f"[cyan]New Value:[/cyan] {log_entry[5]} | "
            f"[cyan]Time:[/cyan] {log_entry[6]}"
        )
        console.print(log_text)



def data_driven_interventions():
    console.print("Filtering students based on set criteria...")

    # Prompt for filtering parameters (optional)
    min_avg_input = input("Enter minimum overall average score (or press Enter for no filter): ").strip()
    max_avg_input = input("Enter maximum overall average score (or press Enter for no filter): ").strip()

    try:
        min_avg = float(min_avg_input) if min_avg_input else None
    except ValueError:
        console.print("[yellow]Invalid input for minimum average; ignoring this filter.[/yellow]")
        min_avg = None

    try:
        max_avg = float(max_avg_input) if max_avg_input else None
    except ValueError:
        console.print("[yellow]Invalid input for maximum average; ignoring this filter.[/yellow]")
        max_avg = None

    db = DBOperations()

    # Fetch all students (each student record: (enrolment_id, fullname, semester))
    students = db.fetch_all_students()
    if not students:
        console.print("[yellow]No students found in the database.[/yellow]")
        return

    results_table = []
    # For each student, compute the overall average score
    for student in students:
        enrolment_id, fullname, current_sem = student
        all_scores = db.fetch_all_semester_scores(enrolment_id)
        if not all_scores:
            overall_avg = None
        else:
            total = sum(row[6] for row in all_scores)  # total_score is at index 6
            count = len(all_scores)
            overall_avg = total / count if count > 0 else None
        results_table.append((enrolment_id, fullname, current_sem, overall_avg))

    # Filter results based on provided criteria
    filtered_students = []
    for rec in results_table:
        enrolment_id, fullname, current_sem, overall_avg = rec
        # Skip student if no data available
        if overall_avg is None:
            continue
        if min_avg is not None and overall_avg < min_avg:
            continue
        if max_avg is not None and overall_avg > max_avg:
            continue
        filtered_students.append(rec)

    if not filtered_students:
        console.print("[yellow]No students match the filtering criteria.[/yellow]")
        return

    # Display the filtered students using a Rich table
    from rich.table import Table
    table = Table(title="Filtered Students Based on Overall Average Score")
    table.add_column("Enrollment ID", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="magenta")
    table.add_column("Current Semester", justify="center", style="green")
    table.add_column("Overall Avg Score", justify="center", style="blue")

    for rec in filtered_students:
        enrolment_id, fullname, current_sem, overall_avg = rec
        table.add_row(enrolment_id, fullname, str(current_sem), f"{overall_avg:.2f}")

    console.print(table)


def real_time_updates(faculty_id):
    """
      1. Ask for the student's enrollment ID.
      2. Verify the student exists.
      3. Ask for the semester to update.
      4. Display all subjects for that semester (using select_subject).
      5. Ask the faculty to choose a subject (by number, acronym, or name).
      6. Fetch and display the current test scores for that subject.
      7. Ask which test (T1, T2, T3, or T4) to update.
      8. Ask for the new score (integer between 0 and 25).
      9. Update the record, recalculate total score, and log the change.
      At any step, entering "cancel" will abort the update.
    """
    db = DBOperations()

    # Step 1: Ask for student's enrollment ID
    student_id = input("Enter the student's Enrollment ID (or 'cancel' to abort): ").strip()
    if student_id.lower() == "cancel":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    # Step 2: Verify student exists
    student = db.fetch_student_by_enrolment(student_id)
    if not student:
        console.print(f"[red]No student found with Enrollment ID: {student_id}.[/red]")
        return

    # Step 3: Ask for semester (1-3)
    sem_input = input("Enter the semester to update (1-3) (or 'cancel' to abort): ").strip()
    if sem_input.lower() == "cancel":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return
    try:
        semester = int(sem_input)
        if semester not in [1, 2, 3]:
            console.print("[red]Invalid semester. Operation aborted.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid input. Operation aborted.[/red]")
        return

    # Step 4: Display all subjects for that student and semester using select_subject.
    # We assume select_subject is already defined in student_cli and imported.
    chosen_subject = select_subject(db, student_id, semester)
    if not chosen_subject:
        console.print("[yellow]No subject selected. Operation cancelled.[/yellow]")
        return

    # Step 5: Fetch current test scores for the selected subject.
    row = db.fetch_test_scores_for_subject(student_id, semester, chosen_subject)
    if not row:
        console.print(f"[red]No test scores found for subject '{chosen_subject}' in semester {semester}.[/red]")
        return
    # row is assumed to be a tuple: (T1, T2, T3, T4)
    T1, T2, T3, T4 = row
    console.print(f"Current scores for '{chosen_subject}': T1={T1}, T2={T2}, T3={T3}, T4={T4}")

    # Step 6: Ask which test to update
    test_field = input("Enter the test field to update (T1, T2, T3, T4) (or 'cancel' to abort): ").strip().upper()
    if test_field.lower() == "cancel":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return
    if test_field not in ['T1', 'T2', 'T3', 'T4']:
        console.print("[red]Invalid test field. Operation aborted.[/red]")
        return

    # Step 7: Ask for the new score value
    new_value_input = input(f"Enter the new score for {test_field} (0-25) (or 'cancel' to abort): ").strip()
    if new_value_input.lower() == "cancel":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return
    try:
        new_value = int(new_value_input)
        if new_value < 0 or new_value > 25:
            console.print("[red]Score must be between 0 and 25. Operation aborted.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid score input. Operation aborted.[/red]")
        return

    # Step 8: Update the student's test score using DBOperations
    update_result = db.update_student_test_score(student_id, semester, chosen_subject, test_field, new_value)
    if not update_result:
        console.print("[red]Failed to update the score. Operation aborted.[/red]")
        return

    old_value, new_total = update_result

    # Prepare a log message
    action_msg = (f"Updated {chosen_subject} {test_field}: {old_value} -> {new_value}, "
                  f"new total score = {new_total}")
    # Step 9: Insert a log record into faculty_logs table.
    db.insert_faculty_log(faculty_id, student_id, action_msg, str(old_value), str(new_value))
    console.print("[green]Update successful![/green]")
    console.print(f"[green]{action_msg}[/green]")


def faculty_menu():
    console.print("[bold blue]Faculty Panel[/bold blue]")
    faculty_id = input("Enter Faculty ID: ").strip()
    password = input("Enter Password: ").strip()

    if not faculty_login(faculty_id, password):
        console.print("[red]Invalid credentials![/red]")
        return

    console.print("[green]Login successful![/green]")
    db = DBOperations()

    while True:
        console.print("\n[bold blue]Faculty Dashboard[/bold blue]")
        console.print("1. Comprehensive Student Overview")
        console.print("2. Individual Student Analysis")
        console.print("3. Class & Semester Trends")
        console.print("4. Audit & Log Data")
        console.print("5. Data-Driven Interventions")
        console.print("6. Real-Time Data Updates & Editing")
        console.print("7. Logout")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            comprehensive_student_overview()
        elif choice == "2":
            individual_student_analysis()
        elif choice == "3":
            class_semester_trends()
        elif choice == "4":
            audit_log_data(faculty_id)
        elif choice == "5":
            data_driven_interventions()
        elif choice == "6":
            real_time_updates(faculty_id)
        elif choice == "7":
            console.print("Logging out...")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
