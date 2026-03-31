from functools import lru_cache
from typing import List

REGISTER_BUTTON_TEXTS = ["Register", "Register Now", "Sign Up", "Join Now", "Get Tickets", "Buy Tickets", "RSVP", "Attend Event", "Book Now", "Enroll Now"]

class EventRegister:
    def __init__(self, event_urls:List[str]):
        self.event_urls = event_urls
        self._playwright = None

    @lru_cache(maxsize=1)
    async def get_playwright(self):
        if self._playwright is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
        return self._playwright

    async def create_browser(self, headless: bool = True):
        playwright = await self.get_playwright()
        return await playwright.chromium.launch(headless=headless)

    async def create_page(self,headless: bool = True):
        browser = await self.create_browser(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        return browser, context, page

    async def register(self):
        browser, context, page = await self.create_page(headless=False)

        if len(self.event_urls) == 0:
            print("No event URLs provided.")
            return

        try:
            for event_url in self.event_urls:
                await page.goto(event_url)

                for button_text in REGISTER_BUTTON_TEXTS:
                    try:
                        all_buttons = await page.query_selector_all(f"text={button_text}")
                        if not all_buttons:
                            raise Exception(f"No buttons found with text '{button_text}'")

                        await all_buttons[0].click()
                        print(f"Clicked on '{button_text}' button.")
                        break

                    except Exception as e:
                        print(f"'{button_text}' button not found: {e}")

        finally:
            await context.close()
            await browser.close()


