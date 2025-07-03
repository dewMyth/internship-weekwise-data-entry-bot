# # pip install playwright
# # playwright install

# import argparse
# from playwright.sync_api import sync_playwright
# from datetime import datetime, timedelta
# import getpass


# # START SCRIPT
# # # # python add_week.py --email silvaja-as20008@stu.kln.ac.lk --password 6268 --start 2025-07-14


# print("🔐 Please enter your credentials and start date:")

# EMAIL = input("Email: ").strip()
# PASSWORD = getpass.getpass("Password (hidden): ").strip()


# def run(email, password, week_start_str):
#     # Calculate week end (start + 4 days)
#     week_end = datetime.strptime(
#         week_start_str, "%Y-%m-%d") + timedelta(days=4)
#     week_start_formatted = week_start_str  # Keep as YYYY-MM-DD
#     week_end_formatted = week_end.strftime("%Y-%m-%d")

#     LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=50)
#         context = browser.new_context()
#         page = context.new_page()

#         # 1. Login
#         page.goto(LOGIN_URL)
#         page.fill('#email', email)
#         page.fill('#password', password)
#         page.click('button[type="submit"]')
#         page.wait_for_load_state("networkidle")
#         print("✅ Logged in")

#         # 2. Click semester link (go to week view)
#         page.wait_for_selector(
#             'a[href*="week_record?semester_id="]', timeout=5000)
#         page.click('a[href*="week_record?semester_id="]')
#         page.wait_for_load_state("networkidle")
#         print("✅ Semester page opened")

#         # 3. Click "ADD WEEK" button
#         page.wait_for_selector("#create_week", timeout=5000)
#         page.evaluate("document.querySelector('#create_week').click()")
#         print("🟡 Clicked ADD WEEK")

#         # 4. Wait for modal to open
#         page.wait_for_selector(".jconfirm.jconfirm-open", timeout=5000)
#         print("✅ Modal opened")

#         # 5. Clear and fill date fields in YYYY-MM-DD format
#         page.evaluate("""
#             () => {
#                 document.querySelector('#week_start_date').value = '';
#                 document.querySelector('#week_end_date').value = '';
#             }
#         """)
#         page.fill("#week_start_date", week_start_formatted)
#         page.fill("#week_end_date", week_end_formatted)
#         print(f"✅ Dates filled: {week_start_formatted} → {week_end_formatted}")

#         # 6. Click "Create Week" button in modal
#         page.click(".jconfirm.jconfirm-open .jconfirm-buttons .btn-danger")
#         print("✅ Clicked Create Week")

#         # 7. Wait for modal to close
#         page.wait_for_selector(".jconfirm.jconfirm-open",
#                                state="hidden", timeout=5000)
#         print("✅ Modal closed")

#         browser.close()


# def get_mondays(start_date, end_date):
#     start = datetime.strptime(start_date, "%Y-%m-%d")
#     end = datetime.strptime(end_date, "%Y-%m-%d")

#     # Make sure the start date is a Monday
#     if start.weekday() != 0:
#         start += timedelta(days=(7 - start.weekday()))

#     mondays = []
#     while start <= end:
#         mondays.append(start.strftime("%Y-%m-%d"))
#         start += timedelta(weeks=1)

#     return mondays


# if __name__ == "__main__":
#     monday_list = get_mondays("2025-02-17", "2025-07-19")
#     for monday in monday_list:
#         run(EMAIL, PASSWORD, monday)


from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import getpass


print("🔐 Please enter your credentials and start date:")
EMAIL = input("Email: ").strip()
PASSWORD = getpass.getpass("Password (hidden): ").strip()

LOGIN_URL = "https://dis.fcms.kln.ac.lk/department_of_accountancy/login"


def get_mondays(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start.weekday() != 0:
        start += timedelta(days=(7 - start.weekday()))

    mondays = []
    while start <= end:
        mondays.append(start.strftime("%Y-%m-%d"))
        start += timedelta(weeks=1)

    return mondays


def create_week(page, week_start_str):
    week_end = datetime.strptime(
        week_start_str, "%Y-%m-%d") + timedelta(days=4)
    week_end_str = week_end.strftime("%Y-%m-%d")

    # Click "ADD WEEK"
    page.wait_for_selector("#create_week", timeout=5000)
    page.evaluate("document.querySelector('#create_week').click()")
    print(f"🟡 Creating week: {week_start_str} → {week_end_str}")

    # Wait for modal
    page.wait_for_selector(".jconfirm.jconfirm-open", timeout=5000)

    # Fill dates
    page.evaluate("""
        () => {
            document.querySelector('#week_start_date').value = '';
            document.querySelector('#week_end_date').value = '';
        }
    """)
    page.fill("#week_start_date", week_start_str)
    page.fill("#week_end_date", week_end_str)

    # Submit
    page.click(".jconfirm.jconfirm-open .jconfirm-buttons .btn-danger")
    print("✅ Submitted week")

    # Wait for modal to close
    page.wait_for_selector(".jconfirm.jconfirm-open",
                           state="hidden", timeout=5000)
    print("✅ Modal closed")

    # Go back
    page.go_back()
    page.wait_for_load_state("networkidle")
    print("🔙 Went back to week list\n")


if __name__ == "__main__":
    mondays = get_mondays("2025-02-17", "2025-07-19")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto(LOGIN_URL)
        page.fill('#email', EMAIL)
        page.fill('#password', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        print("✅ Logged in")

        # Go to week records page
        page.wait_for_selector(
            'a[href*="week_record?semester_id="]', timeout=5000)
        page.click('a[href*="week_record?semester_id="]')
        page.wait_for_load_state("networkidle")
        print("✅ Navigated to week record page")

        # Loop through all Mondays
        for monday in mondays:
            create_week(page, monday)

        browser.close()
