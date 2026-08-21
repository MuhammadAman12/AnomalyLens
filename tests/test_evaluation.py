import pandas as pd
import pytest

from src.evaluation import evaluate_comparison, evaluate_predictions, get_ground_truth


def test_get_ground_truth_from_explicit_column():
    df = pd.DataFrame({"ground_truth": [0, 1, 0, 1]})

    labels, source = get_ground_truth(df)

    assert labels.tolist() == [0, 1, 0, 1]
    assert source == "Dataset column: ground_truth"


def test_get_ground_truth_normalizes_minus_one_labels():
    df = pd.DataFrame({"label": [1, -1, 1, -1]})

    labels, _ = get_ground_truth(df)

    assert labels.tolist() == [0, 1, 0, 1]


def test_evaluate_predictions_perfect_classification():
    ground_truth = pd.Series([0, 1, 0, 1])
    predictions = [1, -1, 1, -1]

    metrics = evaluate_predictions(predictions, ground_truth)

    assert metrics["accuracy"] == pytest.approx(1.0)
    assert metrics["precision"] == pytest.approx(1.0)
    assert metrics["recall"] == pytest.approx(1.0)
    assert metrics["f1"] == pytest.approx(1.0)
    assert metrics["true_positives"] == 2
    assert metrics["true_negatives"] == 2
    assert metrics["false_positives"] == 0
    assert metrics["false_negatives"] == 0


def test_evaluate_comparison_returns_one_row_per_algorithm():
    ground_truth = pd.Series([0, 1, 0, 1])
    predictions = pd.DataFrame(
        {
            "Model A": [1, -1, 1, -1],
            "Model B": [1, 1, 1, -1],
        }
    )

    result = evaluate_comparison(predictions, ground_truth)

    assert result["Algorithm"].tolist() == ["Model A", "Model B"]
    assert result.loc[0, "F1 Score"] == pytest.approx(1.0)
    assert 0 <= result.loc[1, "F1 Score"] <= 1


def test_evaluate_predictions_rejects_invalid_prediction_values():
    ground_truth = pd.Series([0, 1])

    with pytest.raises(ValueError):
        evaluate_predictions([0, 1], ground_truth)
