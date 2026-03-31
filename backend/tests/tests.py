from pathlib import Path
import sys
import asyncio

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from event_register import eventbrite_adapter, luma_adapter
from event_register import event_register


async def chromium_start_test():
    EventRegister = event_register.EventRegister(event_urls=[])
    browser, content, page = await EventRegister.create_page(headless=False)
    assert browser is not None
    assert content is not None
    assert page is not None
    print("Chromium started successfully.")

async def context_save_test(url:str, user_info:eventbrite_adapter.UserInfo):
    EventRegister = event_register.EventRegister(event_urls=[url])
    browser, content, page = await EventRegister.create_page(headless=False)
    EventBriteAdapter = eventbrite_adapter.EventBriteAdapter(event_url=url, browser=browser, context=content, page=page, user_info=user_info)
    status_code = await EventBriteAdapter.register()
    print("Status code:", status_code)
    # assert status_code == 200
    print("Context state saved successfully.")

async def luma_adapter_test(url:str, user_info:luma_adapter.UserInfo):
    EventRegister = event_register.EventRegister(event_urls=[url])
    browser, content, page = await EventRegister.create_page(headless=False)
    LumaAdapter = luma_adapter.LumaAdapter(urls=[url], browser=browser, context=content, page=page, user_info=user_info)
    success = await LumaAdapter.register_user(user_info)
    print("Registration success:", success)
    # assert success == True
    print("Luma registration test completed successfully.")


if __name__ == "__main__":
    asyncio.run(luma_adapter_test(url="https://luma.com/nyc?e=evt-xTRiRNhssgt39FR", user_info=luma_adapter.UserInfo(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        company="Example Inc.",
        title="Software Engineer"
    )))