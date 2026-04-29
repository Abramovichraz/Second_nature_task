# Second Nature Playwright Automation

Python + pytest + Playwright automation suite for a Second Nature QA assignment.

The suite is intentionally focused on stable UI behavior. It avoids long AI conversations and does not validate AI-generated content.

> AI responses are not validated due to their non-deterministic nature. Automation focuses on stable UI flows and system behavior.

## Project Structure

```text
project/
|-- pages/
|   |-- home_page.py
|   |-- course_page.py
|   `-- roleplay_page.py
|-- tests/
|   |-- test_create_course.py
|   |-- test_validation.py
|   |-- test_persistence.py
|   `-- test_roleplay.py
|-- conftest.py
|-- utils/
|-- README.md
|-- requirements.txt
|-- pytest.ini
`-- .env.example
```

## What Is Tested

- Home page readiness after authentication.
- Short course creation smoke flow:
  - Create a course.
  - Fill the title.
  - Move to the next step.
  - Add the AI Assistant role-play template.
- Stable validation checks.
- Role-play smoke test, when a direct role-play URL is configured:
  - Role-play screen opens.
  - Chat input is visible.
  - Send button is visible.
  - One short message can be sent with retry handling for the known transient AI error.

## What Is Not Tested

- AI response correctness.
- Marvel/DC factual accuracy.
- Long AI co-create conversations.
- Persona quality, voice quality, or generated content quality.
- Visual pixel-perfect checks.

## Manual vs Automation Scope

The manual testing phase included extensive coverage of:

- AI behavior and response validation.
- Multilingual scenarios, including Hebrew, English, RTL, and LTR.
- Edge cases, including long inputs and large file uploads.
- UI and UX issues.

Automation focuses only on stable and deterministic flows such as:

- Stable UI flows.
- Input validation.
- Smoke tests.

Complex scenarios involving AI behavior and dynamic content were intentionally tested manually.

## Prerequisites

- Python 3.11 or newer.
- Access to a valid Second Nature test account.
- Chromium installed through Playwright.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Install the Playwright browser:

```powershell
python -m playwright install chromium
```

## Environment Configuration

Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

Example `.env`:

```text
SECOND_NATURE_EMAIL=your.email@example.com
SECOND_NATURE_PASSWORD=your-password
SECOND_NATURE_BASE_URL=https://app.secondnature.ai
SECOND_NATURE_LOGIN_URL=
SECOND_NATURE_ROLEPLAY_URL=
HEADLESS=false
SLOW_MO_MS=100
```

`SECOND_NATURE_LOGIN_URL` is optional. Leave it empty to start from `SECOND_NATURE_BASE_URL` and let the application create a fresh Auth0 state.

`SECOND_NATURE_ROLEPLAY_URL` is optional but required for `tests/test_roleplay.py`. Set it to a direct URL for an existing role-play/test screen. If it is empty, the role-play smoke test is skipped by design.

## Running Tests

Run the full suite:

```powershell
python -m pytest
```

Run smoke tests:

```powershell
python -m pytest -m smoke
```

Run one test file:

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
: Authentication entry point and home page readiness.

`pages/course_page.py`
: Course setup actions and title validation helpers.

`pages/roleplay_page.py`
: Role-play template setup and role-play chat smoke helpers.

`utils/`
: Shared UI helpers for stable interactions.

## AI Retry Handling

The role-play smoke test uses:

```python
send_message_with_retry(page, message, max_retries=2)
```

The helper retries only when this known transient AI error appears:

```text
Oops! Something went wrong, could you try entering your message again?
```

After the configured retry limit, the test fails clearly.

## Validation Notes

Validation tests document only behavior that is reproducible in the current product.
Known product gaps identified during manual testing are documented separately in the bug report and are not all automated, in order to avoid flaky or environment-dependent tests.
If a validation rule is not enforced in the current environment, the related automated check is skipped with a clear reason instead of being marked as a false failure.

## Security

Do not commit `.env`, credentials, storage state, reports, browser traces, or generated artifacts. These files are excluded by `.gitignore`.
