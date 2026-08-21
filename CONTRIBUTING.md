# Contributing to AnomalyLens

Thanks for your interest in improving AnomalyLens.

## Local Setup

```bash
python -m venv venv
```

Activate the environment, then install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Quality Checks

Run linting:

```bash
ruff check app.py src tests
```

Compile the Python sources:

```bash
python -m py_compile app.py src/*.py tests/*.py
```

Run the test suite:

```bash
pytest
```

Run the application:

```bash
streamlit run app.py
```

## Docker Check

```bash
docker build -t anomalylens:local .
docker run --rm -p 8501:8501 anomalylens:local
```

Then visit `http://localhost:8501`.

## Pull Requests

Keep pull requests focused and explain:

- what changed
- why it changed
- how it was tested
- whether UI, ML behavior, or exported results changed

New ML behavior should include tests when practical. UI changes should preserve the existing dark analytics theme and should not weaken the core analysis workflow.
