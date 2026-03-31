from pydantic import BaseModel
from typing import List
import re
class UserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    title: str

    #https://luma.com/60ow6yr6

class LumaAdapter:
    def __init__(self, urls: List[str], browser, context, page, user_info: UserInfo):
        self.urls = urls
        self.browser = browser
        self.context = context
        self.page = page
        self.user_info = user_info

    async def register_user(self, user_info: UserInfo) -> bool:
        if len(self.urls) == 0:
            print("No URLs available for registration.")
            return False
        for url in self.urls:
            try:
                await self.page.goto(url)
                registration_section = self.page.locator("div.jsx-fa675b9a59c2fdd9.base-11-card.rounded-card")
                register_button = registration_section.locator("button:has-text('Register'), button:has-text('Request to Join'), button:has-text('Join Waitlist'), button:has-text('Get Tickets'), button:has-text('Buy Tickets'), button:has-text('RSVP'), button:has-text('Attend Event'), button:has-text('Book Now'), button:has-text('Enroll Now')").first
                await register_button.click()
                #see what fields exist and fill it out accordingly
                left_form = self.page.locator("div.jsx-2978724248.left.flex-1")
                all_fields = left_form.locator("div.lux-input-wrapper.medium.outline")
                all_fields_count = await all_fields.count()
                if all_fields_count == 0:
                    print(f"No input fields found for registration at {url}")
                    continue
                for i in range(all_fields_count):
                    field = all_fields.nth(i)
                    label = await field.locator("label").inner_text()
                    if "name" in label.lower():
                        await field.locator("input").fill(user_info.first_name + " " + user_info.last_name)
                    if "first name" in label.lower():
                        await field.locator("input").fill(user_info.first_name)
                    elif "last name" in label.lower():
                        await field.locator("input").fill(user_info.last_name)
                    elif "email" in label.lower():
                        await field.locator("input").fill(user_info.email)
                    elif "company" in label.lower():
                        await field.locator("input").fill(user_info.company)
                    elif "title" in label.lower():
                        await field.locator("input").fill(user_info.title)

                panel = self.page.locator("div.lux-overlay.glass")
                await panel.wait_for(state="visible")

                print(await panel.get_by_role("button").all_inner_texts())

                submit_button = panel.get_by_role(
                    "button",
                    name=re.compile(r"submit|register|request|waitlist|get tickets|buy tickets|rsvp", re.I),
                ).first

                await submit_button.click()
                print(f"Successfully registered user at {url}")
                return True

            except Exception as e:
                print(f"Failed to register user at {url}: {e}")
                continue
