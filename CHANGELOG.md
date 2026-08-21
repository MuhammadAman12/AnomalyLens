# Changelog

All notable changes to AnomalyLens are documented in this file.

The project follows semantic versioning for public portfolio releases.

## [1.0.0] - 2026-08-22

### Added

- Public Streamlit Community Cloud deployment.
- CSV and Excel dataset upload support.
- Isolation Forest, Local Outlier Factor, and DBSCAN anomaly detection.
- Single-model and multi-model comparison workflows.
- Identifier-aware default feature selection.
- Ground-truth label detection and target leakage protection.
- Precision, recall, F1 score, accuracy, and confusion-matrix evaluation.
- Normalized anomaly scoring for Isolation Forest and LOF.
- Severity-based suspicious-record ranking.
- Multi-model agreement and consensus analysis.
- Interactive Plotly visualizations with selectable scatter axes.
- Exportable analysis and comparison results.
- Custom dark Streamlit dashboard styling.
- Automated unit and visualization regression tests.
- Ruff linting and project quality configuration.
- GitHub Actions CI for compilation, linting, tests, Streamlit health checks, and Docker smoke checks.
- Docker, Docker Compose, and GitHub Container Registry publishing support.
- Dependabot, security policy, and contribution guidelines.

### Improved

- Streamlit startup performance through lazy loading of heavier machine-learning, evaluation, and visualization dependencies.
- Repository documentation and portfolio presentation.
- Persistent analysis behavior so visualization controls do not unnecessarily discard results.

### Notes

- The public portfolio build is available at https://anomalylens.streamlit.app.
- DBSCAN currently uses anomaly labels based on noise detection but does not yet expose a normalized anomaly score.
