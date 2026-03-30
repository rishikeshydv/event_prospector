from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from event_register import event_register


def chromium_start_test():
    browser, content, page = event_register.create_page(headless=False)
    assert browser is not None
    assert content is not None
    assert page is not None
    print("Chromium started successfully.")

if __name__ == "__main__":
    chromium_start_test()