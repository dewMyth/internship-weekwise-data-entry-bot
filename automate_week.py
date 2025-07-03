# pip install playwright pandas
# playwright install


import sys
import argparse
import os
import pandas as pd
from playwright.sync_api import sync_playwright
import time
import getpass

if getattr(sys, 'frozen', False):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(
        sys._MEIPASS, "ms-playwright")

# START SCRIPT
# # # python automate_week.py --email silvaja-as20008@stu.kln.ac.lk --password 6268 --start 2025-07-07
LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"


# parser = argparse.ArgumentParser(description="Automate day record entries.")
# parser.add_argument("--email", required=True, help="Login email")
# parser.add_argument("--password", required=True, help="Login password")
# parser.add_argument("--start", required=True,
#                     help="Week start date (YYYY-MM-DD)")
# args = parser.parse_args()

print("🔐 Please enter your credentials and start date:")

EMAIL = input("Email: ").strip()
PASSWORD = getpass.getpass("Password (hidden): ").strip()
WEEK_START_DATE = input("Week start date (YYYY-MM-DD): ").strip()


# Load records
# EMAIL = args.email
# PASSWORD = args.password
# WEEK_START_DATE = args.start

# Load the matching CSV
csv_filename = f"day_records_{WEEK_START_DATE}.csv"
if not os.path.exists(csv_filename):
    raise FileNotFoundError(f"CSV file not found: {csv_filename}")

records = pd.read_csv(csv_filename)
# records = pd.read_csv("day_records_2025-07-07.csv")


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
        first_date = records.iloc[0]["date"]
        week_rows = page.query_selector_all("#weeks_table tbody tr")
        for row in week_rows:
            if row.inner_text().strip().startswith(first_date):
                row.query_selector('a[href*="week_record"]').click()
                break

        page.wait_for_load_state("networkidle")
        print("✅ Week page opened")

        # 4. Loop through each date in CSV and match corresponding row
        for _, record in records.iterrows():
            date = record["date"]
            day_rows = page.query_selector_all("#week_records_table tbody tr")
            matched = False
            for row in day_rows:
                if date in row.inner_text():
                    link = row.query_selector('a[href*="week_day_record"]')
                    if link:
                        day_url = link.get_attribute("href")
                        matched = True
                        break
            if not matched:
                print(f"❌ Could not find link for date {date}")
                continue

            print(f"➡️ Editing day record for {date}")
            page.goto(day_url)
            page.wait_for_load_state("networkidle")

            # Open modal
            page.click("#add_day_record_btn")
            try:
                page.wait_for_selector("#add_day_record_form", timeout=5000)
            except:
                print(f"❌ Modal did not open for {date}")
                continue

            # Fill dropdowns
            page.select_option("#organization_category",
                               str(record["organization_category"]))
            page.wait_for_timeout(500)
            page.select_option("#experience_category",
                               str(record["experience_category"]))
            page.wait_for_timeout(500)
            page.select_option("#sub_job_experience_category", str(
                record["sub_job_experience_category"]))
            page.wait_for_timeout(500)
            page.select_option("#student_contribution",
                               str(record["student_contribution"]))
            page.wait_for_timeout(500)

            # Fill numeric inputs
            page.fill("#computerized_work_hours", str(
                record["computerized_work_hours"]))
            page.fill("#manual_work_hours", str(record["manual_work_hours"]))

            # Fill rich text editor
            page.eval_on_selector(
                ".note-editable",
                """(el, value) => {
                    el.innerHTML = value;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }""",
                str(record["remarks"])
            )

            try:
                # Wait for confirmation modal and click "Save record"
                page.wait_for_selector(
                    ".jconfirm-buttons .btn-danger", timeout=5000)
                page.wait_for_timeout(300)
                page.click(".jconfirm-buttons .btn-danger")
                page.wait_for_selector(
                    ".jconfirm", state="hidden", timeout=5000)
                print(f"✅ Record submitted for {date}")
                # Go back to the week table page
                page.go_back()
                page.wait_for_load_state("networkidle")
            except Exception as e:
                print(f"⚠️ Submit confirmation not detected for {date}: {e}")

                # Try to recover state by navigating back to week page
                try:
                    page.go_back()
                    page.wait_for_load_state("networkidle")
                    print(
                        f"↩️ Recovered by going back after failure on {date}")
                except:
                    print("🚨 Failed to go back. Skipping to next record...")

                continue  # Safely go to next CSV row

        print("🎉 All records processed")
        browser.close()


if __name__ == "__main__":
    run()
