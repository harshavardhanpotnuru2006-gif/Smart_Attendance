import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "student_cache.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_records (
            roll_no TEXT PRIMARY KEY,
            student_name TEXT,
            branch TEXT,
            semester TEXT,
            overall_attendance TEXT,
            total_held INTEGER,
            total_attended INTEGER,
            subject_wise_json TEXT,
            cgpa REAL,
            credits_earned TEXT,
            overall_marks_percentage TEXT,
            semester_sgpa_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_all_student_data(attendance_data, marks_data):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO student_records 
        (roll_no, student_name, branch, semester, overall_attendance, total_held, total_attended, 
         subject_wise_json, cgpa, credits_earned, overall_marks_percentage, semester_sgpa_json, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        attendance_data.get("roll_no"),
        attendance_data.get("student_name"),
        attendance_data.get("branch"),
        attendance_data.get("semester"),
        attendance_data.get("overall_attendance"),
        attendance_data.get("total_held"),
        attendance_data.get("total_attended"),
        json.dumps(attendance_data.get("subjects", [])),
        marks_data.get("cgpa"),
        marks_data.get("credits"),
        marks_data.get("marks_percentage"),
        json.dumps(marks_data.get("semesters", {}))
    ))
    conn.commit()
    conn.close()

def get_student_profile(roll_no=None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if roll_no:
        cursor.execute("""
            SELECT roll_no, student_name, branch, semester, overall_attendance, 
                   total_held, total_attended, subject_wise_json, cgpa, credits_earned, 
                   overall_marks_percentage, semester_sgpa_json, updated_at 
            FROM student_records 
            WHERE LOWER(roll_no) = LOWER(?)
            ORDER BY updated_at DESC LIMIT 1
        """, (roll_no.strip(),))
    else:
        cursor.execute("""
            SELECT roll_no, student_name, branch, semester, overall_attendance, 
                   total_held, total_attended, subject_wise_json, cgpa, credits_earned, 
                   overall_marks_percentage, semester_sgpa_json, updated_at 
            FROM student_records 
            ORDER BY updated_at DESC LIMIT 1
        """)
        
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "roll_no": row[0],
        "student_name": row[1],
        "branch": row[2],
        "semester": row[3],
        "overall_attendance": row[4],
        "total_held": row[5],
        "total_attended": row[6],
        "attendance_subjects": json.loads(row[7]),
        "cgpa": row[8],
        "credits": row[9],
        "marks_percentage": row[10],
        "semesters_sgpa": json.loads(row[11]),
        "updated_at": row[12]
    }