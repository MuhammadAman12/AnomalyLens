import streamlit as st
import pandas as pd

from src.anomaly_detection import (
    prepare_features,
    detect_anomalies,
    compare_algorithms,
)
from src.scoring import normalize_scores, get_top_suspicious
from src.visualization import (
    create_anomaly_scatter,
    create_algorithm_comparison,
    create_anomaly_distribution,
)
from src.data_processing import (
    load_dataset,
    get_numeric_columns,
    get_default_feature_columns,
    get_dataset_summary,
    preview_dataset,
)
from src.ui_components import (
    apply_dashboard_styles,
    render_header,
    render_dataset_metrics,
)

st.set_page_config(
    page_title="AnomalyLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dashboard_styles()
render_header()

with st.sidebar:
    st.markdown("## 🔍 AnomalyLens")
    st.caption("Configure your dataset and anomaly detection settings.")
    st.divider()
    st.markdown("### 📂 Dataset")
    uploaded_file = st.file_uploader(
        "Upload dataset",
        type=["csv", "xlsx"],
        help="Upload a CSV or Excel dataset for analysis.",
    )

if uploaded_file is None:
    st.info("👈 Upload a CSV or Excel dataset from the sidebar to begin.")

    feature_col1, feature_col2, feature_col3 = st.columns(3)

    with feature_col1:
        st.markdown(
            """
<div style="background:linear-gradient(145deg,rgba(31,42,76,.95),rgba(20,29,52,.95));border:1px solid rgba(86,110,255,.22);border-radius:16px;padding:22px;min-height:165px;box-shadow:0 10px 30px rgba(0,0,0,.16);">
    <div style="font-size:1.6rem;">🤖</div>
    <div style="font-size:1.05rem;font-weight:700;margin-top:10px;color:#f4f6ff;">Multiple ML Models</div>
    <div style="margin-top:8px;color:#aeb9d6;line-height:1.6;">Compare Isolation Forest, Local Outlier Factor, and DBSCAN to identify unusual patterns from different perspectives.</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    with feature_col2:
        st.markdown(
            """
<div style="background:linear-gradient(145deg,rgba(31,42,76,.95),rgba(20,29,52,.95));border:1px solid rgba(124,78,255,.22);border-radius:16px;padding:22px;min-height:165px;box-shadow:0 10px 30px rgba(0,0,0,.16);">
    <div style="font-size:1.6rem;">📊</div>
    <div style="font-size:1.05rem;font-weight:700;margin-top:10px;color:#f4f6ff;">Interactive Analysis</div>
    <div style="margin-top:8px;color:#aeb9d6;line-height:1.6;">Explore model results through interactive visualizations, metrics, distributions, and ranked anomaly records.</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    with feature_col3:
        st.markdown(
            """
<div style="background:linear-gradient(145deg,rgba(31,42,76,.95),rgba(20,29,52,.95));border:1px solid rgba(49,211,159,.22);border-radius:16px;padding:22px;min-height:165px;box-shadow:0 10px 30px rgba(0,0,0,.16);">
    <div style="font-size:1.6rem;">🔎</div>
    <div style="font-size:1.05rem;font-weight:700;margin-top:10px;color:#f4f6ff;">Anomaly Investigation</div>
    <div style="margin-top:8px;color:#aeb9d6;line-height:1.6;">Prioritize suspicious records, investigate model agreement, and export results for deeper analysis.</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()

try:
    df = load_dataset(uploaded_file)
except Exception as e:
    st.error(f"Could not read the dataset: {e}")
    st.stop()

summary = get_dataset_summary(df)
numeric_columns = get_numeric_columns(df)
default_features = get_default_feature_columns(df)

if len(numeric_columns) < 2:
    st.error("This dataset needs at least two numerical columns for anomaly detection.")
    st.stop()

with st.sidebar:
    st.divider()
    st.markdown("### ⚙️ Detection Settings")

    selected_columns = st.multiselect(
        "Features",
        numeric_columns,
        default=default_features,
        help=(
            "Choose the numerical features used by the models. "
            "Identifier-like columns remain available but are excluded from the default selection."
        ),
    )

    identifier_defaults_skipped = [
        column for column in numeric_columns if column not in default_features
    ]
    if identifier_defaults_skipped:
        st.caption(
            "ℹ️ Identifier-like numeric columns are not selected by default because they usually do not describe behavioural patterns."
        )

    detection_mode = st.radio(
        "Detection Mode",
        ["Single Algorithm", "Compare All Algorithms"],
    )

    if detection_mode == "Single Algorithm":
        algorithm = st.selectbox(
            "Algorithm",
            ["Isolation Forest", "Local Outlier Factor", "DBSCAN"],
        )
    else:
        algorithm = None

    contamination = st.slider(
        "Expected anomaly rate",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01,
        help=(
            "Used by Isolation Forest and Local Outlier Factor to estimate "
            "the expected proportion of anomalous records."
        ),
    )

    st.caption(f"Expected anomalies: {contamination * 100:.0f}%")
    st.divider()

    valid_feature_selection = len(selected_columns) >= 2

    if not valid_feature_selection:
        st.warning("Select at least two numerical features.")

    run_detection = st.button(
        "🔍 Run Analysis",
        type="primary",
        use_container_width=True,
        disabled=not valid_feature_selection,
    )

    st.divider()
    st.caption(f"Dataset: {uploaded_file.name}")
    st.caption(f"{summary['rows']:,} rows • {summary['columns']} columns")

st.success(
    f"Dataset loaded successfully — {summary['rows']:,} rows × {summary['columns']} columns"
)

st.subheader("📋 Dataset Overview")
render_dataset_metrics(summary)

overview_tab, visualization_tab, comparison_tab, suspicious_tab = st.tabs(
    ["📊 Overview", "📈 Visualization", "🤖 Comparison", "🔥 Suspicious Records"]
)

with overview_tab:
    st.markdown("### Dataset Preview")
    st.dataframe(preview_dataset(df), use_container_width=True, hide_index=True)
    if not run_detection:
        st.info("Configure the detection settings in the sidebar and click **Run Analysis**.")

with visualization_tab:
    if not run_detection:
        st.info("Run anomaly detection to view interactive anomaly visualizations.")

with comparison_tab:
    if not run_detection:
        st.info("Select **Compare All Algorithms** and run the analysis to compare model results.")

with suspicious_tab:
    if not run_detection:
        st.info("Run a single anomaly detection model to investigate suspicious records.")

if run_detection:
    X = prepare_features(df, selected_columns)

    if detection_mode == "Single Algorithm":
        predictions, raw_scores = detect_anomalies(X, algorithm, contamination)

        if raw_scores is not None:
            anomaly_scores = normalize_scores(raw_scores)
        else:
            anomaly_scores = None

        results = df.copy()
        results["Anomaly"] = predictions

        if anomaly_scores is not None:
            results["Anomaly Score"] = anomaly_scores.values

        results["Anomaly"] = results["Anomaly"].map({1: "Normal", -1: "Anomaly"})

        anomaly_count = int((results["Anomaly"] == "Anomaly").sum())
        normal_count = int((results["Anomaly"] == "Normal").sum())
        anomaly_percentage = anomaly_count / len(results) * 100

        with overview_tab:
            st.markdown("## Analysis Overview")
            metric1, metric2, metric3, metric4 = st.columns(4)
            metric1.metric("Records Analyzed", f"{len(results):,}")
            metric2.metric("Normal Records", f"{normal_count:,}")
            metric3.metric("Anomalies Detected", f"{anomaly_count:,}")
            metric4.metric("Anomaly Rate", f"{anomaly_percentage:.1f}%")

            st.divider()
            chart_col, summary_col = st.columns([2, 1])

            with chart_col:
                distribution_fig = create_anomaly_distribution(results)
                st.plotly_chart(distribution_fig, use_container_width=True)

            with summary_col:
                st.markdown("### Detection Summary")
                st.markdown(f"**Algorithm**  \n{algorithm}")
                st.markdown(f"**Features analyzed**  \n{len(selected_columns)}")
                st.markdown(f"**Expected anomaly rate**  \n{contamination * 100:.0f}%")
                st.markdown(f"**Detected anomaly rate**  \n{anomaly_percentage:.1f}%")
                st.markdown(f"**Anomalies detected**  \n{anomaly_count:,}")

        with visualization_tab:
            st.markdown("## Anomaly Visualization")
            st.caption("Use the chart controls to zoom, pan, and inspect individual records.")
            fig = create_anomaly_scatter(
                results,
                selected_columns[0],
                selected_columns[1],
                algorithm,
            )
            st.plotly_chart(fig, use_container_width=True)

        with comparison_tab:
            st.info(
                "You are currently using **Single Algorithm** mode. "
                "Select **Compare All Algorithms** from the sidebar to view model comparison."
            )

        with suspicious_tab:
            if "Anomaly Score" in results.columns:
                st.markdown("## 🔥 Most Suspicious Records")
                st.caption(
                    "Records are ranked by anomaly score. Higher scores indicate more unusual observations."
                )
                top_suspicious = get_top_suspicious(results, limit=10)
                st.dataframe(top_suspicious, use_container_width=True, hide_index=True)
                st.divider()
            else:
                st.info(
                    "DBSCAN does not currently provide a normalized anomaly score. "
                    "DBSCAN scoring will be added in a future update."
                )

            st.markdown("## 🔎 All Detected Anomalies")
            anomalies = results[results["Anomaly"] == "Anomaly"]
            st.caption(f"{len(anomalies):,} anomalous records detected using {algorithm}.")
            st.dataframe(anomalies, use_container_width=True, hide_index=True)
            st.divider()

            csv = results.to_csv(index=False)
            st.download_button(
                "⬇️ Download Full Analysis",
                data=csv,
                file_name="anomalylens_results.csv",
                mime="text/csv",
                use_container_width=True,
            )

    else:
        comparison_predictions = compare_algorithms(X, contamination)

        isolation_count = int((comparison_predictions["Isolation Forest"] == -1).sum())
        lof_count = int((comparison_predictions["Local Outlier Factor"] == -1).sum())
        dbscan_count = int((comparison_predictions["DBSCAN"] == -1).sum())

        comparison = pd.DataFrame(
            {
                "Algorithm": ["Isolation Forest", "Local Outlier Factor", "DBSCAN"],
                "Anomalies Detected": [isolation_count, lof_count, dbscan_count],
            }
        )
        comparison["Anomaly Percentage"] = (
            comparison["Anomalies Detected"] / len(df) * 100
        ).round(2)

        agreement = pd.DataFrame(
            {
                "Isolation Forest": comparison_predictions["Isolation Forest"] == -1,
                "Local Outlier Factor": comparison_predictions["Local Outlier Factor"] == -1,
                "DBSCAN": comparison_predictions["DBSCAN"] == -1,
            }
        )
        agreement["Algorithms Agree"] = agreement.sum(axis=1)

        all_three_count = int((agreement["Algorithms Agree"] == 3).sum())
        at_least_two_count = int((agreement["Algorithms Agree"] >= 2).sum())

        with overview_tab:
            st.markdown("## Multi-Model Overview")
            metric1, metric2, metric3, metric4 = st.columns(4)
            metric1.metric("Isolation Forest", f"{isolation_count:,}")
            metric2.metric("Local Outlier Factor", f"{lof_count:,}")
            metric3.metric("DBSCAN", f"{dbscan_count:,}")
            metric4.metric("3-Model Consensus", f"{all_three_count:,}")

            st.divider()
            st.markdown("### Analysis Summary")
            st.write(f"**{at_least_two_count:,} records** were flagged by at least two algorithms.")
            st.write(f"**{all_three_count:,} records** were flagged by all three algorithms.")
            st.caption(
                "Different algorithms may detect different patterns because they use different definitions of anomalous behavior."
            )

        with visualization_tab:
            st.info(
                "Individual anomaly maps are available in Single Algorithm mode. "
                "Comparison mode focuses on model-level agreement and detection differences."
            )

        with comparison_tab:
            st.markdown("## 🤖 Algorithm Comparison")
            st.caption(
                "Compare the number and percentage of records identified as anomalous by each model."
            )
            st.dataframe(comparison, use_container_width=True, hide_index=True)
            st.divider()

            comparison_fig = create_algorithm_comparison(comparison)
            st.plotly_chart(comparison_fig, use_container_width=True)

            st.divider()
            st.markdown("## 🔎 Algorithm Agreement")
            agreement_counts = agreement["Algorithms Agree"].value_counts().sort_index()
            agreement_chart = pd.DataFrame(
                {
                    "Algorithms Flagging Record": agreement_counts.index,
                    "Number of Records": agreement_counts.values,
                }
            )
            st.bar_chart(
                agreement_chart,
                x="Algorithms Flagging Record",
                y="Number of Records",
                use_container_width=True,
            )
            st.caption(
                "A value of 3 means that Isolation Forest, Local Outlier Factor, and DBSCAN all flagged the same record."
            )

        with suspicious_tab:
            st.markdown("## 🔥 Consensus Anomalies")
            st.caption(
                "Records flagged by multiple algorithms can be useful candidates for investigation."
            )

            consensus_results = df.copy()
            consensus_results["Isolation Forest"] = agreement["Isolation Forest"].map(
                {True: "Anomaly", False: "Normal"}
            )
            consensus_results["Local Outlier Factor"] = agreement[
                "Local Outlier Factor"
            ].map({True: "Anomaly", False: "Normal"})
            consensus_results["DBSCAN"] = agreement["DBSCAN"].map(
                {True: "Anomaly", False: "Normal"}
            )
            consensus_results["Algorithms Agree"] = agreement["Algorithms Agree"]

            consensus_anomalies = consensus_results[
                consensus_results["Algorithms Agree"] >= 2
            ].sort_values("Algorithms Agree", ascending=False)

            st.dataframe(consensus_anomalies, use_container_width=True, hide_index=True)
            st.divider()

            consensus_csv = consensus_results.to_csv(index=False)
            st.download_button(
                "⬇️ Download Comparison Results",
                data=consensus_csv,
                file_name="anomalylens_model_comparison.csv",
                mime="text/csv",
                use_container_width=True,
            )
