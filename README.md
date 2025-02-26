# Academic Performance Tracker

A Python CLI-based application to track and analyze student academic performance over three semesters.  
Faculty members can manage student records, analyze performance, update data in real time, and generate detailed reports.  
Students can view their own performance metrics, visualizations, and generate performance reports.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [CLI Usage](#cli-usage)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## Overview

The Academic Performance Tracker is a command-line application developed in Python that helps track and analyze student performance over three semesters. Faculty members and students have dedicated interfaces:
  
- **Faculty Panel:**  
  - Comprehensive student overview
  - Detailed analysis for individual students
  - Class and semester trends visualization
  - Real-time updates to student records with audit logs
  - Data-driven interventions and customized reports
  
- **Student Panel:**  
  - View individual subject and test scores with interactive charts
  - Semester-wise performance insights (line graphs and heatmaps)
  - Comparative analysis against class averages
  - Trend insights with moving averages and goal tracking
  - PDF report generation of academic performance

---

## Features

### Faculty Panel

- **Secure Login:** Faculty authentication with encrypted passwords.
- **Comprehensive Student Overview:** View all students with overall average scores.
- **Individual Student Analysis:** Drill-down into a student's performance across semesters.
- **Class & Semester Trends:** Visualize class performance using line graphs and heatmaps.
- **Audit & Log Data:** Maintain an audit trail of changes made to student records.
- **Data-Driven Interventions:** Filter students based on performance criteria.
- **Customized Reports:** Generate PDF reports that include tables, graphs, and comparative analyses.
- **Real-Time Updates:** Update student records with immediate reflection and logging.

### Student Panel

- **Secure Login:** Student authentication using a default password scheme.
- **View Performance:** Visualize individual subject scores with bar and pie charts.
- **Semester-Wise Analysis:** Access performance trends via line graphs and heatmaps.
- **Comparative Analysis:** Compare personal scores with class averages.
- **Trend Insights & Alerts:** View moving averages, set target goals, and receive alerts.
- **PDF Reports:** Generate detailed performance reports.

---

## Tech Stack

- **Programming Language:** Python 3.x
- **Database:** PostgreSQL
- **Libraries & Tools:**
  - Data Manipulation: `pandas`, `numpy`
  - Visualization: `matplotlib`
  - CLI Enhancements: `argparse`, `rich`
  - Database Connectivity: `psycopg2` (or `psycopg2-binary` for easier installation)
  - PDF Generation: `reportlab`, `pdfkit`
  - Password Hashing: `bcrypt`

---

## Project Structure

```
Academic_Performance_Tracker/
├── cli/
│   ├── faculty_cli.py         # Faculty panel CLI implementation
│   └── student_cli.py         # Student panel CLI implementation
├── database/
│   ├── db_init.sql            # SQL script to initialize the database schema
│   └── db_operations.py       # Database connection and CRUD operations
├── utils/
│   ├── error_handling.py      # Custom error handling utilities
│   └── input_validation.py    # Input validation and helper functions (e.g., get_acronym)
├── README.md                  # This file
├── requirements.txt           # Python dependencies list
└── main.py                    # Entry point for the application
```

---

## Setup Instructions

### Prerequisites

- **Python 3.x:** Ensure Python 3.9+ is installed.
- **PostgreSQL:** Install and run PostgreSQL. Download from [postgresql.org](https://www.postgresql.org/download/).
- **Git:** Optional (for cloning the repository).

### Installation

1. **Clone the Repository:**

   ```bash
   git clone git@github.com:AnkushGitRepo/Academic_Performance_Tracker.git
   cd Academic_Performance_Tracker
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # For Windows: .venv\Scripts\activate
   ```

3. **Install Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

   This installs all necessary packages, including:
   - `psycopg2-binary`
   - `pandas`
   - `numpy`
   - `matplotlib`
   - `reportlab`
   - `rich`
   - `bcrypt`

### Database Setup

1. **Create the Database:**

   Launch your PostgreSQL client (e.g., psql or pgAdmin) and create a new database:

   ```sql
   CREATE DATABASE academic_db;
   ```

2. **Initialize the Database Schema:**

   Execute the provided SQL script to create tables:

   ```bash
   psql -U <username> -d academic_db -f database/db_init.sql
   ```

   Replace `<username>` with your PostgreSQL username.

3. **Configure Database Connection:**

   Update the connection parameters in `database/db_operations.py` (e.g., `dbname`, `user`, `password`, `host`, `port`).

---

## Running the Application

1. **Activate the Virtual Environment (if not already active):**

   ```bash
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. **Run the Application:**

   From the project root directory, run:

   ```bash
   python main.py
   ```

   You will be presented with a menu to choose between:
   - Faculty Login
   - Student Login
   - Exit

---

## CLI Usage

### Faculty Panel

After logging in as a faculty member, you have multiple options, including:

1. **Comprehensive Student Overview:**  
   View a table summarizing all students and their overall average scores.

2. **Individual Student Analysis:**  
   Select a student by enrollment ID and access detailed performance analysis (individual scores, semester trends, comparative analysis, etc.).

3. **Class & Semester Trends:**  
   View class-wide performance trends with line graphs and heatmaps.

4. **Audit & Log Data:**  
   Review audit logs of any modifications made to student records.

5. **Data-Driven Interventions:**  
   Filter students based on performance criteria (e.g., overall average score thresholds).

6. **Generate Customized Report:**  
   Generate a detailed PDF report with tables and visualizations.

7. **Real-Time Data Updates & Editing:**  
   Update student records in real time and automatically log the changes.

8. **Performance Trends & Cohort Analysis:**  
   (Planned enhancements)

9. **Logout:**  
   Exit the faculty panel.

### Student Panel

After logging in as a student, the options include:

1. **View Individual Subject & Test Scores:**  
   Display subject-wise scores with bar and pie charts.

2. **View Semester-Wise Performance:**  
   Visualize performance trends with line graphs and heatmaps.

3. **Comparative Analysis:**  
   Compare personal performance against class averages.

4. **Trend Insights & Alerts:**  
   Analyze trends with moving averages and set target goals.

5. **Generate Performance Report:**  
   Create a comprehensive PDF report of performance.

6. **Logout:**  
   Exit the student panel.

---

## Terminal Commands Summary

- **Clone the Repository:**

  ```bash
  git clone <repository_url>
  cd Academic_Performance_Tracker
  ```

- **Create & Activate Virtual Environment (Linux/macOS):**

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Create & Activate Virtual Environment (Windows):**

  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **Install Dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

- **Initialize the Database:**

  ```bash
  psql -U <username> -d academic_db -f database/db_init.sql
  ```

- **Run the Application:**

  ```bash
  python main.py
  ```

---

## Troubleshooting

- **ModuleNotFoundError:**  
  Ensure that your PYTHONPATH includes the project root. Use relative imports if needed.

- **Database Connection Issues:**  
  Confirm that PostgreSQL is running and your connection parameters in `db_operations.py` are correct.

- **Psycopg2 Errors:**  
  If encountering errors with `psycopg2`, try using `psycopg2-binary` as listed in `requirements.txt`.

- **Graphical Issues:**  
  Ensure that your environment supports graphical display for matplotlib. If running on a headless server, consider saving graphs as images.

---

## Future Enhancements

- Develop a web interface using frameworks such as Flask or Django.
- Integrate advanced analytics and machine learning for predictive performance insights.
- Enhance PDF reports with interactive visualizations.
- Extend audit logging and real-time data update functionalities.
- Implement additional performance metrics and cohort analysis features.

---

## Contributing

Contributions are welcome!  
Please fork the repository and create a pull request. For major changes, please open an issue first to discuss what you would like to change.
