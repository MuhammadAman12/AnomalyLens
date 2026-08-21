# AnomalyLens Deployment Guide

AnomalyLens is deployment-ready in two forms: directly from the Python project or as a Docker container.

## Option 1: Streamlit Community Cloud

1. Push the latest `main` branch to GitHub.
2. In Streamlit Community Cloud, create a new app from this repository.
3. Select `app.py` as the entry point.
4. Use Python 3.11 if the platform asks for a runtime version.
5. Deploy.

The repository already contains `requirements.txt` and `.streamlit/config.toml`, so no additional start command is required.

## Option 2: Docker

Build the image:

```bash
docker build -t anomalylens .
```

Run it:

```bash
docker run --rm -p 8501:8501 anomalylens
```

Open `http://localhost:8501`.

The image includes a health check against Streamlit's `/_stcore/health` endpoint.

## Option 3: Docker Compose

```bash
docker compose up --build
```

Stop the service with:

```bash
docker compose down
```

## Generic container hosts

The Docker image can be deployed to container platforms that accept a Dockerfile. Configure the service to expose port `8501` and allow the platform to route external traffic to that port.

## Pre-deployment verification

Run locally before publishing:

```bash
pip install -r requirements-dev.txt
python -m py_compile app.py src/*.py tests/*.py
pytest -q
streamlit run app.py
```

The GitHub Actions workflow repeats the compile, unit-test, application health-check, Docker build, and Docker container health-check steps on every push to `main` and every pull request targeting `main`.

## Production notes

- Do not upload sensitive or regulated production datasets to a public demo deployment.
- The current app processes uploaded data in the running Streamlit session and does not include persistent database storage.
- Authentication and multi-tenant isolation are not implemented yet.
- For a commercial deployment, add authentication, encrypted persistent storage where needed, logging/monitoring, rate limits, and an explicit privacy/data-retention policy.
