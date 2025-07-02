# pip install playwright
# playwright install

import argparse
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

# START SCRIPT
# # # python add_week.py --email silvaja-as20008@stu.kln.ac.lk --password 6268 --start 2025-07-14


def run(email, password, week_start_str):
    # Calculate week end (start + 4 days)
    week_end = datetime.strptime(
        week_start_str, "%Y-%m-%d") + timedelta(days=4)
    week_start_formatted = week_start_str  # Keep as YYYY-MM-DD
    week_end_formatted = week_end.strftime("%Y-%m-%d")

    LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()

        # 1. Login
        page.goto(LOGIN_URL)
        page.fill('#email', email)
        page.fill('#password', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        print("✅ Logged in")

        # 2. Click semester link (go to week view)
        page.wait_for_selector(
            'a[href*="week_record?semester_id="]', timeout=5000)
        page.click('a[href*="week_record?semester_id="]')
        page.wait_for_load_state("networkidle")
        print("✅ Semester page opened")

        # 3. Click "ADD WEEK" button
        page.wait_for_selector("#create_week", timeout=5000)
        page.evaluate("document.querySelector('#create_week').click()")
        print("🟡 Clicked ADD WEEK")

        # 4. Wait for modal to open
        page.wait_for_selector(".jconfirm.jconfirm-open", timeout=5000)
        print("✅ Modal opened")

        # 5. Clear and fill date fields in YYYY-MM-DD format
        page.evaluate("""
            () => {
                document.querySelector('#week_start_date').value = '';
                document.querySelector('#week_end_date').value = '';
            }
        """)
        page.fill("#week_start_date", week_start_formatted)
        page.fill("#week_end_date", week_end_formatted)
        print(f"✅ Dates filled: {week_start_formatted} → {week_end_formatted}")

        # 6. Click "Create Week" button in modal
        page.click(".jconfirm.jconfirm-open .jconfirm-buttons .btn-danger")
        print("✅ Clicked Create Week")

        # 7. Wait for modal to close
        page.wait_for_selector(".jconfirm.jconfirm-open",
                               state="hidden", timeout=5000)
        print("✅ Modal closed")

        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add a new week via automation.")
    parser.add_argument("--email", required=True, help="Login email")
    parser.add_argument("--password", required=True, help="Login password")
    parser.add_argument("--start", required=True,
                        help="Week start date (YYYY-MM-DD)")

    args = parser.parse_args()
    run(args.email, args.password, args.start)
