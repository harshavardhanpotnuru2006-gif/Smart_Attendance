def scrape_attendance(page, data_dir):
    print("Clicking ATTENDANCE menu...")
    
    # Check if alert/dialog appears (invalid credentials or session notice)
    page.on("dialog", lambda dialog: dialog.accept())

    # Check if login actually succeeded
    if "Default.aspx" in page.url and page.locator("#lblMsg").is_visible():
        err_msg = page.locator("#lblMsg").inner_text()
        raise Exception(f"Portal login rejected: {err_msg}")

    # Resilient click with fallback
    try:
        # Try direct click with shorter timeout
        page.locator("a:has-text('Attendance'), a:has-text('ATTENDANCE'), text='ATTENDANCE'").first.click(timeout=8000)
    except Exception:
        # Fallback: Navigate directly to attendance page URL if portal allows,
        # or click via JavaScript evaluation
        page.evaluate("() => { const el = Array.from(document.querySelectorAll('a')).find(a => a.textContent.includes('Attendance') || a.textContent.includes('ATTENDANCE')); if (el) el.click(); }")

    page.wait_for_timeout(2500)

    # Handle iframe or direct page table navigation
    if page.locator("#capIframeId").count() > 0:
        frame = page.frame_locator("#capIframeId")
        print("Selecting 'Till now' radio button...")
        try:
            radio = frame.locator("input[type='radio']").nth(2)
            radio.check(force=True)
            radio.dispatch_event("click")
            page.wait_for_timeout(1500)
        except Exception:
            pass

        print("Clicking 'Show..' button...")
        try:
            frame.locator("input[value*='Show'], input[type='submit'][value*='Show']").first.click(timeout=8000)
        except Exception:
            pass

        try:
            frame.locator("text=ATTENDANCE REPORT, table").wait_for(timeout=15000)
        except Exception:
            page.wait_for_selector("table", timeout=15000)
        page.wait_for_timeout(1500)

        page.screenshot(path=str(data_dir / "attendance_table.png"))
        html = page.evaluate("() => document.getElementById('capIframeId') ? document.getElementById('capIframeId').contentDocument.body.innerHTML : document.body.innerHTML")
    else:
        # Wait for attendance table container to be visible
        page.wait_for_selector("table", timeout=15000)
        page.screenshot(path=str(data_dir / "attendance_table.png"))
        html = page.content()

    with open(data_dir / "attendance_table.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Attendance saved successfully!")