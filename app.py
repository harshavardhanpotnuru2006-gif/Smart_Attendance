import sys
import math
from pathlib import Path
from flask import Flask, render_template, jsonify, request, session

# Inject 'src' into path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from db import get_student_profile, save_all_student_data
from ai_service import ask_academic_assistant, load_timetable
from scraper import run_full_scrape
from parser import parse_attendance, parse_marks

app = Flask(__name__)
app.secret_key = "nsrit_smart_attendance_secret_key"

def enrich_profile_margins(profile):
    if not profile:
        return profile

    total_held = profile.get("total_held") or 0
    total_attended = profile.get("total_attended") or 0

    if total_held > 0:
        overall_pct = (total_attended / total_held) * 100
        if overall_pct >= 75:
            buffer_cls = math.floor((total_attended - 0.75 * total_held) / 0.75)
            profile["health_status"] = f"Nominal Margin: +{buffer_cls} Classes Buffer"
            profile["is_shortage"] = False
        else:
            needed_cls = math.ceil((0.75 * total_held - total_attended) / 0.25)
            profile["health_status"] = f"Attendance Shortage: Need +{needed_cls} Classes"
            profile["is_shortage"] = True
    else:
        profile["health_status"] = "No Records"
        profile["is_shortage"] = False

    subjects = profile.get("attendance_subjects") or []
    for sub in subjects:
        held = sub.get("held") or 0
        attended = sub.get("attended") or 0
        if held > 0:
            pct = (attended / held) * 100
            if pct >= 75:
                buf = math.floor((attended - 0.75 * held) / 0.75)
                sub["margin_badge"] = f"Can skip +{buf}" if buf > 0 else "Safe margin"
                sub["is_shortage"] = False
            else:
                need = math.ceil((0.75 * held - attended) / 0.25)
                sub["margin_badge"] = f"Need +{need} classes"
                sub["is_shortage"] = True
        else:
            sub["margin_badge"] = "No classes"
            sub["is_shortage"] = False

    return profile

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/student", methods=["GET"])
@app.route("/api/data", methods=["GET"])
def get_student_data():
    roll_no = request.args.get("roll_no") or session.get("roll_no")
    profile = get_student_profile(roll_no)
    if not profile:
        return jsonify({"error": "No student record cached. Please login first."}), 404
    enriched = enrich_profile_margins(profile)
    timetable = load_timetable()
    return jsonify({
        "profile": enriched,
        "timetable": timetable
    })

@app.route("/api/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        profile = run_full_scrape(username=username, password=password, headless=True)
        if profile and profile.get("roll_no"):
            session["roll_no"] = profile["roll_no"]
        enriched = enrich_profile_margins(profile)
        return jsonify({
            "message": "Authentication and scraping successful!",
            "profile": enriched
        })
    except PermissionError as e:
        return jsonify({"error": "Invalid Roll Number or Password"}), 401
    except TimeoutError as e:
        return jsonify({"error": f"Portal unreachable or slow response: {str(e)}"}), 504
    except Exception as e:
        err_msg = str(e)
        if "Authentication failed" in err_msg or "Invalid" in err_msg:
            return jsonify({"error": "Invalid Roll Number or Password"}), 401
        return jsonify({"error": f"Portal authentication failed: {err_msg}"}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    user_query = payload.get("message", "").strip()
    if not user_query:
        return jsonify({"error": "Message is empty"}), 400

    try:
        reply = ask_academic_assistant(user_query)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sync", methods=["POST"])
def sync_data():
    try:
        att = parse_attendance()
        mrk = parse_marks()
        save_all_student_data(att, mrk)
        roll_no = session.get("roll_no")
        profile = get_student_profile(roll_no)
        enriched = enrich_profile_margins(profile)
        return jsonify({
            "message": "Data synchronized successfully!",
            "profile": enriched
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
