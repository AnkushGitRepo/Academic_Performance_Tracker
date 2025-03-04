import re

def validate_enrolment_id(enrolment_id):
    if not enrolment_id or len(enrolment_id) < 5:
        return False
    return True

def validate_score(score):
    try:
        score = int(score)
        if 0 <= score <= 100:
            return True
    except ValueError:
        pass
    return False

def get_acronym(subject: str) -> str:
    """
    Extract an acronym from the subject name.
    - If the subject contains 'JAVA-I' or 'JAVA-II', return that as the acronym.
    - Otherwise, if the subject has parentheses, extract text within them.
    - If neither applies, default to the first three uppercase letters.
    """
    upper_sub = subject.upper()
    if 'JAVA-I' in upper_sub:
        return 'JAVA-I'
    elif 'JAVA-II' in upper_sub:
        return 'JAVA-II'

    match = re.search(r'\((.*?)\)', subject)
    if match:
        return match.group(1).strip()
    else:
        return subject[:3].upper()
