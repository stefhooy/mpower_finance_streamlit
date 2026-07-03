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
)

inject_css()

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="mpower-header">
        <div class="mpower-header-inner">
            <div>
                <h1>PMEC Reconciliation</h1>
                <p>MPower Ventures AG — Zambia Finance Team</p>
            </div>
        </div>
        <div class="mpower-header-stripe"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── File upload ──────────────────────────────────────────────────────────────
upload_result = render_upload_section()

if upload_result is None:
    st.stop()

txt_file, insuf_file, rej_file, actual_transfer, pmec_fee_pct = upload_result

# ── Parse files ──────────────────────────────────────────────────────────────
with st.spinner("Parsing files..."):
    try:
        df_success = parse_successful_txt(txt_file)
        df_insuf = parse_insufficient_funds_xlsx(insuf_file)
        df_rej = parse_rejections_xlsx(rej_file)
    except ValueError as e:
        st.error(f"File error: {e}")
        st.stop()

# ── Reconcile ────────────────────────────────────────────────────────────────
results = reconcile(
    df_success,
    df_insuf,
    df_rej,
    actual_transfer=actual_transfer,
    pmec_fee_pct=pmec_fee_pct,
)

# ── Summary dashboard ────────────────────────────────────────────────────────
render_summary(results)

# ── Download button ──────────────────────────────────────────────────────────
st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

with st.spinner("Preparing Excel export..."):
    excel_bytes = build_excel(df_success, df_insuf, df_rej, results)

period = results['period']
st.download_button(
    label="Download Reconciliation Workbook (.xlsx)",
    data=excel_bytes,
    file_name=f"PMEC_Reconciliation_{period}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="mpower-footer">
        Data is processed in memory only — nothing is stored, uploaded, or retained
        after this session. Close the browser tab to discard all uploaded files.
    </div>
    """,
    unsafe_allow_html=True,
)
