from __future__ import annotations

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def login(
        self,
        login_url: str,
        email: str,
        password: str,
        base_url: str = "https://app.secondnature.ai",
    ) -> None:
        if not email or not password:
            raise ValueError("SECOND_NATURE_EMAIL and SECOND_NATURE_PASSWORD are required.")

        self.page.goto(login_url or base_url)
        self.page.get_by_role("textbox", name="Email address").fill(email)
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Continue").click()

        self.expect_loaded()

    def expect_loaded(self) -> None:
        expect(self.page.get_by_test_id("createCourseButton").first).to_be_visible(timeout=60_000)
