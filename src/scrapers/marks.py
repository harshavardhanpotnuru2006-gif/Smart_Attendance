def scrape_marks(page, data_dir):
    print("Scraping Marks...")
    page.locator("text=MARKS").first.click()
    page.wait_for_timeout(3000)

    page.screenshot(path=str(data_dir / "marks_table.png"))
    html = page.evaluate("() => document.getElementById('capIframeId').contentDocument.body.innerHTML")
    with open(data_dir / "marks_table.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Marks saved successfully!")