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
        return pd.Series([0.0] * len(scores), index=scores.index)

    normalized = (
        (scores - min_score)
        / (max_score - min_score)
        * 100
    )

    return normalized.round(2)


def score_to_severity(score):
    """Map a normalized 0-100 anomaly score to an investigation severity."""

    if pd.isna(score):
        return "Unknown"
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def add_severity_labels(results):
    """Add a Severity column when anomaly scores are available."""

    enriched = results.copy()

    if "Anomaly Score" in enriched.columns:
        enriched["Severity"] = enriched["Anomaly Score"].apply(score_to_severity)

    return enriched


def get_top_suspicious(results, limit=10):
    """Return the highest-scoring detected anomalies."""

    if "Anomaly Score" not in results.columns:
        return results.head(0)

    candidates = results.copy()

    if "Anomaly" in candidates.columns:
        anomaly_only = candidates[candidates["Anomaly"] == "Anomaly"]
        if not anomaly_only.empty:
            candidates = anomaly_only

    candidates = add_severity_labels(candidates)

    return (
        candidates
        .sort_values("Anomaly Score", ascending=False)
        .head(limit)
    )
