"""
theme.py - Custom theme injector untuk Dashboard MBG
Import dan panggil apply_theme() di paling atas app.py, setelah st.set_page_config()

Prinsip desain:
- Palet terbatas: petrol blue (#2E6F95) sebagai SATU-SATUNYA aksen utama
- Tanpa glow/shadow/gradient
- Tanpa badge pil berwarna-warni
- Tanpa ikon dekoratif di KPI card
- Border tipis 1px, border-radius kecil (4-6px)
- Font monospace untuk angka (kesan presisi data, bukan marketing)
- Eyebrow label (huruf kapital, letter-spacing) di atas tiap KPI, bukan ikon
"""

import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        /* ============ BASE ============ */
        html, body, [class*="css"] {
            font-family: 'IBM Plex Sans', sans-serif;
        }

        .stApp {
            background-color: #0B1220;
        }

        /* ============ STATUS STRIP (signature element) ============ */
        .status-strip {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 16px;
            background-color: #0E1526;
            border-bottom: 1px solid #1F2A44;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            color: #8B95A7;
            letter-spacing: 0.04em;
            margin: -1rem -1rem 1.5rem -1rem;
        }
        .status-strip .dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #4C9A6A;
            margin-right: 6px;
        }

        /* ============ HEADINGS ============ */
        h1 {
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 1.5rem;
            color: #E8EAED;
            letter-spacing: -0.01em;
        }
        h2, h3 {
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 500;
            font-size: 1.05rem;
            color: #E8EAED;
            border-bottom: 1px solid #1F2A44;
            padding-bottom: 0.4rem;
        }

        p, .stMarkdown {
            color: #8B95A7;
            font-size: 0.875rem;
        }

        /* ============ KPI METRIC CARDS ============ */
        div[data-testid="stMetric"] {
            background-color: #11192B;
            border: 1px solid #1F2A44;
            border-radius: 5px;
            padding: 14px 16px;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.7rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #8B95A7 !important;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 500;
            color: #E8EAED !important;
            font-size: 1.6rem !important;
        }
        div[data-testid="stMetricDelta"] {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
        }

        /* ============ SIDEBAR ============ */
        section[data-testid="stSidebar"] {
            background-color: #0E1526;
            border-right: 1px solid #1F2A44;
        }
        section[data-testid="stSidebar"] .stMultiSelect label,
        section[data-testid="stSidebar"] h2 {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #8B95A7;
            font-weight: 500;
        }

        /* ============ DIVIDER ============ */
        hr {
            border-color: #1F2A44 !important;
            margin: 1.5rem 0 !important;
        }

        /* ============ DATAFRAME / TABLE ============ */
        div[data-testid="stDataFrame"] {
            border: 1px solid #1F2A44;
            border-radius: 5px;
        }

        /* ============ BUTTONS ============ */
        .stButton button, .stDownloadButton button {
            background-color: #11192B;
            border: 1px solid #2E6F95;
            color: #E8EAED;
            border-radius: 4px;
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.8rem;
            font-weight: 500;
        }
        .stButton button:hover, .stDownloadButton button:hover {
            background-color: #2E6F95;
            border-color: #2E6F95;
            color: #FFFFFF;
        }

        /* ============ ALERT / INFO BOX (no rounded pill, flat left-border style) ============ */
        div[data-testid="stAlert"] {
            background-color: #11192B;
            border: 1px solid #1F2A44;
            border-left: 3px solid #C7622D;
            border-radius: 4px;
            color: #E8EAED;
        }

        /* ============ TABS (if used) ============ */
        button[data-baseweb="tab"] {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.85rem;
            color: #8B95A7;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #E8EAED;
            border-bottom: 2px solid #2E6F95;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_strip(records: int, last_sync: str, pipeline_status: str = "ACTIVE"):
    """
    Render strip status di bagian paling atas dashboard.
    Signature element: meniru system status bar command center,
    relevan karena dashboard ini berbasis snapshot data pull (date_pull).

    Contoh pemanggilan di app.py:
        status_strip(records=len(df), last_sync="2026-06-19 13:39")
    """
    st.markdown(
        f"""
        <div class="status-strip">
            <span>MBG ANALYTICS &nbsp;|&nbsp; GOVERNMENT OVERSIGHT DASHBOARD</span>
            <span>
                LAST SYNC: {last_sync} &nbsp;&nbsp;
                RECORDS: {records:,} &nbsp;&nbsp;
                <span class="dot"></span>PIPELINE: {pipeline_status}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============ PLOTLY CHART THEME HELPER ============
# Panggil ini di setiap figure plotly sebelum st.plotly_chart()
# agar background, font, dan gridline konsisten dengan tema dashboard.

def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="#11192B",
        plot_bgcolor="#11192B",
        font=dict(family="IBM Plex Sans, sans-serif", color="#8B95A7", size=12),
        title_font=dict(family="IBM Plex Sans, sans-serif", size=14, color="#E8EAED"),
        legend=dict(font=dict(size=11, color="#8B95A7")),
        margin=dict(t=40, l=10, r=10, b=10),
    )
    fig.update_xaxes(gridcolor="#1F2A44", linecolor="#1F2A44", zerolinecolor="#1F2A44")
    fig.update_yaxes(gridcolor="#1F2A44", linecolor="#1F2A44", zerolinecolor="#1F2A44")
    return fig
