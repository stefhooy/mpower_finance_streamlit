import os
import streamlit as st

NAVY_DARK = "#0A1628"
NAVY = "#142D64"
ORANGE = "#E69500"
GOLD = "#F5B800"
TEXT = "#E8EDF5"
TEXT_MUTED = "#8BAAD4"


def inject_css():
    """Inject MPower dark-navy + African geometric brand CSS."""
    st.markdown(
        f"""
        <style>

        /* ── Base: dark navy canvas with diamond-grid texture ── */
        .stApp {{
            background-color: {NAVY_DARK};
            background-image:
                repeating-linear-gradient(
                    45deg,
                    transparent 0px, transparent 28px,
                    rgba(20,45,100,0.55) 28px, rgba(20,45,100,0.55) 29px
                ),
                repeating-linear-gradient(
                    -45deg,
                    transparent 0px, transparent 28px,
                    rgba(20,45,100,0.55) 28px, rgba(20,45,100,0.55) 29px
                );
        }}

        /* ── Page header ── */
        .mpower-header {{
            background: linear-gradient(135deg, #0D1B3E 0%, {NAVY} 100%);
            border-radius: 0.6rem;
            overflow: hidden;
            margin-bottom: 1.5rem;
            position: relative;
        }}
        /* Diagonal stripe overlay — Adinkra-style geometry */
        .mpower-header::before {{
            content: '';
            position: absolute;
            inset: 0;
            background-image:
                repeating-linear-gradient(
                    60deg,
                    transparent 0px, transparent 18px,
                    rgba(230,149,0,0.07) 18px, rgba(230,149,0,0.07) 19px
                ),
                repeating-linear-gradient(
                    -60deg,
                    transparent 0px, transparent 18px,
                    rgba(230,149,0,0.07) 18px, rgba(230,149,0,0.07) 19px
                );
            pointer-events: none;
        }}
        .mpower-header-inner {{
            padding: 1.2rem 1.6rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            position: relative;
        }}
        .mpower-header h1 {{
            color: white;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }}
        .mpower-header p {{
            color: {TEXT_MUTED};
            margin: 0;
            font-size: 0.85rem;
        }}
        /* Kente-stripe band at base of header */
        .mpower-header-stripe {{
            height: 8px;
            background: repeating-linear-gradient(
                90deg,
                {ORANGE}  0px,  {ORANGE}  22px,
                {GOLD}    22px, {GOLD}    34px,
                white     34px, white     40px,
                {NAVY}    40px, {NAVY}    52px,
                white     52px, white     58px,
                {ORANGE}  58px, {ORANGE}  80px,
                {GOLD}    80px, {GOLD}    92px,
                {NAVY_DARK} 92px, {NAVY_DARK} 104px
            );
        }}

        /* ── Guide intro text ── */
        .guide-intro {{
            font-size: 1rem;
            color: {TEXT_MUTED};
            margin-bottom: 1.2rem;
            line-height: 1.6;
        }}

        /* ── Step cards (placed inside st.columns, not flex wrapper) ── */
        .step-card {{
            background: {NAVY};
            border: 1px solid rgba(230,149,0,0.25);
            border-top: 4px solid {ORANGE};
            border-radius: 0.6rem;
            padding: 1.2rem;
            height: 100%;
            position: relative;
            overflow: hidden;
        }}
        /* Triangular corner accent — Bogolan mud-cloth motif */
        .step-card::after {{
            content: '';
            position: absolute;
            bottom: 0; right: 0;
            width: 0; height: 0;
            border-style: solid;
            border-width: 0 0 36px 36px;
            border-color: transparent transparent
                          rgba(230,149,0,0.18) transparent;
        }}
        .step-number {{
            font-size: 2rem;
            font-weight: 900;
            color: {ORANGE};
            line-height: 1;
            margin-bottom: 0.4rem;
        }}
        .step-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
        }}
        .step-body {{
            font-size: 0.86rem;
            color: {TEXT_MUTED};
            line-height: 1.55;
        }}

        /* ── Section divider — tri-colour gradient rule ── */
        .mpower-divider {{
            border: none;
            height: 4px;
            background: linear-gradient(
                90deg,
                {NAVY_DARK} 0%, {NAVY} 40%,
                {ORANGE} 70%, {GOLD} 100%
            );
            border-radius: 2px;
            margin: 1.6rem 0;
        }}

        /* ── Metric cards ── */
        div[data-testid="metric-container"] {{
            background-color: {NAVY};
            border: 1px solid rgba(230,149,0,0.2);
            border-top: 3px solid {ORANGE};
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
        }}
        div[data-testid="metric-container"] label {{
            color: {TEXT_MUTED} !important;
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        /* ── Expected bank transfer card ── */
        .transfer-card {{
            background: linear-gradient(135deg, {NAVY} 60%, #1a3a7a 100%);
            border: 1px solid rgba(230,149,0,0.35);
            border-radius: 0.6rem;
            text-align: center;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        .transfer-card-inner {{
            padding: 1.3rem 1.5rem;
        }}
        .transfer-card .label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: {TEXT_MUTED};
        }}
        .transfer-card .value {{
            font-size: 2rem;
            font-weight: 800;
            color: white;
            margin: 0.25rem 0;
        }}
        .transfer-card .sub {{
            font-size: 0.82rem;
            color: {TEXT_MUTED};
            margin-top: 0.3rem;
        }}
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

        /* ── Section label ── */
        .section-label {{
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: {ORANGE};
            border-left: 4px solid {ORANGE};
            padding-left: 0.6rem;
            margin: 1rem 0 0.6rem 0;
        }}

        /* ── Flag boxes ── */
        .flag-warning {{
            background-color: rgba(230,149,0,0.12);
            border-left: 4px solid {ORANGE};
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.88rem;
            color: {GOLD};
        }}
        .flag-ok {{
            background-color: rgba(67,160,71,0.12);
            border-left: 4px solid #43a047;
            padding: 0.6rem 1rem;
            border-radius: 0 0.4rem 0.4rem 0;
            margin: 0.4rem 0;
            font-size: 0.88rem;
            color: #81c784;
        }}

        /* ── Upload hints ── */
        .upload-hint {{
            font-size: 0.78rem;
            color: {TEXT_MUTED};
            margin-top: -0.4rem;
            margin-bottom: 0.5rem;
        }}

        /* ── Footer ── */
        .mpower-footer {{
            margin-top: 3rem;
            padding: 1rem 0;
            border-top: 1px solid rgba(230,149,0,0.2);
            font-size: 0.78rem;
            color: {TEXT_MUTED};
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar logo
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets",
        "mpower_africa_logo.jpg",
    )
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
