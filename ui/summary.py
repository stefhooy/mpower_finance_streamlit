import streamlit as st


def _zmw(value) -> str:
    """Format a number as ZMW with thousands separator."""
    try:
        return f"ZMW {value:,.2f}"
    except (TypeError, ValueError):
        return "ZMW N/A"


def render_summary(results: dict):
    """Render the reconciliation dashboard: metrics, bank transfer, flags, breakdowns."""

    period = results['period']
    fee_pct = results['pmec_fee_pct'] * 100

    st.subheader(f"Reconciliation Results: Period {period}")

    # ── Row 1: three category metrics ──
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Successful Deductions",
            value=_zmw(results['total_successful']),
            delta=f"{results['n_successful']} employees",
            delta_color="off",
        )
    with col2:
        st.metric(
            label="Insufficient Funds",
            value=_zmw(results['total_insuf']),
            delta=f"{results['n_insuf']} employees",
            delta_color="off",
        )
    with col3:
        st.metric(
            label="Rejected",
            value=_zmw(results['total_rej']),
            delta=f"{results['n_rej']} employees",
            delta_color="off",
        )

    st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

    # ── Expected bank transfer (highlighted card) ──
    discrepancy_html = ""
    if results['actual_transfer'] is not None:
        diff = results['transfer_discrepancy']
        status = "PASS" if abs(diff) < 1 else f"CHECK: discrepancy of {_zmw(diff)}"
        implied = results['implied_fee_pct'] * 100
        discrepancy_html = (
            f'<div class="sub">Actual received: {_zmw(results["actual_transfer"])} '
            f'&nbsp;|&nbsp; Implied fee: {implied:.2f}% &nbsp;|&nbsp; {status}</div>'
        )

    st.markdown(
        f"""
        <div class="transfer-card">
            <div class="label">Expected Bank Transfer (after {fee_pct:.1f}% PMEC fee)</div>
            <div class="value">{_zmw(results['expected_transfer'])}</div>
            {discrepancy_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

    # ── Data quality flags ──
    st.markdown("**Data Quality Flags**")

    flags = []
    if results['n_insuf_missing_amount'] > 0:
        flags.append(
            f"{results['n_insuf_missing_amount']} insufficient funds records "
            "have no amount recorded. These contribute ZMW 0 to the total."
        )
    if results['n_rej_duplicate_employees'] > 0:
        flags.append(
            f"{results['n_rej_duplicate_employees']} rejection rows share a "
            "duplicate employee number. Review the rejections sheet."
        )

    if flags:
        for flag in flags:
            st.markdown(
                f'<div class="flag-warning">⚠ {flag}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="flag-ok">✓ No data quality issues detected</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

    # ── Breakdown tables ──
    tab1, tab2, tab3 = st.tabs([
        "Successful: by Personnel Area",
        "Insufficient Funds: by Reason",
        "Rejections: by Category",
    ])

    with tab1:
        st.dataframe(
            results['success_breakdown'],
            use_container_width=True,
            hide_index=True,
        )

    with tab2:
        df_insuf = results['insuf_breakdown'].copy()
        df_insuf['Amount (ZMW)'] = df_insuf['Amount (ZMW)'].round(2)
        st.dataframe(df_insuf, use_container_width=True, hide_index=True)

    with tab3:
        df_rej = results['rej_breakdown'].copy()
        df_rej['Amount (ZMW)'] = df_rej['Amount (ZMW)'].round(2)
        st.dataframe(df_rej, use_container_width=True, hide_index=True)
