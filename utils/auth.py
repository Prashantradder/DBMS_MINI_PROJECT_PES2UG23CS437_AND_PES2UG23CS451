# utils/auth.py

from utils.db_helpers import fetch_all
from db_config import get_engine
from sqlalchemy import text


# =====================================================================
#                        STUDENT CHECKS
# =====================================================================

# Check whether SRN exists in Student table
def student_exists(srn):
    df = fetch_all(f"SELECT SRN FROM Student WHERE SRN='{srn}'")
    return not df.empty


# Check whether SRN exists in User_Login table
def account_exists(srn):
    df = fetch_all(f"SELECT SRN FROM User_Login WHERE SRN='{srn}'")
    return not df.empty


# =====================================================================
#                    STUDENT LOGIN VERIFICATION
# =====================================================================

def verify_student_login(srn, password):
    df = fetch_all(f"""
        SELECT * FROM User_Login
        WHERE SRN='{srn}' AND Password='{password}'
    """)
    return not df.empty


# =====================================================================
#                    CASE 2: CREATE LOGIN PASSWORD
# =====================================================================

def create_login_password(srn, password):
    engine = get_engine()
    sql = text("""
        INSERT INTO User_Login (SRN, Password)
        VALUES (:srn, :pwd)
    """)

    with engine.connect() as conn:
        conn.execute(sql, {"srn": srn, "pwd": password})
        conn.commit()


# =====================================================================
#                CASE 3: CREATE FULL STUDENT ACCOUNT
# =====================================================================

# Notice: No password here (as per your requirement)
def create_full_student_account(srn, name, dept, year, contact):
    engine = get_engine()

    sql = text("""
        INSERT INTO Student (SRN, Student_Name, Department, Year, Contact_Info)
        VALUES (:srn, :name, :dept, :year, :contact)
    """)

    with engine.connect() as conn:
        conn.execute(sql, {
            "srn": srn,
            "name": name,
            "dept": dept,
            "year": year,
            "contact": contact
        })
        conn.commit()


# =====================================================================
#                        ADMIN LOGIN CHECK
# =====================================================================

def verify_admin_login(admin_name, password):
    df = fetch_all(f"""
        SELECT * FROM Admin_Login
        WHERE Admin_Name='{admin_name}' AND Password='{password}'
    """)
    return not df.empty
