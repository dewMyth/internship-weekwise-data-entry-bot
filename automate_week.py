# pip install playwright pandas
# playwright install

import pandas as pd
from playwright.sync_api import sync_playwright
import time
import argparse

# EMAIL = "silvaja-as20008@stu.kln.ac.lk"
# PASSWORD = "6268"
# LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"
# WEEK_START_DATE = "2025-07-07"


parser = argparse.ArgumentParser(description="Automate day record entries.")
parser.add_argument("--email", required=True, help="Login email")
parser.add_argument("--password", required=True, help="Login password")
parser.add_argument("--start", required=True,
                    help="Week start date (YYYY-MM-DD)")
args = parser.parse_args()

# python automate_week.py - -email silvaja-as20008@stu.kln.ac.lk - -password 6268 - -start 2025-07-07

EMAIL = args.email
PASSWORD = args.password
WEEK_START_DATE = args.start
LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"


# Load data
records = pd.read_csv("day_records.csv")


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()

        # 1. Login
        page.goto(LOGIN_URL)
        page.fill('#email', EMAIL)
        page.fill('#password', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        print("✅ Logged in")

        # 2. Go to semester week list
        page.click('a[href*="week_record?semester_id="]')
        page.wait_for_load_state("networkidle")

        # 3. Find week row with matching start date
        week_rows = page.query_selector_all("#weeks_table tbody tr")
        for row in week_rows:
            text = row.inner_text().strip()
            if text.startswith(WEEK_START_DATE):
                row.query_selector('a[href*="week_record"]').click()
                break

        page.wait_for_load_state("networkidle")
        print("✅ Week page opened")

        # 4. Get day edit links
        links = page.query_selector_all(
            '#week_records_table tbody tr a[href*="week_day_record"]')
        day_links = [a.get_attribute("href") for a in links][:5]

        # 5. Iterate over 5 days
        for i, link in enumerate(day_links):
            record = records.iloc[i]
            print(f"➡️ Editing Day {i+1}")
            page.goto(link)
            page.wait_for_load_state("networkidle")

            # Open modal
            page.click("#add_day_record_btn")
            try:
                page.wait_for_selector("#add_day_record_form", timeout=5000)
            except:
                print(f"❌ Modal did not open for Day {i+1}")
                continue

            # Fill dropdowns
            page.select_option("#organization_category",
                               str(record["organization_category"]))
            page.select_option("#experience_category",
                               str(record["experience_category"]))
            page.select_option("#sub_job_experience_category",
                               str(record["sub_job_experience_category"]))
            page.select_option("#student_contribution",
                               str(record["student_contribution"]))

            # Fill numeric inputs
            page.fill("#computerized_work_hours",
                      str(record["computerized_work_hours"]))
            page.fill("#manual_work_hours", str(record["manual_work_hours"]))

            # Fill remarks into rich text editor (.note-editable)
            page.eval_on_selector(
                ".note-editable",
                """(el, value) => {
                    el.innerHTML = value;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }""",
                str(record["remarks"])
            )

            # Submit the form (opens confirmation modal)
            # page.click("#add_day_record_form button[type='submit']")

            try:
                # Wait for confirmation modal and click "Save record"
                page.wait_for_selector(
                    ".jconfirm-buttons .btn-danger", timeout=5000)
                page.wait_for_timeout(300)  # Let modal become interactive
                page.click(".jconfirm-buttons .btn-danger")
                page.wait_for_selector(
                    ".jconfirm", state="hidden", timeout=5000)
                print(f"✅ Day {i+1} confirmed and submitted")
            except Exception as e:
                print(
                    f"⚠️ Submit confirmation not detected for Day {i+1}: {e}")
                time.sleep(1)

        print("🎉 All 5 day records submitted")
        browser.close()


if __name__ == "__main__":
    run()
