import pandas as pd


GROUND_TRUTH_COLUMNS = (
    "ground_truth",
    "is_anomaly",
    "anomaly_label",
    "label",
    "target",
)


def _normalize_ground_truth(series):
    """Normalize common binary anomaly labels to 0=normal and 1=anomaly."""

    if pd.api.types.is_bool_dtype(series):
        return series.astype(int)

    if pd.api.types.is_numeric_dtype(series):
        unique_values = set(series.dropna().unique().tolist())

        if unique_values.issubset({0, 1}):
            return series.astype(int)

        if unique_values.issubset({-1, 1}):
            return series.map({1: 0, -1: 1}).astype(int)

    normalized = series.astype(str).str.strip().str.lower()
    mapping = {
        "normal": 0,
        "inlier": 0,
        "false": 0,
        "0": 0,
        "anomaly": 1,
        "anomalous": 1,
        "outlier": 1,
        "true": 1,
        "1": 1,
    }

    mapped = normalized.map(mapping)
    if mapped.notna().all():
        return mapped.astype(int)

    return None


def get_ground_truth(df):
    """
    Return normalized ground-truth labels when the dataset contains them.

    The bundled legacy synthetic dataset did not originally include an
    explicit label column. For that exact dataset shape, transaction IDs
    951-1000 are known injected anomalies and are inferred as ground truth.
    """

    for column in GROUND_TRUTH_COLUMNS:
        if column in df.columns:
            labels = _normalize_ground_truth(df[column])
            if labels is not None:
                return labels, f"Dataset column: {column}"

    if "transaction_id" in df.columns and len(df) == 1000:
        transaction_ids = pd.to_numeric(df["transaction_id"], errors="coerce")
        if (
            transaction_ids.notna().all()
            and transaction_ids.nunique() == 1000
            and int(transaction_ids.min()) == 1
            and int(transaction_ids.max()) == 1000
        ):
            labels = (transaction_ids > 950).astype(int)
            return labels, "Legacy synthetic sample labels inferred from transaction_id"

    return None, None


def evaluate_predictions(predictions, ground_truth):
    """Calculate classification metrics for anomaly predictions."""

    from sklearn.metrics import (
        accuracy_score,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
    )

    predicted = pd.Series(predictions, index=ground_truth.index)
    predicted_binary = predicted.map({1: 0, -1: 1})

    if predicted_binary.isna().any():
        raise ValueError("Predictions must use 1 for normal and -1 for anomaly.")

    tn, fp, fn, tp = confusion_matrix(
        ground_truth,
        predicted_binary,
        labels=[0, 1],
    ).ravel()

    return {
        "accuracy": accuracy_score(ground_truth, predicted_binary),
        "precision": precision_score(ground_truth, predicted_binary, zero_division=0),
        "recall": recall_score(ground_truth, predicted_binary, zero_division=0),
        "f1": f1_score(ground_truth, predicted_binary, zero_division=0),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }


def evaluate_comparison(comparison_predictions, ground_truth):
    """Evaluate every algorithm in a comparison prediction DataFrame."""

    rows = []

    for algorithm in comparison_predictions.columns:
        metrics = evaluate_predictions(
            comparison_predictions[algorithm],
            ground_truth,
        )
        rows.append(
            {
                "Algorithm": algorithm,
                "Precision": metrics["precision"],
                "Recall": metrics["recall"],
                "F1 Score": metrics["f1"],
                "Accuracy": metrics["accuracy"],
                "True Positives": metrics["true_positives"],
                "False Positives": metrics["false_positives"],
                "False Negatives": metrics["false_negatives"],
            }
        )

    return pd.DataFrame(rows)
