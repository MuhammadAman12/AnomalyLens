import plotly.express as px
import pandas as pd


def create_anomaly_scatter(
    results,
    x_column,
    y_column,
    algorithm
):
    """
    Create a 2D scatter plot showing normal
    and anomalous observations.
    """

    fig = px.scatter(
        results,
        x=x_column,
        y=y_column,
        color="Anomaly",
        hover_data=[
            column
            for column in results.columns
            if column not in ["Anomaly"]
        ],
        title=(
            f"{algorithm}: "
            f"{x_column} vs {y_column}"
        )
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        legend_title_text="Status"
    )

    return fig


def create_algorithm_comparison(
    comparison
):
    """
    Create a bar chart comparing the number
    of anomalies detected by each algorithm.
    """

    fig = px.bar(
        comparison,
        x="Algorithm",
        y="Anomalies Detected",
        text="Anomalies Detected",
        title="Algorithm Anomaly Comparison"
    )

    fig.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis_title="Algorithm",
        yaxis_title="Anomalies Detected"
    )

    fig.update_traces(
        textposition="outside"
    )

    return fig


def create_anomaly_distribution(
    results
):
    """
    Create a chart showing normal vs anomalous
    observations.
    """

    distribution = (
        results["Anomaly"]
        .value_counts()
        .reset_index()
    )

    distribution.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        distribution,
        names="Status",
        values="Count",
        hole=0.55,
        title="Anomaly Distribution"
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig