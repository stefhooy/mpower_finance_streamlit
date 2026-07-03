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
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


# ── Helper: load logo as base64 for inline HTML ──────────────────────────────
def _logo_html(height: int = 56) -> str:
    logo_path = os.path.join("assets", "mpower_africa_logo.jpg")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (
            f'<img src="data:image/jpeg;base64,{b64}" '
            f'height="{height}" style="border-radius:6px; margin-right:1rem;">'
        )
    return ""


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="mpower-header">
        <div class="mpower-header-inner">
            {_logo_html(56)}
            <div>
                <h1>PMEC Reconciliation Tool</h1>
                <p>MPower Ventures AG &nbsp;·&nbsp; Zambia Finance Team</p>
            </div>
        </div>
        <div class="mpower-header-stripe"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── How it works guide ───────────────────────────────────────────────────────
st.markdown(
    """
    <div class="guide-intro">
        This tool takes the three files PMEC returns to MPower each month, runs
        the full reconciliation, and produces a ready-to-use Excel workbook —
        no Python or technical knowledge required.
    </div>

    <div class="steps-row">

        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-title">Get your three PMEC files</div>
            <div class="step-body">
                After each monthly submission, PMEC sends back three files:
                a <strong>.txt</strong> file for successful deductions, and two
                <strong>.xlsx</strong> files for insufficient funds and rejections.
            </div>
        </div>

        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-title">Upload each file in the correct slot</div>
            <div class="step-body">
                Use the upload section below. Each slot accepts only the correct
                file type. Upload all three files — the tool will not run until
                all three are present.
            </div>
        </div>

        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-title">Download the reconciliation workbook</div>
            <div class="step-body">
                The tool produces a <strong>7-sheet Excel workbook</strong> with
                the full reconciliation summary, all three data sets, and
                breakdowns by Personnel Area, Reason, and Rejection Category.
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ── File structure guide (collapsible) ───────────────────────────────────────
with st.expander("Which files do I need? (click to expand)", expanded=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **File 1 — Successful Payments**
            `E892 - MPower Ventures Zambia (1).txt`

            A fixed-width text file. Each row that starts with `|` and contains
            the month period code is a deduction record.

            Expected fields per row:
            - Personnel Area & SubArea
            - Employee Number
            - Employee Name
            - NRC Number
            - Period (YYYYMM)
            - Amount deducted (ZMW)
            """
        )

    with col2:
        st.markdown(
            """
            **File 2 — Insufficient Funds**
            `E892 (1).xlsx`

            An Excel file listing employees whose salary headroom was below
            the 30% threshold required by Zambian law.

            Required columns:
            - `Employee No.`
            - `Employee Name`
            - `Personnel SubArea Text`
            - `Start Date` / `End Date`
            - `Amount`
            - `Reason`
            """
        )

    with col3:
        st.markdown(
            """
            **File 3 — Rejections**
            `E892 R.xlsx`

            An Excel file listing employees rejected by PMEC for reasons such
            as termination, retirement, dismissal, or invalid payroll data.

            Required columns:
            - `PERNR` (Employee ID)
            - `FIRST NAME` / `SURNAME`
            - `BEGDA` / `ENDDA` (dates)
            - `BETRG` (amount)
            - `COMMENTS` (rejection category)
            """
        )

    st.markdown(
        """
        > **Note on rejection categories:** Two of the most common rejection codes —
        > `SEPARATEES` and `LOCKED` — refer to Zambian government HR statuses that are
        > not defined in the files themselves. Confirm their meaning with the PMEC
        > administrator if you are unsure how to treat them.
        """
    )

st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

# ── What you will get (output preview) ───────────────────────────────────────
with st.expander(
    "What will the output look like? (click to expand)", expanded=False
):
    st.markdown(
        """
        The downloaded Excel workbook contains **7 sheets**:

        | Sheet | Contents |
        |---|---|
        | `1_Reconciliation_Summary` | Formatted summary: total by category, expected bank transfer, data quality flags |
        | `2_Successful_Payments` | Full row-level list of successful deductions |
        | `3_Insufficient_Funds` | Full row-level list of insufficient funds records |
        | `4_Rejections` | Full row-level list of rejections |
        | `5a_Success_Breakdown` | Successful deductions grouped by Personnel Area |
        | `5b_Insuf_Breakdown` | Insufficient funds grouped by Reason |
        | `5c_Rejection_Breakdown` | Rejections grouped by category (COMMENTS column) |

        If you enter the actual bank transfer amount received, the summary sheet will also
        show the implied PMEC fee percentage and flag any discrepancy from the expected amount.
        """
    )

st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

# ── File upload ───────────────────────────────────────────────────────────────
upload_result = render_upload_section()

if upload_result is None:
    st.stop()

txt_file, insuf_file, rej_file, actual_transfer, pmec_fee_pct = upload_result

# ── Parse ─────────────────────────────────────────────────────────────────────
with st.spinner("Reading and validating files..."):
    try:
        df_success = parse_successful_txt(txt_file)
        df_insuf = parse_insufficient_funds_xlsx(insuf_file)
        df_rej = parse_rejections_xlsx(rej_file)
    except ValueError as e:
        st.error(f"Could not read file: {e}")
        st.stop()

# ── Reconcile ─────────────────────────────────────────────────────────────────
results = reconcile(
    df_success,
    df_insuf,
    df_rej,
    actual_transfer=actual_transfer,
    pmec_fee_pct=pmec_fee_pct,
)

# ── Dashboard ─────────────────────────────────────────────────────────────────
render_summary(results)

# ── Download ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

with st.spinner("Building Excel workbook..."):
    excel_bytes = build_excel(df_success, df_insuf, df_rej, results)

period = results['period']
st.download_button(
    label="⬇  Download Reconciliation Workbook (.xlsx)",
    data=excel_bytes,
    file_name=f"PMEC_Reconciliation_{period}.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ),
    use_container_width=True,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="mpower-footer">
        Data is processed in memory only — nothing is stored, uploaded,
        or retained after you close this tab. &nbsp;·&nbsp; MPower Ventures AG
    </div>
    """,
    unsafe_allow_html=True,
)
