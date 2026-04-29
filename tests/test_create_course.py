from __future__ import annotations

import pytest

from pages.course_page import CoursePage
from pages.home_page import HomePage
from pages.roleplay_page import RoleplayPage


CO_CREATE_MESSAGES = [
    "You are a salesman for Marvel movies. You are an expert with Marvel comics and movies.",
    "Guide me step by step.",
    "No, you should be the salesman for Marvel movies and I will be the customer.",
    (
        "The B2B scenario will be for streaming services. "
        "The company is new in streaming and wants all relevant movies and TV shows."
    ),
]


@pytest.mark.smoke
def test_create_marvel_sales_roleplay_course(page, settings) -> None:
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
    roleplay.send_co_create_messages(CO_CREATE_MESSAGES)
    course.save_course()
    course.approve_and_continue()
    course.set_task_name("Agente de ventas de peliculas Marvel - edicion especial")
    course.edit_conversation_context("")
    course.continue_to_structure()
    roleplay.set_persona_background(
        "You have knowledge of all Marvel and DC movies, TV shows, and comics."
    )
    roleplay.select_custom_persona("Toby")
    roleplay.set_ai_persona_opener("Hi i am Toby, how are you ?")
    course.upload_presentation_if_available(settings.resume_pdf_path)
    course.select_practice_languages(["English", "Hebrew"])
    course.configure_topics_to_cover("Marvel universe", "https://en.wikipedia.org/wiki/Marvel_Studios")
    course.save_course()
    course.expect_publish_available()
