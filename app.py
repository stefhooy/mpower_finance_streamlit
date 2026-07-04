import os
import base64
import streamlit as st

from core.parser import (
    parse_successful_txt,
    parse_insufficient_funds_xlsx,
    parse_rejections_xlsx,
)
from core.reconcile import reconcile
from core.export import build_excel
from ui.styles import inject_css
from ui.upload import render_upload_section
from ui.summary import render_summary

st.set_page_config(
    page_title="MPower PMEC Reconciliation",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


def _img_b64(filename: str, mime: str = "image/jpeg") -> str:
    """Return a base64 data-URI for a file in assets/, or empty string."""
    path = os.path.join("assets", filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def _logo_html(height: int = 52) -> str:
    src = _img_b64("mpower_africa_logo.jpg", "image/jpeg")
    if not src:
        return ""
    return (
        f'<img src="{src}" height="{height}"'
        ' style="border-radius:6px; margin-right:1rem;">'
    )


def _african_banner_html() -> str:
    src = _img_b64("african_design_1.png", "image/png")
    if not src:
        return ""
    return (
        f'<img src="{src}" style="width:100%; height:60px;'
        ' object-fit:cover; object-position:center; display:block;'
        ' opacity:0.92;">'
    )


# ── Header
st.markdown(
    f"""
    <div class="mpower-header">
        <div class="mpower-header-inner">
            {_logo_html(52)}
            <div>
                <h1>PMEC Reconciliation Tool</h1>
                <p>MPower Ventures AG &nbsp;·&nbsp; Zambia Finance Team</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# African design strip — full width below header
_banner = _img_b64("african_design_1.png", "image/png")
if _banner:
    st.markdown(
        f'<img src="{_banner}" style="'
        'width:100%; height:110px; display:block;'
        'object-fit:cover; object-position:center 40%;'
        'border-radius:0.5rem; margin-bottom:1.2rem;">',
        unsafe_allow_html=True,
    )

# ── Intro
st.markdown(
    """
    <div class="guide-intro">
    This tool takes the three files PMEC returns to MPower each month,
    runs the full reconciliation automatically, and produces a
    ready-to-use Excel workbook. No Python or technical knowledge needed.
    </div>
    """,
    unsafe_allow_html=True,
)

# ── How it works
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-title">Get your three PMEC files</div>
            <div class="step-body">
                After each monthly submission, PMEC returns three files:
                a <strong>.txt</strong> file for successful deductions,
                and two <strong>.xlsx</strong> files for insufficient
                funds and rejections.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-title">Upload each file in its slot</div>
            <div class="step-body">
                Use the upload section below. Each slot accepts only the
                correct file type. The tool will not run until all three
                files are uploaded.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-title">Download the workbook</div>
            <div class="step-body">
                The tool produces a <strong>7-sheet Excel workbook</strong>
                with the full reconciliation summary, all three data sets,
                and breakdowns by Personnel Area, Reason, and
                Rejection Category.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

# ── File guide
with st.expander("Which files do I need? (click to open)"):
    g1, g2, g3 = st.columns(3)

    with g1:
        st.markdown("**File 1: Successful Payments**")
        st.caption("E892 - MPower Ventures Zambia.txt")
        st.markdown(
            "Fixed-width text file. Each row starting with `|` that contains "
            "the month period code is one deduction record.\n\n"
            "Fields: Personnel Area, SubArea, Employee No, Name, "
            "NRC No, Period (YYYYMM), Amount (ZMW)"
        )

    with g2:
        st.markdown("**File 2: Insufficient Funds**")
        st.caption("E892.xlsx")
        st.markdown(
            "Excel file listing employees whose salary headroom was below "
            "the 30% threshold required by Zambian law.\n\n"
            "Required columns: `Employee No.`, `Employee Name`, "
            "`Personnel SubArea Text`, `Start Date`, `End Date`, "
            "`Amount`, `Reason`"
        )

    with g3:
        st.markdown("**File 3: Rejections**")
        st.caption("E892 R.xlsx")
        st.markdown(
            "Excel file listing employees rejected by PMEC.\n\n"
            "Required columns: `PERNR`, `FIRST NAME`, `SURNAME`, "
            "`BEGDA`, `ENDDA`, `BETRG`, `COMMENTS`\n\n"
            "> Note: `SEPARATEES` and `LOCKED` are the two largest "
            "rejection categories. Their exact meaning in the Zambian "
            "government HR system should be confirmed with PMEC directly."
        )

# ── Output guide
with st.expander("What does the output look like? (click to open)"):
    st.markdown(
        "The downloaded workbook contains **7 sheets**:\n\n"
        "| Sheet | Contents |\n"
        "|---|---|\n"
        "| `1_Reconciliation_Summary` | Totals, bank transfer, "
        "data quality flags |\n"
        "| `2_Successful_Payments` | Full deductions list |\n"
        "| `3_Insufficient_Funds` | Full insufficient funds list |\n"
        "| `4_Rejections` | Full rejections list |\n"
        "| `5a_Success_Breakdown` | Grouped by Personnel Area |\n"
        "| `5b_Insuf_Breakdown` | Grouped by Reason |\n"
        "| `5c_Rejection_Breakdown` | Grouped by rejection category |\n\n"
        "The summary sheet also shows the PMEC fee calculation and "
        "any data quality flags."
    )

st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

# ── Upload
upload_result = render_upload_section()

if upload_result is None:
    st.stop()

txt_file, insuf_file, rej_file, pmec_fee_pct = upload_result

# ── Parse
with st.spinner("Reading and validating files..."):
    try:
        df_success = parse_successful_txt(txt_file)
        df_insuf = parse_insufficient_funds_xlsx(insuf_file)
        df_rej = parse_rejections_xlsx(rej_file)
    except ValueError as e:
        st.error(f"Could not read file: {e}")
        st.stop()

# ── Reconcile
results = reconcile(
    df_success,
    df_insuf,
    df_rej,
    pmec_fee_pct=pmec_fee_pct,
)

# ── Dashboard
render_summary(results)

# ── Download
st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

with st.spinner("Building Excel workbook..."):
    excel_bytes = build_excel(df_success, df_insuf, df_rej, results)

period = results['period']
st.download_button(
    label="Download Reconciliation Workbook (.xlsx)",
    data=excel_bytes,
    file_name=f"PMEC_Reconciliation_{period}.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument"
        ".spreadsheetml.sheet"
    ),
    use_container_width=True,
)

# ── Footer
st.markdown(
    """
    <div class="mpower-footer">
        Data is processed in memory only. Nothing is stored or retained
        after you close this tab. &nbsp;·&nbsp; MPower Ventures AG
    </div>
    """,
    unsafe_allow_html=True,
)
