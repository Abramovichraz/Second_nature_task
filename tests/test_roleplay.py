from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.roleplay_page import AI_RETRY_ERROR, chat_input, send_button, send_message_with_retry


@pytest.mark.smoke
def test_roleplay_screen_opens_and_accepts_one_message(page, settings) -> None:
    if not settings.roleplay_test_url:
        pytest.skip("Set SECOND_NATURE_ROLEPLAY_URL to run the role-play smoke test.")

    HomePage(page).login(
        settings.login_url,
        settings.email,
        settings.password,
        settings.base_url,
    )
    page.goto(settings.roleplay_test_url)

    expect(chat_input(page)).to_be_visible(timeout=30_000)
    expect(send_button(page)).to_be_visible(timeout=30_000)

    send_message_with_retry(page, "Hello", max_retries=2)

    assert page.get_by_text(AI_RETRY_ERROR).count() <= 2
