BACKGROUND = "rgba(0,0,0,0)"
TEXT = "#E7ECFF"
MUTED_TEXT = "#98A6C7"
GRID = "rgba(122, 139, 190, 0.16)"
BORDER = "rgba(112, 130, 255, 0.18)"

NORMAL_COLOR = "#2DD4BF"
ANOMALY_COLOR = "#FB7185"

MODEL_COLORS = {
    "Isolation Forest": "#5B7CFA",
    "Local Outlier Factor": "#A78BFA",
    "DBSCAN": "#22D3EE",
}


def apply_chart_theme(fig, height=None):
    """Apply the shared AnomalyLens dark analytics theme."""

    fig.update_layout(
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        font=dict(color=TEXT, family="Inter, Segoe UI, Arial, sans-serif"),
        title=dict(font=dict(size=20, color=TEXT), x=0.02, xanchor="left"),
        margin=dict(l=28, r=28, t=72, b=34),
        hoverlabel=dict(
            bgcolor="#151E35",
            bordercolor="#5365D8",
            font=dict(color="#F7F9FF"),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED_TEXT)),
    )

    if height is not None:
        fig.update_layout(height=height)

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(color=MUTED_TEXT),
        title_font=dict(color=MUTED_TEXT),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(color=MUTED_TEXT),
        title_font=dict(color=MUTED_TEXT),
    )

    return fig


def create_anomaly_scatter(results, x_column, y_column, algorithm):
    """Create a polished scatter plot of normal and anomalous records."""

    import plotly.express as px

    fig = px.scatter(
        results,
        x=x_column,
        y=y_column,
        color="Anomaly",
        color_discrete_map={"Normal": NORMAL_COLOR, "Anomaly": ANOMALY_COLOR},
        category_orders={"Anomaly": ["Normal", "Anomaly"]},
        hover_data=[column for column in results.columns if column != "Anomaly"],
        title=f"{algorithm}: {x_column} vs {y_column}",
    )

    apply_chart_theme(fig, height=520)
    fig.update_layout(
        legend_title_text="Record Status",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    for trace in fig.data:
        if trace.name == "Anomaly":
            trace.update(
                marker=dict(
                    size=10,
                    opacity=0.94,
                    symbol="diamond",
                    line=dict(width=1.2, color="#FFD0D8"),
                )
            )
        else:
            trace.update(marker=dict(size=7, opacity=0.62, line=dict(width=0)))

    return fig


def create_algorithm_comparison(comparison):
    """Create a polished bar chart comparing anomaly counts by model."""

    import plotly.express as px

    fig = px.bar(
        comparison,
        x="Algorithm",
        y="Anomalies Detected",
        color="Algorithm",
        color_discrete_map=MODEL_COLORS,
        text="Anomalies Detected",
        title="Algorithm Anomaly Comparison",
    )

    apply_chart_theme(fig, height=460)
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Anomalies Detected",
        bargap=0.38,
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(color=TEXT, size=13),
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Anomalies detected: %{y}<extra></extra>",
    )

    return fig


def create_agreement_chart(agreement_chart):
    """Create a themed chart showing how many models flag each record."""

    import plotly.graph_objects as go

    color_map = {
        0: "#334155",
        1: "#5B7CFA",
        2: "#F59E0B",
        3: "#FB7185",
    }

    fig = go.Figure()
    fig.add_bar(
        x=agreement_chart["Algorithms Flagging Record"],
        y=agreement_chart["Number of Records"],
        marker=dict(
            color=[
                color_map.get(int(value), "#5B7CFA")
                for value in agreement_chart["Algorithms Flagging Record"]
            ],
            line=dict(width=0),
        ),
        text=agreement_chart["Number of Records"],
        textposition="outside",
        hovertemplate=(
            "<b>%{x} model(s) flagged record</b><br>"
            "Records: %{y}<extra></extra>"
        ),
    )

    fig.update_layout(
        title="Model Agreement Distribution",
        xaxis_title="Algorithms Flagging Record",
        yaxis_title="Number of Records",
        bargap=0.35,
    )
    apply_chart_theme(fig, height=430)

    return fig


def create_anomaly_distribution(results):
    """Create a donut chart showing normal vs anomalous records."""

    import plotly.express as px

    distribution = results["Anomaly"].value_counts().reset_index()
    distribution.columns = ["Status", "Count"]

    anomaly_count = int(
        distribution.loc[distribution["Status"] == "Anomaly", "Count"].sum()
    )
    total = int(distribution["Count"].sum())
    anomaly_rate = anomaly_count / total * 100 if total else 0

    fig = px.pie(
        distribution,
        names="Status",
        values="Count",
        hole=0.66,
        color="Status",
        color_discrete_map={"Normal": NORMAL_COLOR, "Anomaly": ANOMALY_COLOR},
        category_orders={"Status": ["Normal", "Anomaly"]},
        title="Anomaly Distribution",
    )

    apply_chart_theme(fig, height=410)
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(color="#F7F9FF", size=13),
        marker=dict(line=dict(color="#0B1020", width=3)),
        hovertemplate=(
            "<b>%{label}</b><br>Records: %{value}<br>"
            "Share: %{percent}<extra></extra>"
        ),
    )
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text=(
                    f"<b>{anomaly_count:,}</b>"
                    f"<br><span style='font-size:12px'>{anomaly_rate:.1f}% anomalies</span>"
                ),
                x=0.5,
                y=0.5,
                font=dict(size=22, color=TEXT),
                showarrow=False,
                align="center",
            )
        ],
    )

    return fig


def create_confusion_matrix(metrics, algorithm):
    """Create a compact confusion-matrix heatmap from evaluation metrics."""

    import plotly.graph_objects as go

    matrix = [
        [metrics["true_negatives"], metrics["false_positives"]],
        [metrics["false_negatives"], metrics["true_positives"]],
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=["Predicted Normal", "Predicted Anomaly"],
            y=["Actual Normal", "Actual Anomaly"],
            colorscale=[
                [0.0, "#111827"],
                [0.45, "#334155"],
                [1.0, "#5B7CFA"],
            ],
            showscale=False,
            text=matrix,
            texttemplate="%{text}",
            textfont=dict(color="#F8FAFC", size=17),
            hovertemplate="%{y}<br>%{x}<br>Records: %{z}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{algorithm} Confusion Matrix",
        xaxis_title=None,
        yaxis_title=None,
    )
    apply_chart_theme(fig, height=390)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_xaxes(showgrid=False)

    return fig
