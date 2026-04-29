from __future__ import annotations

from pages.course_page import CoursePage


def test_course_page_exposes_persistence_actions() -> None:
    course = CoursePage(None)

    assert callable(course.save_course)
    assert callable(course.expect_publish_available)
