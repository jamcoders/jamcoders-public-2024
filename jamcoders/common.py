class EVENT:
    STUDENT_EMAIL_ADDRESS = "student_email_address"
    STUDENT_NAME = "student_name"
    NOTEBOOK_ID = "notebook_id"
    CELL_ID = "cell_id"
    ASSERTION_RESULT = "assertion_result"

class CELL_STATUS:
    PASS = "PASS"       # All recent assertions in this cell have passed.
    FAIL = "FAIL"       # All recent assertions in this cell have failed.
    MIXED = "MIXED"     # Some recent assertions in this cell have passed and some have failed.
    NOT_ATTEMPTED = "NOT_ATTEMPTED"     # There are no assertions in this cell.