from __future__ import annotations

from pages.course_page import CoursePage


def test_course_page_exposes_stable_course_creation_actions() -> None:
    course = CoursePage(None)

    assert callable(course.open_new_course_form)
    assert callable(course.set_course_title)
    assert callable(course.try_continue_from_course_layout)
