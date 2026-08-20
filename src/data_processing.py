import pandas as pd


def load_dataset(uploaded_file):
    """
    Load a CSV or Excel dataset.
    """

    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Unsupported file type.")


def get_numeric_columns(df):
    """
    Return all numeric columns from the dataset.
    """

    return df.select_dtypes(
        include="number"
    ).columns.tolist()


def get_dataset_summary(df):
    """
    Return basic dataset statistics.
    """

    numeric_columns = get_numeric_columns(df)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_features": len(numeric_columns),
        "missing_values": int(
            df.isna().sum().sum()
        )
    }


def preview_dataset(df, rows=20):
    """
    Return the first rows of a dataset.
    """

    return df.head(rows)