import pandas as pd


def normalize_scores(scores):
    """
    Convert raw anomaly scores to a 0-100 scale.

    Higher score means the observation is more anomalous.
    """

    scores = pd.Series(scores)

    min_score = scores.min()
    max_score = scores.max()

    if max_score == min_score:
        return pd.Series(
            [0.0] * len(scores),
            index=scores.index
        )

    normalized = (
        (scores - min_score)
        / (max_score - min_score)
        * 100
    )

    return normalized.round(2)


def get_top_suspicious(results, limit=10):
    """
    Return the records with the highest anomaly scores.
    """

    if "Anomaly Score" not in results.columns:
        return results.head(0)

    return (
        results
        .sort_values(
            "Anomaly Score",
            ascending=False
        )
        .head(limit)
    )