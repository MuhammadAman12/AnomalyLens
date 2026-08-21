import pandas as pd


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
    """
    Return True when a column name looks like an identifier.

    Identifier-like numerical columns remain available for manual selection,
    but are excluded from the default ML feature set because IDs usually
    describe record identity rather than behaviour.
    """

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


def get_default_feature_columns(df, max_features=4):
    """
    Choose sensible default numerical features for anomaly detection.

    Identifier-like columns are skipped automatically. If too few
    behavioural numerical columns remain, numeric columns are used as a
    fallback so the user can still run the application.
    """

    numeric_columns = get_numeric_columns(df)

    preferred = [
        column
        for column in numeric_columns
        if not is_identifier_column(column)
    ]

    if len(preferred) >= 2:
        return preferred[:max_features]

    return numeric_columns[:max_features]


def get_dataset_summary(df):
    """Return basic dataset statistics."""

    numeric_columns = get_numeric_columns(df)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_features": len(numeric_columns),
        "missing_values": int(df.isna().sum().sum()),
    }


def preview_dataset(df, rows=20):
    """Return the first rows of a dataset."""

    return df.head(rows)
