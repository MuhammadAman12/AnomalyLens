import pandas as pd

from src.scoring import get_top_suspicious, normalize_scores


def test_normalize_scores_maps_to_zero_and_one_hundred():
    normalized = normalize_scores([10.0, 20.0, 30.0])

    assert normalized.tolist() == [0.0, 50.0, 100.0]


def test_normalize_scores_handles_constant_input():
    normalized = normalize_scores([5.0, 5.0, 5.0])

    assert normalized.tolist() == [0.0, 0.0, 0.0]


def test_get_top_suspicious_returns_highest_scores_first():
    results = pd.DataFrame(
        {
            "record": ["a", "b", "c"],
            "Anomaly Score": [12.5, 91.0, 55.0],
        }
    )

    top = get_top_suspicious(results, limit=2)

    assert top["record"].tolist() == ["b", "c"]


def test_get_top_suspicious_returns_empty_without_score():
    results = pd.DataFrame({"record": ["a", "b"]})

    top = get_top_suspicious(results)

    assert top.empty
