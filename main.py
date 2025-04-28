import os
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from utils import human_type
from utils import random_delay

load_dotenv()


def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-infobars',
                '--disable-extensions',
                '--start-maximized',
                '--window-size=1280,720',
            ]
        )
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'
        context = browser.new_context(
            user_agent=user_agent
        )
        page = context.new_page()

        try:
            page.goto("https://accounts.google.com/signin")

            # Fill email
            email_input = page.wait_for_selector('input[type="email"]', state='visible', timeout=30000)
            human_type(email_input, os.getenv("GOOGLE_EMAIL"))
            page.get_by_role("button", name="Next").click()
            random_delay(5, 7)

            # Fill password
            password_input = page.wait_for_selector('input[type="password"]', state='visible', timeout=30000)
            human_type(password_input, os.getenv("GOOGLE_PASSWORD"))
            page.get_by_role("button", name="Next").click()
            time.sleep(60)

            # Save session state
            context.storage_state(path="auth.json")
            print("Login successful, session saved.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


def test():
    name = "name"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        page.goto("https://studio.youtube.com/")
        page.get_by_role("button", name="Content").click()

        page.get_by_role("button", name=name).click()
        page.get_by_role("radio", name="No, it's not made for kids").click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_label("Next", exact=True).click()
        page.get_by_role("radio", name="Unlisted").click()
        page.get_by_label("Save", exact=True).click()
        page.locator("ytcp-video-share-dialog #close-button").get_by_role("button", name="Close").click()
        page.goto("https://studio.youtube.com/")
        page.get_by_role("button", name="Content").click()
        time.sleep(60)

        context.close()
        browser.close()
