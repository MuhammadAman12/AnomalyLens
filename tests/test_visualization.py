import pandas as pd

from src.visualization import (
    create_algorithm_comparison,
    create_anomaly_distribution,
    create_anomaly_scatter,
)


def test_create_anomaly_distribution_returns_donut_chart():
    results = pd.DataFrame(
        {
            "feature_a": [1.0, 2.0, 3.0, 9.0],
            "feature_b": [1.0, 2.0, 3.0, 9.0],
            "Anomaly": ["Normal", "Normal", "Normal", "Anomaly"],
        }
    )

    fig = create_anomaly_distribution(results)

    assert len(fig.data) == 1
    assert fig.data[0].type == "pie"
    assert fig.data[0].hole > 0
    assert fig.layout.annotations[0].text.startswith("<b>1</b>")


def test_create_anomaly_scatter_has_normal_and_anomaly_traces():
    results = pd.DataFrame(
        {
            "feature_a": [1.0, 2.0, 9.0],
            "feature_b": [1.5, 2.5, 9.5],
            "Anomaly": ["Normal", "Normal", "Anomaly"],
        }
    )

    fig = create_anomaly_scatter(
        results,
        "feature_a",
        "feature_b",
        "Isolation Forest",
    )

    trace_names = {trace.name for trace in fig.data}

    assert trace_names == {"Normal", "Anomaly"}
    assert fig.layout.height == 520


def test_create_algorithm_comparison_uses_three_model_bars():
    comparison = pd.DataFrame(
        {
            "Algorithm": [
                "Isolation Forest",
                "Local Outlier Factor",
                "DBSCAN",
            ],
            "Anomalies Detected": [5, 6, 7],
        }
    )

    fig = create_algorithm_comparison(comparison)

    assert len(fig.data) == 3
    assert {trace.name for trace in fig.data} == {
        "Isolation Forest",
        "Local Outlier Factor",
        "DBSCAN",
    }
    assert fig.layout.height == 460
