import streamlit as st


def apply_dashboard_styles():
    """
    Apply the main AnomalyLens visual theme.
    """

    st.markdown(
        """
        <style>

        /* ==========================================
           APP BACKGROUND
        ========================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(68, 89, 255, 0.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at top right,
                    rgba(138, 43, 226, 0.10),
                    transparent 25%
                ),
                #0b1020;
            color: #eaf0ff;
        }


        /* ==========================================
           MAIN CONTAINER
        ========================================== */

        .block-container {
            padding-top: 1.7rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }


        /* ==========================================
           SIDEBAR
        ========================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #10172a 0%,
                    #0d1322 100%
                );

            border-right:
                1px solid rgba(120, 140, 255, 0.18);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.7rem;
        }


        /* ==========================================
           HEADINGS
        ========================================== */

        h1, h2, h3 {
            color: #f5f7ff;
            letter-spacing: -0.025em;
        }

        h1 {
            font-weight: 800;
        }

        h2 {
            font-weight: 720;
        }

        h3 {
            font-weight: 680;
        }


        /* ==========================================
           PRODUCT HEADER
        ========================================== */

        .anomalylens-hero {
            padding: 1.5rem 1.7rem;
            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    rgba(61, 79, 255, 0.18),
                    rgba(119, 56, 255, 0.10)
                );

            border:
                1px solid rgba(112, 130, 255, 0.25);

            box-shadow:
                0 14px 40px rgba(0, 0, 0, 0.18);

            margin-bottom: 1.4rem;
        }

        .anomalylens-title {
            font-size: 2.45rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            margin: 0;

            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #a7b4ff
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .anomalylens-subtitle {
            color: #9aa8c7;
            font-size: 1rem;
            margin-top: 0.35rem;
            margin-bottom: 0;
        }


        /* ==========================================
           STATUS BADGE
        ========================================== */

        .status-badge {
            display: inline-flex;
            align-items: center;

            padding:
                0.4rem 0.75rem;

            border-radius:
                999px;

            color:
                #8cf0c0;

            background:
                rgba(54, 211, 153, 0.10);

            border:
                1px solid rgba(54, 211, 153, 0.25);

            font-size:
                0.82rem;

            font-weight:
                700;
        }


        /* ==========================================
           METRIC CARDS
        ========================================== */

        div[data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(20, 29, 52, 0.95),
                    rgba(15, 22, 39, 0.95)
                );

            border:
                1px solid rgba(112, 130, 255, 0.16);

            border-radius:
                16px;

            padding:
                20px 22px;

            min-height:
                125px;

            box-shadow:
                0 8px 24px rgba(0, 0, 0, 0.15);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform:
                translateY(-3px);

            border-color:
                rgba(110, 132, 255, 0.45);

            box-shadow:
                0 12px 30px rgba(0, 0, 0, 0.24);
        }

        div[data-testid="stMetricLabel"] {
            color:
                #97a5c4;

            font-weight:
                650;

            font-size:
                0.88rem;
        }

        div[data-testid="stMetricValue"] {
            color:
                #f7f9ff;

            font-weight:
                800;
        }


        /* ==========================================
           TABS
        ========================================== */

        div[data-baseweb="tab-list"] {
            gap: 0.5rem;
            border-bottom:
                1px solid rgba(120, 140, 255, 0.12);
        }

        button[data-baseweb="tab"] {
            color:
                #9aa8c7;

            font-weight:
                650;

            padding-left:
                1rem;

            padding-right:
                1rem;

            border-radius:
                10px 10px 0 0;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color:
                #dfe5ff;

            background:
                rgba(92, 112, 255, 0.09);
        }


        /* ==========================================
           BUTTONS
        ========================================== */

        .stButton > button {
            border-radius:
                10px;

            font-weight:
                700;

            min-height:
                44px;

            border:
                1px solid rgba(110, 130, 255, 0.28);

            background:
                linear-gradient(
                    90deg,
                    #4457ff,
                    #6f48ff
                );

            color:
                white;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }

        .stButton > button:hover {
            transform:
                translateY(-1px);

            box-shadow:
                0 8px 18px rgba(70, 88, 255, 0.28);
        }


        /* ==========================================
           DOWNLOAD BUTTON
        ========================================== */

        .stDownloadButton > button {
            border-radius:
                10px;

            font-weight:
                700;

            min-height:
                44px;

            border:
                1px solid rgba(87, 206, 170, 0.28);

            background:
                linear-gradient(
                    90deg,
                    #168d78,
                    #1aa88d
                );

            color:
                white;
        }


        /* ==========================================
           FILE UPLOADER
        ========================================== */

        div[data-testid="stFileUploader"] {
            background:
                rgba(17, 25, 45, 0.75);

            border:
                1px solid rgba(100, 120, 255, 0.16);

            border-radius:
                14px;

            padding:
                0.25rem;
        }


        /* ==========================================
           INPUT CONTROLS
        ========================================== */

        div[data-baseweb="select"] > div {
            background-color:
                #151e35;

            border-color:
                rgba(120, 140, 255, 0.20);
        }

        div[data-baseweb="input"] {
            background-color:
                #151e35;
        }


        /* ==========================================
           TABLES / DATAFRAMES
        ========================================== */

        div[data-testid="stDataFrame"] {
            border-radius:
                14px;

            overflow:
                hidden;

            border:
                1px solid rgba(112, 130, 255, 0.12);

            box-shadow:
                0 8px 22px rgba(0, 0, 0, 0.12);
        }


        /* ==========================================
           INFO / SUCCESS BOXES
        ========================================== */

        div[data-testid="stAlert"] {
            border-radius:
                12px;

            border:
                1px solid rgba(120, 140, 255, 0.14);
        }


        /* ==========================================
           DIVIDERS
        ========================================== */

        hr {
            border-color:
                rgba(130, 145, 190, 0.14);
        }


        /* ==========================================
           CAPTIONS / BODY
        ========================================== */

        p {
            color:
                #b7c1d9;
        }

        small {
            color:
                #8694b3;
        }


        /* ==========================================
           HIDE STREAMLIT FOOTER
        ========================================== */

        footer {
            visibility: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_header():
    """
    Render the main AnomalyLens product header.
    """

    header_html = (
        '<div class="anomalylens-hero">'
        '<div style="display:flex;justify-content:space-between;'
        'align-items:center;gap:20px;">'
        '<div>'
        '<div class="anomalylens-title">🔍 AnomalyLens</div>'
        '<div class="anomalylens-subtitle">'
        'Intelligent anomaly detection and multi-model analysis '
        'for structured data'
        '</div>'
        '</div>'
        '<div>'
        '<span class="status-badge">● System Ready</span>'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True
    )

def render_dataset_metrics(summary):
    """
    Render top-level dataset KPI cards.
    """

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{summary['rows']:,}"
    )

    col2.metric(
        "Columns",
        summary["columns"]
    )

    col3.metric(
        "Numeric Features",
        summary["numeric_features"]
    )

    col4.metric(
        "Missing Values",
        summary["missing_values"]
    )