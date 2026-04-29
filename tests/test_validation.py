from __future__ import annotations

import pytest
from playwright.sync_api import expect

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
    reason="Known validation bug: course title currently accepts more than 70 characters.",
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
    reason="Known validation bug: empty course title currently allows continuing to the next step.",
    strict=True,
)
def test_required_course_title_blocks_continue(page, settings) -> None:
    login(page, settings)
    course = CoursePage(page)

    course.open_new_course_form()
    course.set_course_title("")
    current_url = page.url
    course.try_continue_from_course_layout()

    validation_visible = page.get_by_text("required", exact=False).is_visible(timeout=3_000)
    still_on_title_step = page.url == current_url and page.get_by_test_id("title").is_visible(timeout=3_000)
    assert validation_visible or still_on_title_step


@pytest.mark.xfail(
    reason=(
        "Known product behavior to verify: empty Conversation Context may currently be saved. "
        "If the product accepts an empty context, this should remain documented as a known bug."
    ),
    strict=True,
)
def test_empty_conversation_context_should_not_save(page, settings) -> None:
    login(page, settings)
    course = CoursePage(page)

    course.create_course_shell("Validation - empty conversation context")
    course.edit_conversation_context("")
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("required", exact=False)).to_be_visible(timeout=5_000)
