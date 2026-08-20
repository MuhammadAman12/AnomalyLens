import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AnomalyLens",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🔍 AnomalyLens")
st.markdown("### Machine Learning Anomaly Detection Platform")

st.write(
    "Upload a dataset, select numerical features, and use "
    "machine learning to identify unusual observations."
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV or Excel dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Upload a dataset to begin.")
    st.stop()


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

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


# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.subheader("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Rows",
    f"{len(df):,}"
)

col2.metric(
    "Columns",
    len(df.columns)
)

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

col3.metric(
    "Numeric Features",
    len(numeric_columns)
)

col4.metric(
    "Missing Values",
    int(df.isna().sum().sum())
)


with st.expander("Preview Dataset"):
    st.dataframe(
        df.head(20),
        use_container_width=True
    )


# --------------------------------------------------
# VALIDATE FEATURES
# --------------------------------------------------

if len(numeric_columns) < 2:
    st.error(
        "The dataset needs at least two numerical columns "
        "for anomaly detection."
    )
    st.stop()


# --------------------------------------------------
# DETECTION SETTINGS
# --------------------------------------------------

st.subheader("⚙️ Detection Settings")

selected_columns = st.multiselect(
    "Select features",
    numeric_columns,
    default=numeric_columns[:min(4, len(numeric_columns))]
)

if len(selected_columns) < 2:
    st.warning("Select at least two features.")
    st.stop()


detection_mode = st.radio(
    "Detection Mode",
    [
        "Single Algorithm",
        "Compare All Algorithms"
    ],
    horizontal=True
)

if detection_mode == "Single Algorithm":

    algorithm = st.selectbox(
        "Choose detection algorithm",
        [
            "Isolation Forest",
            "Local Outlier Factor",
            "DBSCAN"
        ]
    )

contamination = st.slider(
    "Expected anomaly percentage",
    min_value=0.01,
    max_value=0.20,
    value=0.05,
    step=0.01
)


# --------------------------------------------------
# DETECTION
# --------------------------------------------------

if st.button(
    "🔍 Detect Anomalies",
    type="primary"
):

    X = df[selected_columns].copy()

    # Handle missing values
    X = X.fillna(X.median())

    # --------------------------------------------------
    # SINGLE ALGORITHM MODE
    # --------------------------------------------------

    if detection_mode == "Single Algorithm":

        if algorithm == "Isolation Forest":

            model = IsolationForest(
                contamination=contamination,
                random_state=42
            )

            predictions = model.fit_predict(X)

        elif algorithm == "Local Outlier Factor":

            model = LocalOutlierFactor(
                n_neighbors=20,
                contamination=contamination
            )

            predictions = model.fit_predict(X)

        else:

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            model = DBSCAN(
                eps=0.8,
                min_samples=10
            )

            predictions = model.fit_predict(X_scaled)

            predictions = [
                -1 if label == -1 else 1
                for label in predictions
            ]

        # Create results
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

        # Download
        csv = results.to_csv(index=False)

        st.download_button(
            "⬇️ Download Full Results",
            data=csv,
            file_name="anomaly_results.csv",
            mime="text/csv"
        )

    # --------------------------------------------------
    # COMPARE ALL ALGORITHMS
    # --------------------------------------------------

    else:

        # Isolation Forest
        isolation_model = IsolationForest(
            contamination=contamination,
            random_state=42
        )

        isolation_predictions = (
            isolation_model.fit_predict(X)
        )

        # Local Outlier Factor
        lof_model = LocalOutlierFactor(
            n_neighbors=20,
            contamination=contamination
        )

        lof_predictions = (
            lof_model.fit_predict(X)
        )

        # DBSCAN
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        dbscan_model = DBSCAN(
            eps=0.8,
            min_samples=10
        )

        dbscan_predictions = (
            dbscan_model.fit_predict(X_scaled)
        )

        dbscan_predictions = [
            -1 if label == -1 else 1
            for label in dbscan_predictions
        ]

        # Count anomalies
        isolation_count = (
            isolation_predictions == -1
        ).sum()

        lof_count = (
            lof_predictions == -1
        ).sum()

        dbscan_count = (
            pd.Series(dbscan_predictions) == -1
        ).sum()

        # Comparison DataFrame
        comparison = pd.DataFrame({
            "Algorithm": [
                "Isolation Forest",
                "Local Outlier Factor",
                "DBSCAN"
            ],
            "Anomalies Detected": [
                isolation_count,
                lof_count,
                dbscan_count
            ]
        })

        comparison["Anomaly Percentage"] = (
            comparison["Anomalies Detected"]
            / len(df)
            * 100
        )

        # Display comparison
        st.subheader("🤖 Algorithm Comparison")

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        # Comparison chart
        fig = px.bar(
            comparison,
            x="Algorithm",
            y="Anomalies Detected",
            text="Anomalies Detected",
            title="Anomalies Detected by Algorithm"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Algorithm agreement
        agreement = pd.DataFrame({
            "Isolation Forest": isolation_predictions == -1,
            "Local Outlier Factor": lof_predictions == -1,
            "DBSCAN": (
                pd.Series(dbscan_predictions).values == -1
            )
        })

        agreement["Algorithms Agree"] = (
            agreement.sum(axis=1)
        )

        st.subheader("🔎 Algorithm Agreement")

        agreement_counts = (
            agreement["Algorithms Agree"]
            .value_counts()
            .sort_index()
        )

        agreement_chart = pd.DataFrame({
            "Number of Algorithms": agreement_counts.index,
            "Number of Records": agreement_counts.values
        })

        fig_agreement = px.bar(
            agreement_chart,
            x="Number of Algorithms",
            y="Number of Records",
            text="Number of Records",
            title="How Many Algorithms Flagged Each Record?"
        )

        fig_agreement.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_agreement,
            use_container_width=True
        )