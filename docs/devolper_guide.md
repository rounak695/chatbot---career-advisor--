# Developer Guide

... (other sections by Person A, B, D) ...

---

## 🤖 AI Setup (Person C)

This section covers the setup and architecture of the AI components, primarily managed by the `core/llm_engine.py` and `core/prompts.py` files.

### 1. Environment Configuration

The AI engine uses the OpenAI API. To enable it, you must configure your environment variables.

1.  **Create a `.env` file**: In the project's root directory, create a file named `.env`.
2.  **Get an OpenAI API Key**: Sign up on the [OpenAI Platform](https://platform.openai.com/) and generate a new secret key.
3.  **Add Key to `.env`**: Add your API key to the `.env` file like this:
    ```
    OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
    ```
    The `.gitignore` file is already configured to ignore the `.env` file, so your key will not be committed to version control.

### 2. Core Components

* **`core/llm_engine.py`**: This is the heart of the AI. The `LLMEngine` class handles all communication with the OpenAI API through the `langchain` library. It initializes the `ChatOpenAI` model and uses a `RunnableWithMessageHistory` to automatically manage conversation context. Session history is stored in-memory, keyed by a `session_id`.

* **`core/prompts.py`**: This file contains the `CAREER_ADVISOR_PROMPT`, which is a `ChatPromptTemplate`. This template defines the persona, tone, and instructions for the chatbot. **Modifying this prompt is the primary way to alter the chatbot's behavior and personality.**

* **`utils/errors.py`**: Defines the `LLMResponseError` custom exception. This is used to gracefully handle failures in the `LLMEngine` (e.g., API key is invalid, network error). The main application can catch this specific error to display a user-friendly fallback message.

### 3. How to Test the LLM

Unit tests for the LLM are located in `tests/test_llm_engine.py`.

* **Mocking**: The tests **do not** make real API calls. They use `unittest.mock.patch` to mock the `ChatOpenAI` class. This makes tests fast, deterministic, and free.
* **Fixtures**: Test cases with sample user inputs are defined in `tests/fixtures.json`. These are used to guide the creation of tests that check for expected *behavior* rather than exact string outputs, as LLM responses can vary.

To run the tests, use `pytest`:
```bash
pytest tests/test_llm_engine.py