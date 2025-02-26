import bcrypt
from database.db_operations import DBOperations
from utils.error_handling import log_error

def faculty_login(faculty_id, password):
    db = DBOperations()
    try:
        with db.conn.cursor() as cur:
            cur.execute("SELECT password FROM faculty WHERE faculty_id = %s", (faculty_id,))
            result = cur.fetchone()
            if result and bcrypt.checkpw(password.encode(), result[0].encode()):
                return True
            else:
                return False
    except Exception as e:
        log_error("Faculty login error", e)
        return False
