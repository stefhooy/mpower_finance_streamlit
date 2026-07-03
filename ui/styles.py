import os
import streamlit as st


NAVY = "#142D64"
ORANGE = "#E69500"
GOLD = "#F5B800"
WARM_WHITE = "#FAFAF7"


def inject_css():
    """Inject MPower brand CSS with African-inspired geometric accents."""
    st.markdown(
        f"""
        <style>
        /* ── Global warm background ── */
        .stApp {{
            background-color: {WARM_WHITE};
        }}

        /* ── Page header bar ── */
        .mpower-header {{
            background-color: {NAVY};
            padding: 0;
            border-radius: 0.6rem;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}
        .mpower-header-inner {{
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .mpower-header h1 {{
            color: white;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }}
        .mpower-header p {{
            color: #aabbd4;
            margin: 0;
            font-size: 0.85rem;
        }}
        /* African kente-stripe accent at bottom of header */
        .mpower-header-stripe {{
            height: 7px;
            background: repeating-linear-gradient(
                90deg,
                {ORANGE}   0px,  {ORANGE}  24px,
                {GOLD}     24px, {GOLD}    36px,
                white      36px, white     42px,
                {NAVY}     42px, {NAVY}    54px,
                white      54px, white     60px,
                {ORANGE}   60px, {ORANGE}  84px,
                {GOLD}     84px, {GOLD}    96px,
                {NAVY}     96px, {NAVY}   108px
            );
        }}

        /* ── Section divider — double-rule with orange/navy ── */
        .mpower-divider {{
            border: none;
            height: 4px;
            background: linear-gradient(
                90deg,
                {NAVY} 0%, {NAVY} 60%,
                {ORANGE} 60%, {ORANGE} 80%,
                {GOLD} 80%, {GOLD} 100%
            );
            border-radius: 2px;
            margin: 1.5rem 0;
        }}

        /* ── Metric cards ── */
        div[data-testid="metric-container"] {{
            background-color: white;
            border: 1px solid #dde3ef;
            border-top: 3px solid {ORANGE};
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
        }}
        div[data-testid="metric-container"] label {{
            color: {NAVY};
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* ── Highlighted transfer card ── */
        .transfer-card {{
            background: linear-gradient(135deg, {NAVY} 70%, #1e3d80 100%);
            color: white;
            border-radius: 0.6rem;
            padding: 0;
            text-align: center;
            margin-top: 0.5rem;
            overflow: hidden;
        }}
        .transfer-card-inner {{
            padding: 1.2rem 1.5rem;
        }}
        .transfer-card .label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #aabbd4;
        }}
        .transfer-card .value {{
            font-size: 2rem;
            font-weight: 800;
            color: white;
            margin: 0.2rem 0;
        }}
        .transfer-card .sub {{
            font-size: 0.82rem;
            color: #aabbd4;
            margin-top: 0.3rem;
        }}
        /* Kente stripe accent at bottom of transfer card */
        .transfer-card-stripe {{
            height: 5px;
            background: repeating-linear-gradient(
                90deg,
                {ORANGE} 0px, {ORANGE} 20px,
                {GOLD}   20px, {GOLD}   32px,
                white    32px, white    38px,
                {ORANGE} 38px, {ORANGE} 58px
            );
        }}

        /* ── Section label (bold orange-left-border style) ── */
        .section-label {{
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {NAVY};
            border-left: 4px solid {ORANGE};
            padding-left: 0.6rem;
            margin: 1rem 0 0.6rem 0;
        }}

        /* ── Warning / flag boxes ── */
        .flag-warning {{
            background-color: #fff8e1;
            border-left: 4px solid {ORANGE};
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.88rem;
            color: #5a3e00;
        }}
        .flag-ok {{
            background-color: #e8f5e9;
            border-left: 4px solid #43a047;
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.88rem;
            color: #1b5e20;
        }}

        /* ── Upload section hints ── */
        .upload-hint {{
            font-size: 0.78rem;
            color: #888;
            margin-top: -0.4rem;
            margin-bottom: 0.5rem;
        }}

        /* ── Footer ── */
        .mpower-footer {{
            margin-top: 3rem;
            padding: 1rem 0;
            border-top: 3px solid;
            border-image: linear-gradient(
                90deg, {NAVY}, {ORANGE}, {GOLD}
            ) 1;
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
