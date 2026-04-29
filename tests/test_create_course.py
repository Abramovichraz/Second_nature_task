from __future__ import annotations

import pytest

from pages.course_page import CoursePage
from pages.home_page import HomePage
from pages.roleplay_page import RoleplayPage


@pytest.mark.smoke
def test_create_course_and_add_roleplay_template(page, settings) -> None:
    HomePage(page).login(
        settings.login_url,
        settings.email,
        settings.password,
        settings.base_url,
    )

    course = CoursePage(page)
    roleplay = RoleplayPage(page)

    course.create_course_shell("AI assistant - QA assignment [Raz Abramovich]")
    roleplay.add_ai_assistant_roleplay_template()
    roleplay.expect_template_ready_for_ai_creation()
