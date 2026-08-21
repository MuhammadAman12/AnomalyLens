import streamlit as st


ACCENTS = {
    "blue": ("#5B7CFA", "rgba(91,124,250,.18)"),
    "green": ("#2DD4BF", "rgba(45,212,191,.16)"),
    "red": ("#FB7185", "rgba(251,113,133,.16)"),
    "orange": ("#F59E0B", "rgba(245,158,11,.16)"),
    "purple": ("#A78BFA", "rgba(167,139,250,.16)"),
    "cyan": ("#22D3EE", "rgba(34,211,238,.16)"),
}


def apply_dashboard_styles():
    """Apply the main AnomalyLens visual theme."""

    st.markdown(
        """
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(68,89,255,.14), transparent 30%),
        radial-gradient(circle at top right, rgba(138,43,226,.10), transparent 25%),
        #0b1020;
    color:#eaf0ff;
}
.block-container { padding-top:1.7rem; padding-bottom:3rem; max-width:1500px; }
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#10172a 0%,#0d1322 100%);
    border-right:1px solid rgba(120,140,255,.18);
}
section[data-testid="stSidebar"] .block-container { padding-top:1.7rem; }
h1,h2,h3 { color:#f5f7ff; letter-spacing:-.025em; }
h1 { font-weight:800; } h2 { font-weight:720; } h3 { font-weight:680; }
p { color:#b7c1d9; }
small { color:#8694b3; }
hr { border-color:rgba(130,145,190,.14); }
footer { visibility:hidden; }

.anomalylens-hero {
    padding:1.5rem 1.7rem;
    border-radius:18px;
    background:linear-gradient(135deg,rgba(61,79,255,.18),rgba(119,56,255,.10));
    border:1px solid rgba(112,130,255,.25);
    box-shadow:0 14px 40px rgba(0,0,0,.18);
    margin-bottom:1.4rem;
}
.anomalylens-title {
    font-size:2.45rem; font-weight:800; letter-spacing:-.05em; margin:0;
    background:linear-gradient(90deg,#fff,#a7b4ff);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.anomalylens-subtitle { color:#9aa8c7; font-size:1rem; margin-top:.35rem; }
.status-badge {
    display:inline-flex; align-items:center; padding:.4rem .75rem; border-radius:999px;
    color:#8cf0c0; background:rgba(54,211,153,.10);
    border:1px solid rgba(54,211,153,.25); font-size:.82rem; font-weight:700;
}

.kpi-card {
    position:relative; overflow:hidden; min-height:122px; padding:19px 20px;
    border-radius:16px; background:linear-gradient(145deg,rgba(20,29,52,.97),rgba(15,22,39,.97));
    border:1px solid rgba(112,130,255,.16); box-shadow:0 8px 24px rgba(0,0,0,.15);
    transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease;
}
.kpi-card:hover { transform:translateY(-3px); box-shadow:0 12px 30px rgba(0,0,0,.24); }
.kpi-card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--accent); }
.kpi-label { color:#97a5c4; font-size:.83rem; font-weight:650; }
.kpi-value { color:#f7f9ff; font-size:1.72rem; line-height:1.2; font-weight:800; margin-top:.45rem; }
.kpi-note { color:#7f8dab; font-size:.75rem; margin-top:.35rem; }

.summary-card {
    padding:20px 22px; border-radius:16px;
    background:linear-gradient(145deg,rgba(18,27,49,.94),rgba(13,20,37,.94));
    border:1px solid rgba(112,130,255,.16); box-shadow:0 10px 26px rgba(0,0,0,.14);
}
.summary-title { color:#f5f7ff; font-size:1.08rem; font-weight:750; margin-bottom:14px; }
.summary-row { display:flex; justify-content:space-between; gap:16px; padding:9px 0; border-bottom:1px solid rgba(120,140,255,.09); }
.summary-row:last-child { border-bottom:none; }
.summary-label { color:#8f9dbc; font-size:.82rem; }
.summary-value { color:#eef2ff; font-weight:700; text-align:right; }
.summary-highlight { color:#fb7185; font-size:1.2rem; font-weight:800; }

.badge {
    display:inline-flex; align-items:center; padding:.28rem .55rem; border-radius:999px;
    font-size:.72rem; font-weight:750; border:1px solid rgba(255,255,255,.08);
}
.badge-blue { color:#aebcff; background:rgba(91,124,250,.14); }
.badge-green { color:#83f2df; background:rgba(45,212,191,.12); }
.badge-red { color:#ff9aaa; background:rgba(251,113,133,.12); }
.badge-orange { color:#ffd27a; background:rgba(245,158,11,.12); }
.badge-purple { color:#cebaff; background:rgba(167,139,250,.12); }

.eval-card {
    padding:18px 20px; border-radius:15px; background:rgba(18,27,49,.88);
    border:1px solid rgba(112,130,255,.15); min-height:108px;
}
.eval-label { color:#93a1c1; font-size:.82rem; font-weight:650; }
.eval-value { color:#f8faff; font-size:1.55rem; font-weight:800; margin-top:.4rem; }

div[data-testid="stMetric"] {
    background:linear-gradient(145deg,rgba(20,29,52,.95),rgba(15,22,39,.95));
    border:1px solid rgba(112,130,255,.16); border-radius:16px; padding:20px 22px;
    min-height:120px; box-shadow:0 8px 24px rgba(0,0,0,.15);
}
div[data-testid="stMetricLabel"] { color:#97a5c4; font-weight:650; font-size:.88rem; }
div[data-testid="stMetricValue"] { color:#f7f9ff; font-weight:800; }

div[data-baseweb="tab-list"] { gap:.5rem; border-bottom:1px solid rgba(120,140,255,.12); }
button[data-baseweb="tab"] { color:#9aa8c7; font-weight:650; padding-left:1rem; padding-right:1rem; border-radius:10px 10px 0 0; }
button[data-baseweb="tab"][aria-selected="true"] { color:#dfe5ff; background:rgba(92,112,255,.09); }

.stButton > button {
    border-radius:10px; font-weight:700; min-height:44px;
    border:1px solid rgba(110,130,255,.28);
    background:linear-gradient(90deg,#4457ff,#6f48ff); color:white;
}
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 8px 18px rgba(70,88,255,.28); }
.stDownloadButton > button {
    border-radius:10px; font-weight:700; min-height:44px;
    border:1px solid rgba(87,206,170,.28);
    background:linear-gradient(90deg,#168d78,#1aa88d); color:white;
}

div[data-testid="stFileUploader"] {
    background:rgba(17,25,45,.75); border:1px solid rgba(100,120,255,.16);
    border-radius:14px; padding:.25rem;
}
div[data-baseweb="select"] > div { background-color:#151e35; border-color:rgba(120,140,255,.20); }
div[data-baseweb="input"] { background-color:#151e35; }
div[data-testid="stDataFrame"] {
    border-radius:14px; overflow:hidden; border:1px solid rgba(112,130,255,.12);
    box-shadow:0 8px 22px rgba(0,0,0,.12);
}
div[data-testid="stAlert"] { border-radius:12px; border:1px solid rgba(120,140,255,.14); }
</style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    header_html = (
        '<div class="anomalylens-hero">'
        '<div style="display:flex;justify-content:space-between;align-items:center;gap:20px;">'
        '<div><div class="anomalylens-title">🔍 AnomalyLens</div>'
        '<div class="anomalylens-subtitle">Intelligent anomaly detection and multi-model analysis for structured data</div></div>'
        '<div><span class="status-badge">● System Ready</span></div>'
        '</div></div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def _render_kpi(label, value, accent="blue", note=None):
    color, glow = ACCENTS[accent]
    note_html = f'<div class="kpi-note">{note}</div>' if note else ""
    st.markdown(
        f'<div class="kpi-card" style="--accent:{color};box-shadow:0 8px 24px {glow};">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>{note_html}</div>',
        unsafe_allow_html=True,
    )


def render_dataset_metrics(summary):
    cols = st.columns(4)
    items = [
        ("Total Records", f"{summary['rows']:,}", "blue"),
        ("Columns", summary["columns"], "purple"),
        ("Numeric Features", summary["numeric_features"], "cyan"),
        ("Missing Values", summary["missing_values"], "orange"),
    ]
    for col, (label, value, accent) in zip(cols, items):
        with col:
            _render_kpi(label, value, accent)


def render_analysis_metrics(total, normal, anomalies, rate):
    cols = st.columns(4)
    items = [
        ("Records Analyzed", f"{total:,}", "blue", "Current analysis run"),
        ("Normal Records", f"{normal:,}", "green", "Not flagged by the model"),
        ("Anomalies Detected", f"{anomalies:,}", "red", "Requires investigation"),
        ("Anomaly Rate", f"{rate:.1f}%", "orange", "Share of analyzed records"),
    ]
    for col, item in zip(cols, items):
        with col:
            _render_kpi(*item)


def render_comparison_metrics(isolation_count, lof_count, dbscan_count, consensus_count):
    cols = st.columns(4)
    items = [
        ("Isolation Forest", f"{isolation_count:,}", "blue", "Anomalies detected"),
        ("Local Outlier Factor", f"{lof_count:,}", "purple", "Anomalies detected"),
        ("DBSCAN", f"{dbscan_count:,}", "cyan", "Noise points detected"),
        ("3-Model Consensus", f"{consensus_count:,}", "red", "Flagged by all models"),
    ]
    for col, item in zip(cols, items):
        with col:
            _render_kpi(*item)


def render_detection_summary(algorithm, feature_count, expected_rate, detected_rate, anomaly_count):
    html = (
        '<div class="summary-card">'
        '<div class="summary-title">Detection Summary</div>'
        f'<div class="summary-row"><span class="summary-label">Algorithm</span><span class="badge badge-blue">{algorithm}</span></div>'
        f'<div class="summary-row"><span class="summary-label">Features analyzed</span><span class="summary-value">{feature_count}</span></div>'
        f'<div class="summary-row"><span class="summary-label">Expected anomaly rate</span><span class="summary-value">{expected_rate:.1f}%</span></div>'
        f'<div class="summary-row"><span class="summary-label">Detected anomaly rate</span><span class="summary-value">{detected_rate:.1f}%</span></div>'
        f'<div class="summary-row"><span class="summary-label">Anomalies detected</span><span class="summary-highlight">{anomaly_count:,}</span></div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_evaluation_metrics(metrics):
    cols = st.columns(4)
    items = [
        ("Precision", f"{metrics['precision']:.1%}"),
        ("Recall", f"{metrics['recall']:.1%}"),
        ("F1 Score", f"{metrics['f1']:.1%}"),
        ("Accuracy", f"{metrics['accuracy']:.1%}"),
    ]
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="eval-card"><div class="eval-label">{label}</div><div class="eval-value">{value}</div></div>',
                unsafe_allow_html=True,
            )
