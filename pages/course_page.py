from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect

from utils.ui import dismiss_open_popovers


class CoursePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_new_course_form(self) -> None:
        self.page.get_by_test_id("createCourseButton").first.click()
        expect(self.page.get_by_test_id("title")).to_be_visible(timeout=20_000)

    def set_course_title(self, title: str) -> None:
        self.page.get_by_test_id("title").fill(title)

    def course_title_value(self) -> str:
        return self.page.get_by_test_id("title").input_value()

    def try_continue_from_course_layout(self) -> None:
        self.page.get_by_test_id("next-step-button").click()

    def create_course_shell(self, title: str) -> None:
        self.open_new_course_form()
        self.set_course_title(title)
        self.try_continue_from_course_layout()

    def save_course(self) -> None:
        self.page.get_by_test_id("save-course").click()
        success = self.page.get_by_label("Success")
        expect(success).to_be_visible(timeout=60_000)
        success.get_by_role("button", name="Close").click()

    def approve_and_continue(self) -> None:
        self.page.get_by_test_id("approve-and-continue-button").click()
        confirm = self.page.get_by_test_id("confirm-approve-and-continue-button")
        if confirm.is_visible(timeout=5_000):
            confirm.click()

    def set_task_name(self, task_name: str) -> None:
        self.page.locator("#title").get_by_text("Edit", exact=True).click()
        self.page.get_by_test_id("task-name").fill(task_name)
        self.page.get_by_test_id("task-name-section-button").click()

    def edit_conversation_context(self, context_text: str) -> None:
        self.page.locator("#parameters-setup").get_by_role("button", name="Edit").click()
        self.page.get_by_role("textbox", name="The Conversation Context").fill(context_text)
        self.page.get_by_role("button", name="Save").click()

    def continue_to_structure(self) -> None:
        self.page.get_by_role("link", name="Continue").click()

    def upload_presentation_if_available(self, file_path: Path) -> None:
        if not file_path.exists():
            return

        self.page.get_by_test_id("edit-presentation-button").click()
        self.page.locator("#deck-settings").get_by_test_id("undefined-trigger").click()
        self.page.get_by_role("button", name="Upload PDF or PPTX").set_input_files(str(file_path))
        self.page.get_by_role("button", name="Done").click()

    def select_practice_languages(self, languages: list[str]) -> None:
        language_block = self.page.locator("#simulation-language-settings")
        language_block.scroll_into_view_if_needed()

        language_switch = language_block.locator("#language [role='switch']").first
        expect(language_switch).to_be_visible(timeout=20_000)
        if language_switch.get_attribute("aria-checked") != "true":
            language_switch.click(force=True)

        language_selector = language_block.locator("#language-selection").first
        self.page.wait_for_function(
            "() => document.querySelector('#language-selection')?.getBoundingClientRect().height > 0",
            timeout=20_000,
        )
        language_selector.click(force=True)

        search_box = self.page.get_by_placeholder("Search...")
        expect(search_box).to_be_visible(timeout=20_000)

        for language in languages:
            if self.page.locator(".tag-container").filter(has_text=language).count():
                continue

            search_box.fill(language)
            option = self.page.get_by_text(language, exact=False).last
            expect(option).to_be_visible(timeout=20_000)
            option.click(force=True)

        self.page.keyboard.press("Escape")
        self.page.keyboard.press("Escape")
        dismiss_open_popovers(self.page)

    def configure_topics_to_cover(self, topic_name: str, url: str, make_or_break: bool = True) -> None:
        self.page.get_by_test_id("edit-presentation-button").click()
        self.page.locator("#custom-topic-settings-block").get_by_test_id("undefined-trigger").click()
        self.page.locator("#custom-topic-setting").click(force=True)
        self.page.get_by_test_id("edit-topics").click(force=True)
        topic_input = self.page.get_by_test_id("topic-row-0-topic-name")
        if not topic_input.is_visible(timeout=5_000):
            return

        topic_input.fill(topic_name)
        self.page.get_by_test_id("refresh-topic-button").click()

        if make_or_break:
            make_or_break_toggle = self.page.locator(
                "[data-testid*='make-or-break'], "
                "#make-or-break, "
                "td:has-text('Make or Break') .slider, "
                ".evaluation-topics-table .sn-toggle .slider"
            ).last
            if make_or_break_toggle.count() and make_or_break_toggle.is_visible(timeout=2_000):
                make_or_break_toggle.click(force=True)

        self.page.get_by_text("Click to add URL").click()
        self.page.get_by_role("textbox", name="Link to relevant materials at").fill(url)
        self.page.get_by_role("button", name="Save").click()
        self.page.get_by_test_id("done-with-custom-topics").click()

    def expect_publish_available(self) -> None:
        expect(self.page.get_by_test_id("publish-and-share-button")).to_be_visible(timeout=60_000)
