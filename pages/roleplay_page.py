from __future__ import annotations

from playwright.sync_api import Page, expect

from utils.ui import dismiss_open_popovers


AI_RETRY_ERROR = "Oops! Something went wrong, could you try entering your message again?"


def chat_input(page: Page):
    return page.get_by_test_id("roleplay-chat-input")


def send_button(page: Page):
    return page.get_by_test_id("roleplay-chat-send")


def send_message_with_retry(page: Page, message: str, max_retries: int = 2) -> None:
    input_box = chat_input(page)
    submit = send_button(page)
    retry_error = page.get_by_text(AI_RETRY_ERROR)

    expect(input_box).to_be_visible(timeout=30_000)
    expect(submit).to_be_visible(timeout=30_000)

    seen_errors = retry_error.count()
    for attempt in range(max_retries + 1):
        input_box.fill(message)
        before_response = page.locator("body").inner_text(timeout=5_000)
        submit.click()

        page.wait_for_function(
            """({beforeResponse, errorText, seenErrors}) => {
                const body = document.body?.innerText || "";
                const errorCount = body.split(errorText).length - 1;
                return errorCount > seenErrors || body !== beforeResponse;
            }""",
            {
                "beforeResponse": before_response,
                "errorText": AI_RETRY_ERROR,
                "seenErrors": seen_errors,
            },
            timeout=45_000,
        )

        if retry_error.count() > seen_errors:
            seen_errors = retry_error.count()
            if attempt >= max_retries:
                raise AssertionError(
                    f'Known AI error appeared more than {max_retries} times: "{AI_RETRY_ERROR}"'
                )
            continue

        return


class RoleplayPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def add_ai_assistant_roleplay_template(self) -> None:
        dismiss_open_popovers(self.page)
        self.page.get_by_test_id("task-selector-button").click(force=True)
        expect(self.page.get_by_test_id("add-roleplay-template-button")).to_be_visible(timeout=20_000)
        self.page.get_by_test_id("add-roleplay-template-button").click()
        self.page.get_by_test_id("available-templates-toggle").click()
        expect(
            self.page.get_by_test_id("featured-template-single-persona-role-play-[ai-assistant]")
        ).to_be_visible(timeout=20_000)
        self.page.get_by_test_id("featured-template-single-persona-role-play-[ai-assistant]").click()

    def expect_template_ready_for_ai_creation(self) -> None:
        expect(self.page.get_by_test_id("co-create-with-ai-button")).to_be_visible(timeout=20_000)
