from __future__ import annotations

from playwright.sync_api import Page, expect


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

    def title_input_is_visible(self) -> bool:
        return self.page.get_by_test_id("title").is_visible(timeout=3_000)

    def try_continue_from_course_layout(self) -> None:
        self.page.get_by_test_id("next-step-button").click()

    def create_course_shell(self, title: str) -> None:
        self.open_new_course_form()
        self.set_course_title(title)
        self.try_continue_from_course_layout()
        expect(self.page.get_by_test_id("task-selector-button")).to_be_visible(timeout=30_000)
