-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    enrolment_id VARCHAR(14) PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    semester INT NOT NULL CHECK (semester >= 1 AND semester <= 3)
);

-- Create Faculty Table
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Create Student Scores Table
CREATE TABLE IF NOT EXISTS student_scores (
    enrolment_id VARCHAR(14) REFERENCES students(enrolment_id),
    semester INT CHECK (semester >= 1 AND semester <= 3),
    subject VARCHAR(100) NOT NULL,
    T1 INT CHECK (T1 >= 0 AND T1 <= 25),
    T2 INT CHECK (T2 >= 0 AND T2 <= 25),
    T3 INT CHECK (T3 >= 0 AND T3 <= 25),
    T4 INT CHECK (T4 >= 0 AND T4 <= 25),
    total_score INT CHECK (total_score >= 0 AND total_score <= 100)
);

-- Create Faculty Logs Table
CREATE TABLE IF NOT EXISTS faculty_logs (
    log_id SERIAL PRIMARY KEY,
    faculty_id VARCHAR(10) REFERENCES faculty(faculty_id),
    enrolment_id VARCHAR(14) REFERENCES students(enrolment_id),
    action TEXT,
    old_value TEXT,
    new_value TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
