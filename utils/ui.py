from __future__ import annotations

from playwright.sync_api import Error, Page, expect


def dismiss_open_popovers(page: Page) -> None:
    page.keyboard.press("Escape")
    backdrop = page.locator(".sn-popover-content-backdrop.block-clicks")
    if backdrop.is_visible(timeout=2_000):
        backdrop.click(position={"x": 5, "y": 5}, force=True)


def fill_stable_test_id(page: Page, test_id: str, value: str) -> None:
    locator = page.get_by_test_id(test_id)
    last_error: Error | None = None

    for _ in range(3):
        try:
            expect(locator).to_be_visible(timeout=20_000)
            locator.fill(value)
            return
        except Error as error:
            last_error = error
            page.wait_for_timeout(1_000)

    if last_error:
        raise last_error
