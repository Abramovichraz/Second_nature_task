from __future__ import annotations

import pytest

from pages.course_page import CoursePage
from pages.home_page import HomePage


def login(page, settings) -> None:
    HomePage(page).login(
        settings.login_url,
        settings.email,
        settings.password,
        settings.base_url,
    )


@pytest.mark.xfail(
    reason="Confirmed product validation gap: course title is not limited to 70 characters in the current environment.",
    strict=True,
)
def test_course_title_max_length_is_limited_to_70_characters(page, settings) -> None:
    login(page, settings)
    course = CoursePage(page)
    long_title = "AI assistant QA assignment " + ("x" * 80)

    course.open_new_course_form()
    course.set_course_title(long_title)

    assert len(course.course_title_value()) <= 70


@pytest.mark.xfail(
    reason="Confirmed product validation gap: empty course title can currently continue to the next step.",
    strict=True,
)
def test_required_course_title_blocks_continue(page, settings) -> None:
    login(page, settings)
    course = CoursePage(page)

    course.open_new_course_form()
    course.set_course_title("")
    current_url = page.url
    course.try_continue_from_course_layout()

    assert page.url == current_url
    assert course.title_input_is_visible()
