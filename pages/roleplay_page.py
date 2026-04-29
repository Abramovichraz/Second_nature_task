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
        self.page.get_by_test_id("task-selector-button").click()
        expect(self.page.get_by_test_id("add-roleplay-template-button")).to_be_visible(timeout=20_000)
        self.page.get_by_test_id("add-roleplay-template-button").click()
        self.page.get_by_test_id("available-templates-toggle").click()
        expect(
            self.page.get_by_test_id("featured-template-single-persona-role-play-[ai-assistant]")
        ).to_be_visible(timeout=20_000)
        self.page.get_by_test_id("featured-template-single-persona-role-play-[ai-assistant]").click()

    def expect_template_ready_for_ai_creation(self) -> None:
        expect(self.page.get_by_test_id("co-create-with-ai-button")).to_be_visible(timeout=20_000)

    def start_ai_co_create(self) -> None:
        self.page.get_by_test_id("co-create-with-ai-button").click()
        self.page.get_by_test_id("confirm-generate-roleplay-button").click()

    def send_co_create_messages(self, messages: list[str]) -> None:
        input_box = self.page.get_by_test_id("co-create-chat-input")
        send_button = self.page.get_by_test_id("co-create-chat-send")
        thinking_status = self.page.get_by_text("Client is thinking")
        retry_error = self.page.get_by_text(AI_RETRY_ERROR)

        for message in messages:
            error_count = 0

            while True:
                expect(input_box).to_be_visible(timeout=120_000)
                expect(thinking_status).not_to_be_visible(timeout=180_000)

                previous_retry_errors = retry_error.count()
                input_box.click()
                input_box.fill("")
                input_box.type(message, delay=5)
                expect(send_button).to_be_enabled(timeout=60_000)
                send_button.click()

                self.page.wait_for_timeout(500)
                if thinking_status.is_visible(timeout=10_000):
                    expect(thinking_status).not_to_be_visible(timeout=180_000)

                if retry_error.count() <= previous_retry_errors:
                    break

                error_count += 1
                if error_count > 2:
                    raise AssertionError(
                        f'AI co-create returned "{AI_RETRY_ERROR}" more than 2 times for message: {message}'
                    )

    def set_persona_background(self, background: str) -> None:
        background_box = self.page.get_by_role("textbox", name="The Persona's Background")
        if not background_box.is_visible(timeout=5_000):
            return

        background_box.fill(background)
        self.page.get_by_role("button", name="Save").click()

    def select_custom_persona(self, persona_name: str) -> None:
        self.page.get_by_test_id("persona-setup-edit-button").click()
        self.page.get_by_text("Custom Personas", exact=True).click()
        self.page.get_by_test_id(f"persona-card-{persona_name}").click()
        self.page.get_by_test_id("persona-setup-done-btn").click(force=True)

    def set_ai_persona_opener(self, opener_text: str) -> None:
        prospect_opener = self.page.locator("#prospect-opener")
        prospect_opener.scroll_into_view_if_needed()

        opener_candidates = [
            self.page.locator("#ProspectOpener"),
            prospect_opener.locator("textarea, input").first,
            prospect_opener.locator("[contenteditable=true]").first,
        ]
        edit_buttons = [
            prospect_opener.get_by_role("button", name="Edit"),
            prospect_opener.get_by_text("Edit", exact=True),
            self.page.locator("#ai-trainer-opener").get_by_role("button", name="Edit"),
            self.page.locator("#ai-trainer-opener").get_by_text("Edit", exact=True),
        ]

        opener = None
        for attempt in range(3):
            for candidate in opener_candidates:
                if candidate.count() and candidate.first.is_visible(timeout=2_000):
                    opener = candidate.first
                    break
            if opener:
                break

            for edit_button in edit_buttons:
                if edit_button.count() and edit_button.first.is_visible(timeout=2_000):
                    edit_button.first.click(force=True)
                    self.page.wait_for_timeout(1_000)
                    break

            if attempt == 1:
                prospect_opener.click(force=True)

        if opener is None:
            opener = prospect_opener.locator("textarea, input, [contenteditable=true]").first
        expect(opener).to_be_visible(timeout=20_000)
        opener.fill(opener_text)
        prospect_opener.get_by_role("button", name="Done").click(force=True)
