import psycopg2
from psycopg2 import Error
from utils.error_handling import log_error

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="academic_db",
            user="postgres",
            password="1806",
            host="localhost",
            port="5432"
        )
        return conn
    except Error as e:
        log_error("Database connection failed", e)
        raise e

class DBOperations:
    def __init__(self):
        self.conn = get_connection()

    def fetch_student_by_enrolment(self, enrolment_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM students WHERE enrolment_id = %s", (enrolment_id,))
                student = cur.fetchone()
                return student
        except Error as e:
            log_error("Error fetching student", e)
            return None

    # Example update function for student score (expand as needed)
    def update_student_score(self, enrolment_id, subject, new_total_score):
        try:
            with self.conn.cursor() as cur:
                query = """
                UPDATE student_scores
                SET total_score = %s
                WHERE enrolment_id = %s AND subject = %s
                """
                cur.execute(query, (new_total_score, enrolment_id, subject))
                self.conn.commit()
                return True
        except Error as e:
            log_error("Error updating student score", e)
            self.conn.rollback()
            return False


    def fetch_student_scores(self, enrolment_id, semester):
        """
        Fetch subject-wise test scores for the given student and semester.
        Returns a list of tuples: (subject, T1, T2, T3, T4, total_score)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT subject, T1, T2, T3, T4, total_score FROM student_scores WHERE enrolment_id = %s AND semester = %s",
                    (enrolment_id, semester)
                )
                results = cur.fetchall()
                return results
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching student scores", e)
            return []

    def fetch_all_semester_scores(self, enrolment_id):
        """
        Fetch all semesters' scores for the given student.
        Returns a list of tuples: (semester, subject, T1, T2, T3, T4, total_score).
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT semester, subject, T1, T2, T3, T4, total_score
                    FROM student_scores
                    WHERE enrolment_id = %s
                    ORDER BY semester, subject
                """
                cur.execute(query, (enrolment_id,))
                return cur.fetchall()
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching all semester scores", e)
            return []

    def fetch_semester_scores_all_students(self, semester):
        """
        Fetch (enrolment_id, subject, total_score) for all students in the given semester.
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT enrolment_id, subject, total_score
                    FROM student_scores
                    WHERE semester = %s
                    ORDER BY subject
                """
                cur.execute(query, (semester,))
                return cur.fetchall()
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching semester scores for all students", e)
            return []

    def fetch_test_scores_for_subject(self, enrolment_id, semester, subject):
        """
        Fetch T1, T2, T3, T4 scores for a single subject in a given semester
        for the specified student.
        Returns a tuple (T1, T2, T3, T4) or None if no record is found.
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT T1, T2, T3, T4
                    FROM student_scores
                    WHERE enrolment_id = %s
                      AND semester = %s
                      AND subject ILIKE %s
                    LIMIT 1
                """
                cur.execute(query, (enrolment_id, semester, subject))
                row = cur.fetchone()
                return row  # e.g. (13.5, 15, 12.5, 11.5)
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching test scores for subject", e)
            return None

    def fetch_subjects_for_semester(self, enrolment_id, semester):
        """
        Returns a list of distinct subject names for the given student and semester.
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT DISTINCT subject
                    FROM student_scores
                    WHERE enrolment_id = %s
                      AND semester = %s
                    ORDER BY subject
                """
                cur.execute(query, (enrolment_id, semester))
                rows = cur.fetchall()  # e.g. [('JAVA-I',), ('Physics (PHY)',), ...]
                subjects = [row[0] for row in rows]  # flatten tuples
                return subjects
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching subjects for semester", e)
            return []

    def fetch_all_scores(self):
        """
        Returns a list of tuples (enrolment_id, semester, subject, total_score)
        for all students and all semesters in the student_scores table.
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT enrolment_id, semester, subject, total_score
                    FROM student_scores
                    ORDER BY subject
                """
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            from utils.error_handling import log_error
            log_error("Error fetching all scores", e)
            return []

    def fetch_all_students(self):
        """
        Returns a list of all students with columns:
        (enrolment_id, fullname, semester)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT enrolment_id, fullname, semester
                    FROM students
                    ORDER BY enrolment_id
                """)
                return cur.fetchall()
        except Exception as e:
            # Log error if necessary
            return []

    def fetch_all_student_scores(self):
        """
        Returns all student scores with columns:
        (enrolment_id, subject, T1, T2, T3, T4, total_score, semester)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT enrolment_id, subject, T1, T2, T3, T4, total_score, semester
                    FROM student_scores
                    ORDER BY semester, enrolment_id
                """)
                return cur.fetchall()
        except Exception as e:
            # Optionally log error
            return []

    def fetch_faculty_logs(self, faculty_id):
        """
        Returns a list of audit log entries for the given faculty_id.
        Each entry is a tuple:
          (log_id, faculty_id, enrolment_id, action, old_value, new_value, timestamp)
        Ordered by timestamp descending.
        """
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT log_id, faculty_id, enrolment_id, action, old_value, new_value, timestamp
                    FROM faculty_logs
                    WHERE faculty_id = %s
                    ORDER BY timestamp DESC
                """
                cur.execute(query, (faculty_id,))
                return cur.fetchall()
        except Exception as e:
            # Optionally log the error
            return []

    def update_student_test_score(self, enrolment_id, semester, subject, test_field, new_value):
        """
        Updates the test score for a given student, semester, and subject.
        Recalculates the total score (sum of T1, T2, T3, T4) after update.
        Returns a tuple (old_value, new_total) if successful, or None if failed.
        """
        try:
            with self.conn.cursor() as cur:
                # Fetch current test scores
                cur.execute("""
                    SELECT T1, T2, T3, T4 
                    FROM student_scores 
                    WHERE enrolment_id = %s AND semester = %s AND subject = %s
                """, (enrolment_id, semester, subject))
                row = cur.fetchone()
                if not row:
                    return None
                scores = list(row)  # [T1, T2, T3, T4]
                test_index = {'T1': 0, 'T2': 1, 'T3': 2, 'T4': 3}
                if test_field not in test_index:
                    return None
                old_value = scores[test_index[test_field]]

                # Update the specified test score
                cur.execute(f"""
                    UPDATE student_scores
                    SET {test_field} = %s
                    WHERE enrolment_id = %s AND semester = %s AND subject = %s
                """, (new_value, enrolment_id, semester, subject))

                # Update the total score
                scores[test_index[test_field]] = new_value
                new_total = sum(scores)
                cur.execute("""
                    UPDATE student_scores
                    SET total_score = %s
                    WHERE enrolment_id = %s AND semester = %s AND subject = %s
                """, (new_total, enrolment_id, semester, subject))
                self.conn.commit()
                return (old_value, new_total)
        except Exception as e:
            self.conn.rollback()
            return None

    def insert_faculty_log(self, faculty_id, enrolment_id, action, old_value, new_value):
        """
        Inserts a record into the faculty_logs table.
        Returns True if successful, or False if failed.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO faculty_logs (faculty_id, enrolment_id, action, old_value, new_value)
                    VALUES (%s, %s, %s, %s, %s)
                """, (faculty_id, enrolment_id, action, old_value, new_value))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            return False

    def fetch_all_student_scores(self):
        """
        Returns all student scores with columns:
        (enrolment_id, subject, T1, T2, T3, T4, total_score, semester)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT enrolment_id, subject, T1, T2, T3, T4, total_score, semester
                    FROM student_scores
                    ORDER BY semester, enrolment_id
                """)
                return cur.fetchall()
        except Exception as e:
            return []
