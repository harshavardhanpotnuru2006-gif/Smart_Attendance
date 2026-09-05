import sys
from pathlib import Path

# Add 'src' directory to Python system path
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from playwright.sync_api import sync_playwright
from auth import login
from scrapers.attendance import scrape_attendance
from scrapers.marks import scrape_marks
from parser import parse_attendance, parse_marks
from db import save_all_student_data, get_student_profile

def run_full_scrape(username=None, password=None, headless=True):
    data_dir = src_dir.parent / "data"
    data_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            # 1. Login with dynamic or env credentials
            login(page, user=username, pwd=password)

            # 2. Run modular scrapers
            scrape_attendance(page, data_dir)
            scrape_marks(page, data_dir)
        finally:
            browser.close()

    # 3. Parse and cache into SQLite
    att = parse_attendance()
    mrk = parse_marks()
    save_all_student_data(att, mrk)

    target_roll = att.get("roll_no") or username
    return get_student_profile(target_roll)

if __name__ == "__main__":
    print("Running scraper manually...")
    profile = run_full_scrape(headless=False)
    print(f"Scraped & Cached successfully for: {profile['student_name']} ({profile['roll_no']})")