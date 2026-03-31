# eventbrite pageflow
# url -> get_tickets -> enter promo code (if any) -> select ticket quantity -> checkout ->
# first name, last name, email, confirm email, cell phone
# click on credit number, enter card details, click Place Order

import httpx
from pydantic import BaseModel
from typing import Any
import time

class UserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    confirm_email: str
    cell_phone: str
    ticket_quantity: int
    promo_code: str = None

class PaymentContextPayload(BaseModel):
    context_state: dict[str, Any]
    user_info: UserInfo
    event_url: str


class EventBriteAdapter:
    def __init__(self, event_url,browser, context, page, user_info:UserInfo):
        self.event_url = event_url
        self.user_info = user_info
        self.browser = browser
        self.context = context
        self.page = page

    async def register(self):
        await self.page.goto(self.event_url)

        register_button = self.page.locator(
            'button:has-text("Get Tickets"), '
            'button:has-text("Reserve a spot"), '
            'button:has-text("Register"), '
            'button:has-text("Register Now"), '
            'button:has-text("Sign Up"), '
            'button:has-text("Join Now"), '
            'button:has-text("Buy Tickets"), '
            'button:has-text("RSVP"), '
            'button:has-text("Attend Event"), '
            'button:has-text("Book Now"), '
            'button:has-text("Enroll Now")'
        ).first

        await register_button.click()

        iframe_locator = self.page.locator("iframe").last
        await iframe_locator.wait_for(state="attached")
        checkout_frame = iframe_locator.content_frame

        if self.user_info.promo_code:
            await checkout_frame.locator('#promo-code-field').fill(self.user_info.promo_code)

        if self.user_info.ticket_quantity > 1:
            stepper_button = checkout_frame.locator(".eds-stepper-button").first
            for _ in range(self.user_info.ticket_quantity - 1):
                await stepper_button.click()
        if not await checkout_frame.locator('button:has-text("Check out"), button:has-text("Register")').count():
            print("Checkout button not found, waiting for it to appear...")
            await checkout_frame.locator('button:has-text("Check out"), button:has-text("Register")').wait_for(state="visible")
            print("Checkout button is now visible.")
        checkout_button = checkout_frame.locator(
            'button:has-text("Check out"), button:has-text("Register")'
        ).first

        await checkout_button.click()

        # Re-resolve iframe after the click in case the checkout UI swaps/reloads frames
        iframe_after = self.page.locator("iframe").last
        await iframe_after.wait_for(state="attached")
        new_frame = iframe_after.content_frame

        # check if id="buyer.N-first_name" exists else checkout button click again to trigger the frame reload and form to appear
        if not await new_frame.locator('[id="buyer.N-first_name"]').count():
            print("First name field not found, clicking checkout button again to trigger frame reload")
            await checkout_button.click()
            # wait for the first name field to appear after the second click
            await new_frame.locator('[id="buyer.N-first_name"]').wait_for(state="visible")
        await new_frame.locator('[id="buyer.N-first_name"]').fill(self.user_info.first_name)
        await new_frame.locator('[id="buyer.N-last_name"]').fill(self.user_info.last_name)
        await new_frame.locator('[id="buyer.N-email"]').fill(self.user_info.email)
        await new_frame.locator('[id="buyer.confirmEmailAddress"]').fill(self.user_info.confirm_email)
        await new_frame.locator('[id="buyer.N-cell_phone"]').fill(self.user_info.cell_phone)
        #store browser context state and send to frontend for card details input
        context_state = await self.context.storage_state()
        payload = PaymentContextPayload(
            context_state=context_state,
            user_info=self.user_info,
            event_url=self.event_url
        )
        #send context to redis pubsub channel for frontend to pick up and use for card details input
        async with httpx.AsyncClient() as client:
            res = await client.post("http://localhost:8000/api/v1/payment_context", json=payload.model_dump())
            res.raise_for_status()
            return res.status_code
