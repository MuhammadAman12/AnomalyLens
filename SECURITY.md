# Security Policy

## Supported Version

AnomalyLens is currently under active development. Security fixes are applied to the latest version on the `main` branch.

## Reporting a Security Issue

Please do not open a public GitHub issue for a vulnerability that could expose sensitive data or create an exploitable condition.

Instead, contact the repository owner privately with:

- a clear description of the issue
- steps to reproduce it
- the affected file or component
- the potential impact
- any suggested mitigation, if known

Please avoid including real credentials, private datasets, API keys, or other sensitive information in reports.

## Data Handling Notes

AnomalyLens processes datasets supplied by the user. The current Streamlit application does not intentionally persist uploaded datasets outside the application session, but users should still avoid uploading confidential or regulated data to untrusted deployments.
