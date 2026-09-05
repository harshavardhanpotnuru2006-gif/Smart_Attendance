import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Add 'src' directory to Python system path
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from db import get_student_profile

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=api_key)

COURSE_MAPPING = {
    "23CS403": "Operating Systems (OS)",
    "23CS601": "Computer Networks (CN)",
    "23AI403": "Machine Learning (ML)",
    "23CS304": "Software Engineering (SE)",
    "23DS503": "Mathematical Modeling / MST",
    "23AI406": "Machine Learning Lab (ML LAB)",
    "23CS608": "Computer Networks Lab (CN LAB)",
    "23DS509": "Technical Lab (T LAB)",
    "OE1": "Open Elective - 1 (OE1)",
    "MENTORING": "Mentoring & Counseling",
    "SS": "Soft Skills",
    "QA": "Quantitative Aptitude"
}

def resolve_timetable_subjects(timetable):
    if not timetable or "schedule" not in timetable:
        return timetable

    resolved_schedule = {}
    for day, periods in timetable["schedule"].items():
        if isinstance(periods, list):
            resolved_periods = []
            for p in periods:
                code = p.get("code") or p.get("subject")
                subj_raw = p.get("subject", "")
                subject_name = COURSE_MAPPING.get(code) or COURSE_MAPPING.get(subj_raw) or subj_raw
                resolved_periods.append({
                    "period": p.get("period"),
                    "time": p.get("time"),
                    "subject": subject_name,
                    "code": code
                })
            resolved_schedule[day] = resolved_periods
        else:
            resolved_schedule[day] = periods

    res = dict(timetable)
    res["schedule"] = resolved_schedule
    return res

def load_timetable():
    timetable_file = BASE_DIR / "data" / "timetable.json"
    if timetable_file.exists():
        with open(timetable_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return resolve_timetable_subjects(raw_data)
    return {}

def ask_academic_assistant(user_query: str) -> str:
    # 1. Fetch current student record from SQLite
    student_data = get_student_profile()
    if not student_data:
        return "Student data SQLite DB lo dorakaledu. Mundhu scraper run cheyyi."

    # 2. Fetch timetable
    timetable = load_timetable()

    # 3. Formulate System Prompt with Live Context
    system_instruction = f"""
You are an intelligent, authentic academic advisor and assistant for college student {student_data['student_name']} ({student_data['roll_no']}), Branch: {student_data['branch']}, Semester: {student_data['semester']}.

STUDENT LIVE ACADEMIC RECORD:
- Overall Attendance: {student_data['overall_attendance']}
- Total Classes Conducted (Held): {student_data['total_held']}
- Total Classes Attended: {student_data['total_attended']}
- Subject-wise Attendance: {json.dumps(student_data['attendance_subjects'], indent=2)}
- Overall CGPA: {student_data['cgpa']}
- Total Credits: {student_data['credits']}
- Marks Percentage: {student_data['marks_percentage']}
- Semester SGPA Breakdown: {json.dumps(student_data['semesters_sgpa'], indent=2)}

COURSE CODE TO SUBJECT NAME MAPPING:
{json.dumps(COURSE_MAPPING, indent=2)}

TIMETABLE SCHEDULE MATRIX:
{json.dumps(timetable, indent=2)}

TIMETABLE & SCHEDULE FORMATTING RULES:
1. Whenever the user asks for any timetable (daily, weekly, or specific day like Monday):
   - NEVER output plain text lists, bullet points, or unformatted text for timetable schedules.
   - ALWAYS output an ultra-clean Markdown Table with these exact column headers:
     | Period | Time | Subject / Lab | Code | Room |
     | :---: | :---: | :--- | :---: | :---: |
   - Use the human-readable subject name (e.g. "Operating Systems (OS)") in the "Subject / Lab" column, and the course code (e.g. "23CS403") in the "Code" column. NEVER duplicate the subject code in the "Subject / Lab" column.
   - Use the room number "{timetable.get('room_no', '402 (Block III)')}" for the Room column.
   - If the user asks for a specific day (e.g. "Monday timetable" or "Today's schedule"), output only that day's clean Markdown table.
   - If the user asks for a full weekly schedule, render markdown tables for each active day or a combined matrix.

CALCULATION RULES:
1. When simulating leaves for a day (e.g., Monday, Tuesday):
   - Check the timetable for that specific day and count the periods and their subjects.
   - If leave is taken: New Held = Current Held + day's total periods; New Attended = Current Attended (since student is absent).
   - Calculate new overall attendance: (New Attended / New Held) * 100.
   - For every subject held on that day, recalculate subject percentage: current_attended / (current_held + periods_missed) * 100.
   - If any subject or overall attendance falls below 75%, clearly highlight it as a WARNING.
2. If the user asks in Tinglish/Telugu, reply naturally in Tinglish with technical words in English.
3. Be precise with numbers and percentages.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.2
        }
    )
    return response.text

if __name__ == "__main__":
    test_query = "Nenu Monday roju holiday theesukovalani anukuntunna. Na attendance meedha impact entha untundi? Direct calculations tho cheppu."
    print("User Query:", test_query)
    print("\nAI Response:\n")
    print(ask_academic_assistant(test_query))