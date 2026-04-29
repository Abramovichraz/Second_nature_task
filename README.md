# Second Nature Playwright Automation

End-to-end test automation for the Second Nature course editor using Python, pytest, and Playwright.

The project follows the Page Object Model so UI selectors and business actions are kept in `pages/`, while test intent remains clear in `tests/`.

## Project Structure

```text
project/
├── pages/
│   ├── home_page.py
│   ├── course_page.py
│   └── roleplay_page.py
├── tests/
│   ├── test_create_course.py
│   ├── test_validation.py
│   ├── test_persistence.py
│   └── test_roleplay.py
├── conftest.py
├── utils/
├── README.md
├── requirements.txt
├── pytest.ini
└── .env.example
```

## What Is Covered

- Login through the stable Second Nature application URL.
- Course creation from the course editor.
- AI Assistant role-play template creation.
- Co-create chat interaction with retry handling for transient AI errors.
- Course save and approve flow.
- Custom persona selection for `Toby`.
- AI persona opener update.
- Language settings for English and Hebrew.
- Topics to Cover configuration with a Marvel Studios helpful link.

## Prerequisites

- Python 3.11 or newer.
- Access to a valid Second Nature test account.
- Chromium browser installed through Playwright.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install the Playwright browser:

```powershell
python -m playwright install chromium
```

## Configuration

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your test credentials:

```text
SECOND_NATURE_EMAIL=your.email@example.com
SECOND_NATURE_PASSWORD=your-password
SECOND_NATURE_BASE_URL=https://app.secondnature.ai
SECOND_NATURE_LOGIN_URL=
SECOND_NATURE_ROLEPLAY_URL=
HEADLESS=false
SLOW_MO_MS=100
```

`SECOND_NATURE_LOGIN_URL` is optional. Leave it empty unless you intentionally want to start from a specific Auth0 URL. Auth0 state URLs can expire, so the default behavior is to start from `SECOND_NATURE_BASE_URL` and let the application create a fresh login session.

`SECOND_NATURE_ROLEPLAY_URL` is optional. Set it to a direct role-play/test screen URL to run the role-play smoke test. When it is empty, that test is skipped rather than creating a long AI setup flow.

## Running Tests

Run the full suite:

```powershell
python -m pytest
```

Run only the main smoke flow:

```powershell
python -m pytest -m smoke
```

Run a specific file:

```powershell
python -m pytest tests/test_create_course.py
```

Run with the browser visible:

```powershell
$env:HEADLESS="false"
python -m pytest -s
```

## Test Design

`pages/home_page.py`
: Login and home page readiness checks.

`pages/course_page.py`
: Course editor actions such as creating a course shell, saving, language settings, presentation settings, and Topics to Cover.

`pages/roleplay_page.py`
: Role-play setup actions such as template selection, AI co-create chat, custom persona selection, and conversation opener editing.

`utils/`
: Shared UI helpers for retrying unstable fills and dismissing blocking popovers.

## Stability Notes

The AI co-create step depends on live generation and can occasionally take longer than a normal deterministic UI action. The test includes retry handling for this exact application response:

```text
Oops! Something went wrong, could you try entering your message again?
```

If that response appears more than two times for the same message, the test fails with a clear assertion.

Validation tests intentionally document current product gaps with strict `xfail` markers:

- Course title currently accepts more than 70 characters.
- Empty course title currently allows continuing to the next step.
- Empty Conversation Context may currently save successfully.

When the product behavior is fixed, pytest will report XPASS failures so the known-bug markers can be removed.

## Security

Do not commit `.env`, credentials, storage state, reports, or generated browser artifacts. These are excluded by `.gitignore`.
