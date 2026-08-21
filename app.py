import pandas as pd
import streamlit as st

from src.anomaly_detection import compare_algorithms, detect_anomalies, prepare_features
from src.data_processing import (
    get_dataset_summary,
    get_default_feature_columns,
    get_model_feature_columns,
    is_identifier_column,
    load_dataset,
    preview_dataset,
)
from src.evaluation import evaluate_comparison, evaluate_predictions, get_ground_truth
from src.scoring import add_severity_labels, get_top_suspicious, normalize_scores
from src.ui_components import (
    apply_dashboard_styles,
    render_analysis_metrics,
    render_comparison_metrics,
    render_dataset_metrics,
    render_detection_summary,
    render_evaluation_metrics,
    render_header,
)
from src.visualization import (
    create_agreement_chart,
    create_algorithm_comparison,
    create_anomaly_distribution,
    create_anomaly_scatter,
    create_confusion_matrix,
)


st.set_page_config(
    page_title="AnomalyLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dashboard_styles()
render_header()


# ==================================================
# SIDEBAR — DATASET
# ==================================================

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


# ==================================================
# EMPTY STATE
# ==================================================

if uploaded_file is None:
    st.info("👈 Upload a CSV or Excel dataset from the sidebar to begin.")
    feature_col1, feature_col2, feature_col3 = st.columns(3)

    cards = [
        (
            feature_col1,
            "🤖",
            "Multiple ML Models",
            "Compare Isolation Forest, Local Outlier Factor, and DBSCAN to identify unusual patterns from different perspectives.",
            "rgba(86,110,255,.22)",
        ),
        (
            feature_col2,
            "📊",
            "Interactive Analysis",
            "Explore model results through interactive visualizations, metrics, distributions, and ranked anomaly records.",
            "rgba(124,78,255,.22)",
        ),
        (
            feature_col3,
            "🔎",
            "Anomaly Investigation",
            "Prioritize suspicious records, investigate model agreement, evaluate model quality, and export results.",
            "rgba(49,211,159,.22)",
        ),
    ]

    for col, icon, title, text, border in cards:
        with col:
            st.markdown(
                f"""
<div style="background:linear-gradient(145deg,rgba(31,42,76,.95),rgba(20,29,52,.95));border:1px solid {border};border-radius:16px;padding:22px;min-height:165px;box-shadow:0 10px 30px rgba(0,0,0,.16);">
    <div style="font-size:1.6rem;">{icon}</div>
    <div style="font-size:1.05rem;font-weight:700;margin-top:10px;color:#f4f6ff;">{title}</div>
    <div style="margin-top:8px;color:#aeb9d6;line-height:1.6;">{text}</div>
</div>
                """,
                unsafe_allow_html=True,
            )
    st.stop()


# ==================================================
# LOAD DATASET
# ==================================================

try:
    df = load_dataset(uploaded_file)
except Exception as exc:
    st.error(f"Could not read the dataset: {exc}")
    st.stop()

summary = get_dataset_summary(df)
feature_columns = get_model_feature_columns(df)
default_features = get_default_feature_columns(df)
ground_truth, ground_truth_source = get_ground_truth(df)

if len(feature_columns) < 2:
    st.error("This dataset needs at least two numerical feature columns for anomaly detection.")
    st.stop()


# ==================================================
# SIDEBAR — DETECTION SETTINGS
# ==================================================

with st.sidebar:
    st.divider()
    st.markdown("### ⚙️ Detection Settings")

    selected_columns = st.multiselect(
        "Features",
        feature_columns,
        default=default_features,
        help=(
            "Choose the numerical features used by the models. Identifier-like "
            "columns remain available but are excluded from the default selection."
        ),
    )

    skipped_identifiers = [
        column for column in feature_columns if is_identifier_column(column)
    ]
    if skipped_identifiers:
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
            "Used by Isolation Forest and Local Outlier Factor to estimate the expected proportion of anomalous records."
        ),
    )

    st.caption(f"Expected anomalies: {contamination * 100:.0f}%")

    if ground_truth is not None:
        st.success("Evaluation labels detected")
    else:
        st.caption("No ground-truth labels detected — evaluation metrics will stay hidden.")

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


# Persist an analysis until model settings change. This allows chart axis controls
# to rerun Streamlit without making the user press Run Analysis again.
settings_signature = (
    uploaded_file.name,
    tuple(selected_columns),
    detection_mode,
    algorithm,
    float(contamination),
)

if run_detection:
    st.session_state["analysis_signature"] = settings_signature

analysis_active = (
    valid_feature_selection
    and st.session_state.get("analysis_signature") == settings_signature
)


# ==================================================
# DATASET OVERVIEW
# ==================================================

st.success(
    f"Dataset loaded successfully — {summary['rows']:,} rows × {summary['columns']} columns"
)
st.subheader("📋 Dataset Overview")
render_dataset_metrics(summary)

(
    overview_tab,
    visualization_tab,
    comparison_tab,
    suspicious_tab,
    evaluation_tab,
) = st.tabs(
    [
        "📊 Overview",
        "📈 Visualization",
        "🤖 Comparison",
        "🔥 Suspicious Records",
        "🎯 Evaluation",
    ]
)

with overview_tab:
    st.markdown("### Dataset Preview")
    st.dataframe(preview_dataset(df), use_container_width=True, hide_index=True)
    if not analysis_active:
        st.info("Configure the detection settings in the sidebar and click **Run Analysis**.")

with visualization_tab:
    if not analysis_active:
        st.info("Run anomaly detection to view interactive anomaly visualizations.")

with comparison_tab:
    if not analysis_active:
        st.info("Select **Compare All Algorithms** and run the analysis to compare model results.")

with suspicious_tab:
    if not analysis_active:
        st.info("Run anomaly detection to investigate suspicious records.")

with evaluation_tab:
    if not analysis_active:
        st.info("Run anomaly detection to evaluate model performance when labels are available.")


# ==================================================
# RUN ANALYSIS
# ==================================================

if analysis_active:
    X = prepare_features(df, selected_columns)

    # ==============================================
    # SINGLE ALGORITHM MODE
    # ==============================================
    if detection_mode == "Single Algorithm":
        predictions, raw_scores = detect_anomalies(X, algorithm, contamination)
        anomaly_scores = normalize_scores(raw_scores) if raw_scores is not None else None

        results = df.copy()
        results["Anomaly"] = predictions

        if anomaly_scores is not None:
            results["Anomaly Score"] = anomaly_scores.values

        results["Anomaly"] = results["Anomaly"].map({1: "Normal", -1: "Anomaly"})
        results = add_severity_labels(results)

        anomaly_count = int((results["Anomaly"] == "Anomaly").sum())
        normal_count = int((results["Anomaly"] == "Normal").sum())
        anomaly_percentage = anomaly_count / len(results) * 100

        with overview_tab:
            st.markdown("## Analysis Overview")
            render_analysis_metrics(
                len(results),
                normal_count,
                anomaly_count,
                anomaly_percentage,
            )
            st.divider()

            chart_col, summary_col = st.columns([2, 1])
            with chart_col:
                distribution_fig = create_anomaly_distribution(results)
                st.plotly_chart(distribution_fig, use_container_width=True)
            with summary_col:
                render_detection_summary(
                    algorithm,
                    len(selected_columns),
                    contamination * 100,
                    anomaly_percentage,
                    anomaly_count,
                )

        with visualization_tab:
            st.markdown("## Anomaly Visualization")
            st.caption("Choose any two selected features and inspect records interactively.")

            axis_col1, axis_col2 = st.columns(2)
            with axis_col1:
                x_column = st.selectbox(
                    "X-axis",
                    selected_columns,
                    index=0,
                    key="single_x_axis",
                )
            with axis_col2:
                default_y_index = 1 if len(selected_columns) > 1 else 0
                y_column = st.selectbox(
                    "Y-axis",
                    selected_columns,
                    index=default_y_index,
                    key="single_y_axis",
                )

            if x_column == y_column:
                st.warning("Choose two different features for the clearest scatter plot.")

            fig = create_anomaly_scatter(results, x_column, y_column, algorithm)
            st.plotly_chart(fig, use_container_width=True)

        with comparison_tab:
            st.info(
                "You are currently using **Single Algorithm** mode. Select **Compare All Algorithms** from the sidebar to view model comparison."
            )

        with suspicious_tab:
            if "Anomaly Score" in results.columns:
                st.markdown("## 🔥 Most Suspicious Records")
                st.caption(
                    "Only detected anomalies are ranked. Higher scores indicate more unusual observations."
                )
                top_suspicious = get_top_suspicious(results, limit=10)

                column_config = {
                    "Anomaly Score": st.column_config.ProgressColumn(
                        "Anomaly Score",
                        help="Normalized anomaly score from 0 to 100",
                        min_value=0,
                        max_value=100,
                        format="%.1f",
                    ),
                    "Severity": st.column_config.TextColumn(
                        "Severity",
                        help="Score-based investigation priority",
                    ),
                }
                st.dataframe(
                    top_suspicious,
                    use_container_width=True,
                    hide_index=True,
                    column_config=column_config,
                )
                st.divider()
            else:
                st.info(
                    "DBSCAN does not currently provide a normalized anomaly score, so score-based severity is unavailable."
                )

            st.markdown("## 🔎 All Detected Anomalies")
            anomalies = results[results["Anomaly"] == "Anomaly"].copy()
            if "Anomaly Score" in anomalies.columns:
                anomalies = anomalies.sort_values("Anomaly Score", ascending=False)

            st.caption(f"{len(anomalies):,} anomalous records detected using {algorithm}.")
            st.dataframe(
                anomalies,
                use_container_width=True,
                hide_index=True,
                column_config=(
                    {
                        "Anomaly Score": st.column_config.ProgressColumn(
                            "Anomaly Score",
                            min_value=0,
                            max_value=100,
                            format="%.1f",
                        )
                    }
                    if "Anomaly Score" in anomalies.columns
                    else None
                ),
            )
            st.divider()

            st.download_button(
                "⬇️ Download Full Analysis",
                data=results.to_csv(index=False),
                file_name="anomalylens_results.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with evaluation_tab:
            st.markdown("## 🎯 Model Evaluation")

            if ground_truth is None:
                st.info(
                    "This dataset does not contain recognized ground-truth anomaly labels. Evaluation is shown only when labels are available."
                )
            else:
                metrics = evaluate_predictions(predictions, ground_truth)
                st.caption(f"Ground truth source: {ground_truth_source}")
                render_evaluation_metrics(metrics)
                st.divider()

                chart_col, detail_col = st.columns([1.5, 1])
                with chart_col:
                    confusion_fig = create_confusion_matrix(metrics, algorithm)
                    st.plotly_chart(confusion_fig, use_container_width=True)
                with detail_col:
                    st.markdown("### Classification Details")
                    st.metric("True Positives", metrics["true_positives"])
                    st.metric("False Positives", metrics["false_positives"])
                    st.metric("False Negatives", metrics["false_negatives"])
                    st.caption(
                        "Precision measures how many flagged records were truly anomalous. Recall measures how many true anomalies were successfully found."
                    )

    # ==============================================
    # COMPARE ALL ALGORITHMS MODE
    # ==============================================
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
            render_comparison_metrics(
                isolation_count,
                lof_count,
                dbscan_count,
                all_three_count,
            )
            st.divider()
            st.markdown("### Analysis Summary")
            summary_col1, summary_col2 = st.columns(2)
            summary_col1.metric("Flagged by at least 2 models", f"{at_least_two_count:,}")
            summary_col2.metric("Flagged by all 3 models", f"{all_three_count:,}")
            st.caption(
                "Different algorithms identify different anomaly structures. Multi-model agreement is useful for prioritizing records for investigation."
            )

        with visualization_tab:
            st.info(
                "Comparison mode focuses on model-level agreement. Switch to Single Algorithm mode for an interactive feature scatter plot."
            )

        with comparison_tab:
            st.markdown("## 🤖 Algorithm Comparison")
            st.caption("Compare detection volume and model agreement across all three algorithms.")

            display_comparison = comparison.copy()
            display_comparison["Anomaly Percentage"] = display_comparison[
                "Anomaly Percentage"
            ].map(lambda value: f"{value:.2f}%")
            st.dataframe(display_comparison, use_container_width=True, hide_index=True)

            comparison_fig = create_algorithm_comparison(comparison)
            st.plotly_chart(comparison_fig, use_container_width=True)
            st.divider()

            agreement_counts = agreement["Algorithms Agree"].value_counts().sort_index()
            agreement_chart = pd.DataFrame(
                {
                    "Algorithms Flagging Record": agreement_counts.index,
                    "Number of Records": agreement_counts.values,
                }
            )
            agreement_fig = create_agreement_chart(agreement_chart)
            st.plotly_chart(agreement_fig, use_container_width=True)
            st.caption(
                "A value of 3 means Isolation Forest, Local Outlier Factor, and DBSCAN all flagged the same record."
            )

        with suspicious_tab:
            st.markdown("## 🔥 Consensus Anomalies")
            st.caption("Records flagged by multiple algorithms are prioritized for investigation.")

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
            consensus_results["Consensus Level"] = consensus_results[
                "Algorithms Agree"
            ].map({3: "High Consensus", 2: "Moderate Consensus", 1: "Low Consensus", 0: "None"})

            consensus_anomalies = consensus_results[
                consensus_results["Algorithms Agree"] >= 2
            ].sort_values("Algorithms Agree", ascending=False)

            st.dataframe(
                consensus_anomalies,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Algorithms Agree": st.column_config.ProgressColumn(
                        "Algorithms Agree",
                        min_value=0,
                        max_value=3,
                        format="%d",
                    )
                },
            )
            st.divider()
            st.download_button(
                "⬇️ Download Comparison Results",
                data=consensus_results.to_csv(index=False),
                file_name="anomalylens_model_comparison.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with evaluation_tab:
            st.markdown("## 🎯 Multi-Model Evaluation")

            if ground_truth is None:
                st.info(
                    "This dataset does not contain recognized ground-truth anomaly labels. Evaluation is shown only when labels are available."
                )
            else:
                evaluation = evaluate_comparison(comparison_predictions, ground_truth)
                st.caption(f"Ground truth source: {ground_truth_source}")

                best_row = evaluation.loc[evaluation["F1 Score"].idxmax()]
                st.success(
                    f"Best F1 score: **{best_row['Algorithm']}** at **{best_row['F1 Score']:.1%}**"
                )

                display_evaluation = evaluation.copy()
                for column in ["Precision", "Recall", "F1 Score", "Accuracy"]:
                    display_evaluation[column] = display_evaluation[column].map(
                        lambda value: f"{value:.1%}"
                    )

                st.dataframe(display_evaluation, use_container_width=True, hide_index=True)
                st.caption(
                    "Use these metrics only when ground-truth labels are trustworthy. Unsupervised anomaly detection is often used on unlabeled datasets, where these metrics are unavailable."
                )
