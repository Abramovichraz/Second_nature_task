from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


ROOT_DIR = Path(__file__).parent


@dataclass(frozen=True)
class Settings:
    email: str
    password: str
    login_url: str
    base_url: str
    roleplay_test_url: str
    headless: bool
    slow_mo_ms: int
    salesman_image_path: Path
    resume_pdf_path: Path
    large_test_file_path: Path


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _path_env(name: str, default: str) -> Path:
    raw_path = os.getenv(name, default)
    path = Path(raw_path)
    return path if path.is_absolute() else ROOT_DIR / path


@pytest.fixture(scope="session")
def settings() -> Settings:
    load_dotenv(ROOT_DIR / ".env")

    return Settings(
        email=os.getenv("SECOND_NATURE_EMAIL", ""),
        password=os.getenv("SECOND_NATURE_PASSWORD", ""),
        login_url=os.getenv("SECOND_NATURE_LOGIN_URL", ""),
        base_url=os.getenv("SECOND_NATURE_BASE_URL", "https://app.secondnature.ai"),
        roleplay_test_url=os.getenv("SECOND_NATURE_ROLEPLAY_URL", ""),
        headless=_bool_env("HEADLESS", False),
        slow_mo_ms=int(os.getenv("SLOW_MO_MS", "100")),
        salesman_image_path=_path_env("SALESMAN_IMAGE_PATH", "assets/salesman.png"),
        resume_pdf_path=_path_env("RESUME_PDF_PATH", "assets/CV.Raz_Abramovich.pdf"),
        large_test_file_path=_path_env("LARGE_TEST_FILE_PATH", "assets/large_test_file.pdf"),
    )


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture()
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser = playwright_instance.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo_ms,
    )
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    context.set_default_timeout(20_000)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    return context.new_page()
