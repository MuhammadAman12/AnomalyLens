import pandas as pd


TARGET_COLUMN_NAMES = {
    "ground_truth",
    "is_anomaly",
    "anomaly_label",
    "label",
    "target",
}


def load_dataset(uploaded_file):
    """Load a CSV or Excel dataset."""

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if filename.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Unsupported file type.")


def get_numeric_columns(df):
    """Return all numeric columns from the dataset."""

    return df.select_dtypes(include="number").columns.tolist()


def is_identifier_column(column_name):
    """Return True when a column name looks like a record identifier."""

    normalized = str(column_name).strip().lower()

    identifier_names = {
        "id",
        "index",
        "row_id",
        "record_id",
        "transaction_id",
        "customer_id",
        "user_id",
        "account_id",
    }

    return (
        normalized in identifier_names
        or normalized.endswith("_id")
        or normalized.startswith("id_")
    )


def is_target_column(column_name):
    """Return True when a column name looks like a known label/target column."""

    return str(column_name).strip().lower() in TARGET_COLUMN_NAMES


def get_model_feature_columns(df):
    """
    Return numerical columns that may be selected as model inputs.

    Explicit label/target columns are excluded to prevent target leakage.
    Identifier columns remain available for manual selection, but are not
    selected by default.
    """

    return [
        column
        for column in get_numeric_columns(df)
        if not is_target_column(column)
    ]


def get_default_feature_columns(df, max_features=4):
    """Choose sensible default numerical features for anomaly detection."""

    feature_columns = get_model_feature_columns(df)

    preferred = [
        column
        for column in feature_columns
        if not is_identifier_column(column)
    ]

    if len(preferred) >= 2:
        return preferred[:max_features]

    return feature_columns[:max_features]


def get_dataset_summary(df):
    """Return basic dataset statistics."""

    feature_columns = get_model_feature_columns(df)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_features": len(feature_columns),
        "missing_values": int(df.isna().sum().sum()),
    }


def preview_dataset(df, rows=20):
    """Return the first rows of a dataset."""

    return df.head(rows)
