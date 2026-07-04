import streamlit as st


def render_upload_section() -> tuple | None:
    """Render the three file uploaders and PMEC fee input.

    Returns:
        (txt_file, insuf_file, rej_file, pmec_fee_pct)
        or None if not all three required files have been uploaded.
    """
    st.subheader("Upload PMEC Return Files")
    st.markdown(
        "Upload the three files returned by PMEC for the month "
        "you want to reconcile."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Successful Payments**")
        st.markdown(
            '<p class="upload-hint">Fixed-width text file, '
            'e.g. E892 - MPower Ventures Zambia.txt</p>',
            unsafe_allow_html=True,
        )
        txt_file = st.file_uploader(
            "Successful payments (.txt)",
            type=["txt"],
            key="upload_txt",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("**Insufficient Funds**")
        st.markdown(
            '<p class="upload-hint">Excel file, e.g. E892.xlsx</p>',
            unsafe_allow_html=True,
        )
        insuf_file = st.file_uploader(
            "Insufficient funds (.xlsx)",
            type=["xlsx"],
            key="upload_insuf",
            label_visibility="collapsed",
        )

    with col3:
        st.markdown("**Rejections**")
        st.markdown(
            '<p class="upload-hint">Excel file, e.g. E892 R.xlsx</p>',
            unsafe_allow_html=True,
        )
        rej_file = st.file_uploader(
            "Rejections (.xlsx)",
            type=["xlsx"],
            key="upload_rej",
            label_visibility="collapsed",
        )

    st.markdown('<hr class="mpower-divider">', unsafe_allow_html=True)

    col_a, _ = st.columns([2, 5])
    with col_a:
        pmec_fee_pct = st.number_input(
            "PMEC fee % (default 2%)",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1,
            format="%.2f",
            help=(
                "The PMEC administration fee applied to successful "
                "deductions. Change this if the rate differs this month."
            ),
        ) / 100.0

    if not (txt_file and insuf_file and rej_file):
        missing = []
        if not txt_file:
            missing.append("Successful payments (.txt)")
        if not insuf_file:
            missing.append("Insufficient funds (.xlsx)")
        if not rej_file:
            missing.append("Rejections (.xlsx)")
        st.info(f"Waiting for: {', '.join(missing)}")
        return None

    return txt_file, insuf_file, rej_file, pmec_fee_pct
