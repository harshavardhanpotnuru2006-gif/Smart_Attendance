import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

def login(page, user=None, pwd=None, url=None):
    if not url:
        url = os.getenv("COLLEGE_URL")
    if not user:
        user = os.getenv("COLLEGE_USERNAME")
    if not pwd:
        pwd = os.getenv("COLLEGE_PASSWORD")

    if not url or not user or not pwd:
        raise ValueError("Invalid Roll Number or Password")

    alerts = []
    def handle_dialog(dialog):
        message = dialog.message
        print(f"Alert caught during login: {message}")
        alerts.append(message)
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    print(f"Navigating to: {url}")
    try:
        page.goto(url, timeout=45000, wait_until="domcontentloaded")
        page.wait_for_selector("#txtId2", timeout=15000)
        page.fill("#txtId2", user)
        page.fill("#txtPwd2", pwd)
        page.click("#imgBtn2")
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
    except Exception as nav_err:
        raise TimeoutError(f"Portal unreachable or slow response: {str(nav_err)}")

    if alerts:
        raise PermissionError(f"Invalid Roll Number or Password (Portal message: {alerts[-1]})")

    print(f"Authentication successful for user: {user}")