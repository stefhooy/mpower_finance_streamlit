import os
import streamlit as st


NAVY = "#142D64"
ORANGE = "#E69500"


def inject_css():
    """Inject MPower brand CSS and configure the sidebar logo."""
    st.markdown(
        f"""
        <style>
        /* ── Page header bar ── */
        .mpower-header {{
            background-color: {NAVY};
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .mpower-header h1 {{
            color: white;
            margin: 0;
            font-size: 1.4rem;
            font-weight: 700;
        }}
        .mpower-header p {{
            color: #cccccc;
            margin: 0;
            font-size: 0.85rem;
        }}

        /* ── Section divider ── */
        .mpower-divider {{
            border: none;
            border-top: 3px solid {ORANGE};
            margin: 1.5rem 0;
        }}

        /* ── Metric cards ── */
        div[data-testid="metric-container"] {{
            background-color: #f7f9fc;
            border: 1px solid #dde3ef;
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
        }}
        div[data-testid="metric-container"] label {{
            color: {NAVY};
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* ── Highlighted transfer metric ── */
        .transfer-card {{
            background-color: {NAVY};
            color: white;
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            text-align: center;
            margin-top: 0.5rem;
        }}
        .transfer-card .label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #aabbdd;
        }}
        .transfer-card .value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
        }}
        .transfer-card .sub {{
            font-size: 0.8rem;
            color: #aabbdd;
            margin-top: 0.25rem;
        }}

        /* ── Warning / flag boxes ── */
        .flag-warning {{
            background-color: #fff8e1;
            border-left: 4px solid {ORANGE};
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.9rem;
        }}
        .flag-ok {{
            background-color: #e8f5e9;
            border-left: 4px solid #43a047;
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.9rem;
        }}

        /* ── Upload section cards ── */
        .upload-hint {{
            font-size: 0.78rem;
            color: #888;
            margin-top: -0.5rem;
            margin-bottom: 0.5rem;
        }}

        /* ── Footer ── */
        .mpower-footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #dde3ef;
            font-size: 0.78rem;
            color: #888;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar logo — only shown if the file exists in assets/
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "assets", "mpower_africa_logo.jpg"
    )
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
