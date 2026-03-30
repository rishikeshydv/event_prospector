from functools import lru_cache

REGISTER_BUTTON_TEXTS = ["Register", "Sign Up", "Join Now"]

class EventRegister:
    def __init__(self, event_url):
        self.event_url = event_url

    @lru_cache(maxsize=1)
    def get_playwright(self):
        from playwright.sync_api import sync_playwright
        return sync_playwright().start()


    def create_browser(self,headless: bool = True):
        return self.get_playwright().chromium.launch(headless=headless)

    def create_page(self,headless: bool = True):
        browser = self.create_browser(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        return browser, context, page

    def register(self):
        browser, context, page = self.create_page(headless=False)
        try:
            page.goto(self.event_url)
            for button_text in REGISTER_BUTTON_TEXTS:
                try:
                    page.click(f"text={button_text}")
                    print(f"Clicked on '{button_text}' button.")
                    break
                except Exception as e:
                    print(f"'{button_text}' button not found: {e}")
        finally:
            browser.close()


