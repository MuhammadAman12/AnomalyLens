import io

import pandas as pd

from src.data_processing import (
    get_dataset_summary,
    get_default_feature_columns,
    get_numeric_columns,
    is_identifier_column,
    load_dataset,
    preview_dataset,
)


class UploadedCSV(io.BytesIO):
    name = "sample.csv"


def test_load_dataset_reads_csv():
    uploaded = UploadedCSV(b"a,b\n1,2\n3,4\n")
    df = load_dataset(uploaded)

    assert df.shape == (2, 2)
    assert df["a"].tolist() == [1, 3]


def test_numeric_columns_and_summary():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "amount": [10.0, 20.0, 30.0],
            "category": ["a", "b", "c"],
            "with_missing": [1.0, None, 3.0],
        }
    )

    assert get_numeric_columns(df) == ["transaction_id", "amount", "with_missing"]

    summary = get_dataset_summary(df)
    assert summary == {
        "rows": 3,
        "columns": 4,
        "numeric_features": 3,
        "missing_values": 1,
    }


def test_identifier_detection_and_default_features():
    df = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "customer_id": [100, 101, 102],
            "amount": [10.0, 20.0, 30.0],
            "frequency": [1, 2, 3],
            "account_age": [50, 60, 70],
        }
    )

    assert is_identifier_column("transaction_id")
    assert is_identifier_column("CUSTOMER_ID")
    assert not is_identifier_column("amount")

    defaults = get_default_feature_columns(df)
    assert defaults == ["amount", "frequency", "account_age"]


def test_preview_dataset_limits_rows():
    df = pd.DataFrame({"value": range(30)})
    preview = preview_dataset(df, rows=5)

    assert len(preview) == 5
    assert preview["value"].tolist() == [0, 1, 2, 3, 4]
