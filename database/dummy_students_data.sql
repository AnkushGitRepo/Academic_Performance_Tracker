------------------------------
-- Student Records Insertion
------------------------------
-- Reference Student
INSERT INTO students (enrolment_id, fullname, password, semester)
VALUES ('23002171410016', 'Ankush Gupta', 'Ankush0016', 3);

-- 9 Additional Students
INSERT INTO students (enrolment_id, fullname, password, semester)
VALUES
  ('23002171410017', 'Rahul Sharma', 'Rahul0017', 3),
  ('23002171410018', 'Priya Singh', 'Priya0018', 3),
  ('23002171410019', 'Amit Kumar', 'Amit0019', 3),
  ('23002171410020', 'Sneha Verma', 'Sneha0020', 3),
  ('23002171410021', 'Vikram Patel', 'Vikram0021', 3),
  ('23002171410022', 'Ritika Mehta', 'Ritika0022', 3),
  ('23002171410023', 'Karan Joshi', 'Karan0023', 3),
  ('23002171410024', 'Deepika Rao', 'Deepika0024', 3),
  ('23002171410025', 'Suresh Reddy', 'Suresh0025', 3);

-------------------------------------------------
-- Student Scores: Semester 1 (4 subjects each)
-------------------------------------------------
-- For Ankush Gupta (Reference Data)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410016', 1, 'Software Engineering (SE)', 19.5, 13.5, 13.5, 10.5, 57),
  ('23002171410016', 1, 'Physics (PHY)', 14, 9.5, 11.5, 17, 52),
  ('23002171410016', 1, 'MATHS I (MATHS-I)', 0, 5, 7, 18, 30),
  ('23002171410016', 1, 'JAVA-I', 10, 8, 17, 16, 51);

-- For Rahul Sharma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410017', 1, 'Software Engineering (SE)', 23, 22, 21, 20, 86),
  ('23002171410017', 1, 'Physics (PHY)', 22, 20, 21, 22, 85),
  ('23002171410017', 1, 'MATHS I (MATHS-I)', 20, 19, 21, 20, 80),
  ('23002171410017', 1, 'JAVA-I', 22, 21, 20, 23, 86);

-- For Priya Singh (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410018', 1, 'Software Engineering (SE)', 16, 15, 14, 13, 58),
  ('23002171410018', 1, 'Physics (PHY)', 15, 14, 13, 15, 57),
  ('23002171410018', 1, 'MATHS I (MATHS-I)', 10, 12, 11, 10, 43),
  ('23002171410018', 1, 'JAVA-I', 14, 13, 15, 14, 56);

-- For Amit Kumar (Below Average/Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410019', 1, 'Software Engineering (SE)', 8, 7, 6, 5, 26),
  ('23002171410019', 1, 'Physics (PHY)', 7, 6, 5, 8, 26),
  ('23002171410019', 1, 'MATHS I (MATHS-I)', 4, 5, 6, 5, 20),
  ('23002171410019', 1, 'JAVA-I', 6, 5, 4, 7, 22);

-- For Sneha Verma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410020', 1, 'Software Engineering (SE)', 24, 23, 22, 23, 92),
  ('23002171410020', 1, 'Physics (PHY)', 23, 22, 23, 24, 92),
  ('23002171410020', 1, 'MATHS I (MATHS-I)', 22, 23, 24, 22, 91),
  ('23002171410020', 1, 'JAVA-I', 23, 24, 23, 24, 94);

-- For Vikram Patel (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410021', 1, 'Software Engineering (SE)', 15, 14, 15, 14, 58),
  ('23002171410021', 1, 'Physics (PHY)', 14, 13, 14, 15, 56),
  ('23002171410021', 1, 'MATHS I (MATHS-I)', 12, 11, 10, 11, 44),
  ('23002171410021', 1, 'JAVA-I', 13, 12, 13, 12, 50);

-- For Ritika Mehta (Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410022', 1, 'Software Engineering (SE)', 5, 6, 5, 4, 20),
  ('23002171410022', 1, 'Physics (PHY)', 4, 5, 5, 4, 18),
  ('23002171410022', 1, 'MATHS I (MATHS-I)', 3, 4, 3, 4, 14),
  ('23002171410022', 1, 'JAVA-I', 5, 4, 4, 5, 18);

-- For Karan Joshi (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410023', 1, 'Software Engineering (SE)', 16, 15, 15, 14, 60),
  ('23002171410023', 1, 'Physics (PHY)', 15, 14, 15, 14, 58),
  ('23002171410023', 1, 'MATHS I (MATHS-I)', 11, 12, 11, 12, 46),
  ('23002171410023', 1, 'JAVA-I', 14, 13, 14, 13, 54);

-- For Deepika Rao (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410024', 1, 'Software Engineering (SE)', 23, 22, 22, 23, 90),
  ('23002171410024', 1, 'Physics (PHY)', 22, 22, 22, 23, 89),
  ('23002171410024', 1, 'MATHS I (MATHS-I)', 21, 22, 23, 22, 88),
  ('23002171410024', 1, 'JAVA-I', 22, 23, 22, 23, 90);

-- For Suresh Reddy (Below Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410025', 1, 'Software Engineering (SE)', 10, 9, 8, 9, 36),
  ('23002171410025', 1, 'Physics (PHY)', 9, 8, 9, 8, 34),
  ('23002171410025', 1, 'MATHS I (MATHS-I)', 7, 6, 7, 6, 26),
  ('23002171410025', 1, 'JAVA-I', 8, 7, 8, 7, 30);

-------------------------------------------------
-- Student Scores: Semester 2 (5 subjects each)
-------------------------------------------------
-- For Ankush Gupta
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410016', 2, 'Data Structures using JAVA (DS)', 13.5, 15, 12.5, 11.5, 52.5),
  ('23002171410016', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 10, 13.5, 15, 20, 58.5),
  ('23002171410016', 2, 'JAVA-II', 13.5, 15, 16, 16.5, 61),
  ('23002171410016', 2, 'Database Management System (DBMS)', 17.5, 17, 18, 15, 67.5),
  ('23002171410016', 2, 'MATHS II (MATHS-II)', 11, 9, 7, 2.5, 29.5);

-- For Rahul Sharma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410017', 2, 'Data Structures using JAVA (DS)', 23, 22, 21, 22, 88),
  ('23002171410017', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 21, 22, 23, 22, 88),
  ('23002171410017', 2, 'JAVA-II', 22, 23, 22, 21, 88),
  ('23002171410017', 2, 'Database Management System (DBMS)', 24, 23, 22, 24, 93),
  ('23002171410017', 2, 'MATHS II (MATHS-II)', 21, 20, 22, 21, 84);

-- For Priya Singh (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410018', 2, 'Data Structures using JAVA (DS)', 15, 14, 16, 15, 60),
  ('23002171410018', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 14, 15, 14, 16, 59),
  ('23002171410018', 2, 'JAVA-II', 15, 15, 15, 15, 60),
  ('23002171410018', 2, 'Database Management System (DBMS)', 16, 15, 15, 16, 62),
  ('23002171410018', 2, 'MATHS II (MATHS-II)', 12, 11, 10, 10, 43);

-- For Amit Kumar (Below Average/Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410019', 2, 'Data Structures using JAVA (DS)', 7, 6, 5, 7, 25),
  ('23002171410019', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 6, 7, 6, 8, 27),
  ('23002171410019', 2, 'JAVA-II', 7, 6, 5, 6, 24),
  ('23002171410019', 2, 'Database Management System (DBMS)', 8, 7, 7, 8, 30),
  ('23002171410019', 2, 'MATHS II (MATHS-II)', 5, 4, 4, 5, 18);

-- For Sneha Verma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410020', 2, 'Data Structures using JAVA (DS)', 24, 23, 24, 23, 94),
  ('23002171410020', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 23, 24, 23, 24, 94),
  ('23002171410020', 2, 'JAVA-II', 24, 24, 23, 24, 95),
  ('23002171410020', 2, 'Database Management System (DBMS)', 25, 24, 25, 24, 98),
  ('23002171410020', 2, 'MATHS II (MATHS-II)', 23, 22, 23, 23, 91);

-- For Vikram Patel (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410021', 2, 'Data Structures using JAVA (DS)', 14, 15, 14, 15, 58),
  ('23002171410021', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 13, 14, 13, 15, 55),
  ('23002171410021', 2, 'JAVA-II', 14, 14, 15, 14, 57),
  ('23002171410021', 2, 'Database Management System (DBMS)', 15, 14, 14, 15, 58),
  ('23002171410021', 2, 'MATHS II (MATHS-II)', 11, 10, 11, 10, 42);

-- For Ritika Mehta (Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410022', 2, 'Data Structures using JAVA (DS)', 4, 5, 4, 5, 18),
  ('23002171410022', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 3, 4, 3, 4, 14),
  ('23002171410022', 2, 'JAVA-II', 4, 3, 4, 3, 14),
  ('23002171410022', 2, 'Database Management System (DBMS)', 5, 4, 5, 4, 18),
  ('23002171410022', 2, 'MATHS II (MATHS-II)', 3, 3, 4, 3, 13);

-- For Karan Joshi (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410023', 2, 'Data Structures using JAVA (DS)', 15, 14, 15, 14, 58),
  ('23002171410023', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 14, 15, 14, 15, 58),
  ('23002171410023', 2, 'JAVA-II', 15, 14, 15, 14, 58),
  ('23002171410023', 2, 'Database Management System (DBMS)', 16, 15, 16, 15, 62),
  ('23002171410023', 2, 'MATHS II (MATHS-II)', 12, 11, 12, 11, 46);

-- For Deepika Rao (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410024', 2, 'Data Structures using JAVA (DS)', 23, 22, 23, 22, 90),
  ('23002171410024', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 22, 23, 22, 23, 90),
  ('23002171410024', 2, 'JAVA-II', 23, 23, 22, 23, 91),
  ('23002171410024', 2, 'Database Management System (DBMS)', 24, 23, 24, 23, 94),
  ('23002171410024', 2, 'MATHS II (MATHS-II)', 22, 22, 23, 22, 89);

-- For Suresh Reddy (Below Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410025', 2, 'Data Structures using JAVA (DS)', 9, 8, 9, 8, 34),
  ('23002171410025', 2, 'Fundamental of Electronics and Electrical Engineering (FEE)', 8, 7, 8, 7, 30),
  ('23002171410025', 2, 'JAVA-II', 9, 8, 9, 8, 34),
  ('23002171410025', 2, 'Database Management System (DBMS)', 10, 9, 10, 9, 38),
  ('23002171410025', 2, 'MATHS II (MATHS-II)', 7, 6, 7, 6, 26);

-------------------------------------------------
-- Student Scores: Semester 3 (5 subjects each)
-------------------------------------------------
-- For Ankush Gupta
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410016', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 11.5, 16.5, 14.5, 13.5, 56),
  ('23002171410016', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 22, 13, 24, 17.5, 76.5),
  ('23002171410016', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 21, 16, 21, 17.5, 75.5),
  ('23002171410016', 3, 'Digital Electronics (DE)', 19, 12, 11, 11, 53),
  ('23002171410016', 3, 'Effective Technical Communication (ETC)', 20.5, 18, 25, 15, 78.5);

-- For Rahul Sharma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410017', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 22, 23, 22, 23, 90),
  ('23002171410017', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 25, 24, 23, 24, 96),
  ('23002171410017', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 24, 25, 24, 25, 98),
  ('23002171410017', 3, 'Digital Electronics (DE)', 23, 22, 21, 22, 88),
  ('23002171410017', 3, 'Effective Technical Communication (ETC)', 24, 23, 25, 24, 96);

-- For Priya Singh (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410018', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 14, 15, 14, 15, 58),
  ('23002171410018', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 18, 17, 18, 17, 70),
  ('23002171410018', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 17, 16, 17, 16, 66),
  ('23002171410018', 3, 'Digital Electronics (DE)', 15, 14, 14, 15, 58),
  ('23002171410018', 3, 'Effective Technical Communication (ETC)', 16, 15, 16, 15, 62);

-- For Amit Kumar (Below Average/Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410019', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 6, 5, 5, 6, 22),
  ('23002171410019', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 8, 7, 7, 8, 30),
  ('23002171410019', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 7, 6, 6, 7, 26),
  ('23002171410019', 3, 'Digital Electronics (DE)', 5, 4, 5, 4, 18),
  ('23002171410019', 3, 'Effective Technical Communication (ETC)', 6, 5, 6, 5, 22);

-- For Sneha Verma (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410020', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 24, 23, 24, 23, 94),
  ('23002171410020', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 25, 25, 24, 25, 99),
  ('23002171410020', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 24, 25, 25, 24, 98),
  ('23002171410020', 3, 'Digital Electronics (DE)', 23, 24, 23, 23, 93),
  ('23002171410020', 3, 'Effective Technical Communication (ETC)', 25, 24, 25, 24, 98);

-- For Vikram Patel (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410021', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 13, 14, 13, 14, 54),
  ('23002171410021', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 17, 16, 17, 16, 66),
  ('23002171410021', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 16, 15, 16, 15, 62),
  ('23002171410021', 3, 'Digital Electronics (DE)', 14, 13, 14, 13, 54),
  ('23002171410021', 3, 'Effective Technical Communication (ETC)', 15, 14, 15, 14, 58);

-- For Ritika Mehta (Failing)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410022', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 4, 4, 4, 4, 16),
  ('23002171410022', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 5, 5, 5, 5, 20),
  ('23002171410022', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 4, 4, 4, 4, 16),
  ('23002171410022', 3, 'Digital Electronics (DE)', 3, 3, 3, 3, 12),
  ('23002171410022', 3, 'Effective Technical Communication (ETC)', 4, 4, 4, 4, 16);

-- For Karan Joshi (Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410023', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 15, 14, 15, 14, 58),
  ('23002171410023', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 19, 18, 19, 18, 74),
  ('23002171410023', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 18, 17, 18, 17, 70),
  ('23002171410023', 3, 'Digital Electronics (DE)', 15, 14, 15, 14, 58),
  ('23002171410023', 3, 'Effective Technical Communication (ETC)', 16, 15, 16, 15, 62);

-- For Deepika Rao (Topper)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410024', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 23, 22, 23, 22, 90),
  ('23002171410024', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 25, 24, 25, 24, 98),
  ('23002171410024', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 24, 25, 24, 25, 98),
  ('23002171410024', 3, 'Digital Electronics (DE)', 23, 22, 23, 22, 90),
  ('23002171410024', 3, 'Effective Technical Communication (ETC)', 24, 23, 24, 23, 94);

-- For Suresh Reddy (Below Average)
INSERT INTO student_scores (enrolment_id, semester, subject, T1, T2, T3, T4, total_score)
VALUES
  ('23002171410025', 3, 'Introduction to Probability Theory and Stochastic Processes (PS)', 8, 7, 8, 7, 30),
  ('23002171410025', 3, 'Fundamentals of Computer Science using Python - I (FCSP-I)', 10, 9, 10, 9, 38),
  ('23002171410025', 3, 'Full Stack Development with Javascript-1 (FSD-I)', 9, 8, 9, 8, 34),
  ('23002171410025', 3, 'Digital Electronics (DE)', 8, 7, 8, 7, 30),
  ('23002171410025', 3, 'Effective Technical Communication (ETC)', 9, 8, 9, 8, 34);
