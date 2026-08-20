import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

st.set_page_config(
    page_title="AnomalyLens",
    page_icon="🔍",
    layout="wide"
)

# Header
st.title("🔍 AnomalyLens")
st.markdown("### Machine Learning Anomaly Detection Platform")

st.write(
    "Upload a dataset, select numerical features, and use "
    "machine learning to identify unusual observations."
)

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Upload a dataset to begin.")
    st.stop()

# Load dataset
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

except Exception as e:
    st.error(f"Could not read the dataset: {e}")
    st.stop()

st.success(
    f"Dataset loaded successfully: "
    f"{df.shape[0]:,} rows × {df.shape[1]} columns"
)

# Dataset overview
st.subheader("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", f"{len(df):,}")
col2.metric("Columns", len(df.columns))

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

col3.metric("Numeric Features", len(numeric_columns))
col4.metric(
    "Missing Values",
    int(df.isna().sum().sum())
)

with st.expander("Preview Dataset"):
    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# Validate features
if len(numeric_columns) < 2:
    st.error(
        "The dataset needs at least two numerical columns "
        "for anomaly detection."
    )
    st.stop()

# Detection settings
st.subheader("⚙️ Detection Settings")

selected_columns = st.multiselect(
    "Select features",
    numeric_columns,
    default=numeric_columns[:min(4, len(numeric_columns))]
)

if len(selected_columns) < 2:
    st.warning("Select at least two features.")
    st.stop()

algorithm = st.selectbox(
    "Choose detection algorithm",
    [
        "Isolation Forest",
        "Local Outlier Factor"
    ]
)

contamination = st.slider(
    "Expected anomaly percentage",
    min_value=0.01,
    max_value=0.20,
    value=0.05,
    step=0.01
)

# Detection
if st.button(
    "🔍 Detect Anomalies",
    type="primary"
):

    X = df[selected_columns].copy()

    # Handle missing values
    X = X.fillna(X.median())

    if algorithm == "Isolation Forest":

        model = IsolationForest(
            contamination=contamination,
            random_state=42
        )

        predictions = model.fit_predict(X)

    else:

        model = LocalOutlierFactor(
            n_neighbors=20,
            contamination=contamination
        )

        predictions = model.fit_predict(X)

    results = df.copy()

    results["Anomaly"] = predictions

    results["Anomaly"] = results["Anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # Calculate metrics
    anomaly_count = (
        results["Anomaly"] == "Anomaly"
    ).sum()

    normal_count = (
        results["Anomaly"] == "Normal"
    ).sum()

    anomaly_percentage = (
        anomaly_count / len(results)
    ) * 100

    # Results
    st.subheader("📊 Detection Results")

    result_col1, result_col2, result_col3 = st.columns(3)

    result_col1.metric(
        "Total Records",
        f"{len(results):,}"
    )

    result_col2.metric(
        "Normal Records",
        f"{normal_count:,}"
    )

    result_col3.metric(
        "Anomalies",
        f"{anomaly_count:,}",
        f"{anomaly_percentage:.1f}%"
    )

    # Visualization
    st.subheader("📈 Anomaly Visualization")

    fig = px.scatter(
        results,
        x=selected_columns[0],
        y=selected_columns[1],
        color="Anomaly",
        hover_data=selected_columns,
        title=(
            f"{algorithm}: "
            f"{selected_columns[0]} vs "
            f"{selected_columns[1]}"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Anomaly table
    st.subheader("🔎 Detected Anomalies")

    anomalies = results[
        results["Anomaly"] == "Anomaly"
    ]

    st.dataframe(
        anomalies,
        use_container_width=True
    )

    # Download results
    csv = results.to_csv(index=False)

    st.download_button(
        "⬇️ Download Full Results",
        data=csv,
        file_name="anomaly_results.csv",
        mime="text/csv"
    )