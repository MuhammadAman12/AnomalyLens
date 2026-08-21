import numpy as np
import pandas as pd

from src.anomaly_detection import (
    compare_algorithms,
    detect_anomalies,
    detect_dbscan,
    detect_isolation_forest,
    detect_lof,
    prepare_features,
)


def make_dataset():
    rng = np.random.default_rng(42)
    normal = rng.normal(0, 1, size=(60, 3))
    anomalies = rng.normal(8, 0.5, size=(6, 3))
    values = np.vstack([normal, anomalies])
    return pd.DataFrame(values, columns=["a", "b", "c"])


def test_prepare_features_fills_missing_values():
    df = pd.DataFrame({"a": [1.0, None, 3.0], "b": [4.0, 5.0, 6.0]})

    features = prepare_features(df, ["a", "b"])

    assert not features.isna().any().any()
    assert features.loc[1, "a"] == 2.0


def test_isolation_forest_returns_predictions_and_scores():
    X = make_dataset()

    predictions, scores = detect_isolation_forest(X, contamination=0.1)

    assert len(predictions) == len(X)
    assert len(scores) == len(X)
    assert set(predictions).issubset({-1, 1})


def test_lof_returns_predictions_and_scores():
    X = make_dataset()

    predictions, scores = detect_lof(X, contamination=0.1)

    assert len(predictions) == len(X)
    assert len(scores) == len(X)
    assert set(predictions).issubset({-1, 1})


def test_dbscan_returns_anomaly_labels():
    X = make_dataset()

    predictions = detect_dbscan(X)

    assert len(predictions) == len(X)
    assert set(predictions).issubset({-1, 1})


def test_detect_anomalies_dispatches_supported_model():
    X = make_dataset()

    predictions, scores = detect_anomalies(X, "Isolation Forest", 0.1)

    assert len(predictions) == len(X)
    assert scores is not None


def test_compare_algorithms_returns_expected_columns():
    X = make_dataset()

    comparison = compare_algorithms(X, contamination=0.1)

    assert list(comparison.columns) == [
        "Isolation Forest",
        "Local Outlier Factor",
        "DBSCAN",
    ]
    assert len(comparison) == len(X)
