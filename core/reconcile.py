import pandas as pd

PMEC_FEE_PCT = 0.02


def reconcile(
    df_success: pd.DataFrame,
    df_insuf: pd.DataFrame,
    df_rej: pd.DataFrame,
    actual_transfer: float | None = None,
) -> dict:
    """Run the full PMEC reconciliation and return all results in one dict.

    Args:
        df_success: output of parse_successful_txt
        df_insuf:   output of parse_insufficient_funds_xlsx
        df_rej:     output of parse_rejections_xlsx
        actual_transfer: actual ZMW amount received from bank (optional)

    Returns dict keys:
        period, n_successful, total_successful,
        n_insuf, total_insuf, n_insuf_missing_amount,
        n_rej, total_rej, n_rej_duplicate_employees,
        total_implied, pmec_fee, expected_transfer,
        actual_transfer, implied_fee_pct, transfer_discrepancy,
        rej_breakdown (DataFrame)
    """
    # -- Successful --
    n_successful = len(df_success)
    total_successful = df_success['Amount (ZMW)'].sum()
    period = df_success['Period'].iloc[0] if n_successful > 0 else ''

    # -- Insufficient funds --
    n_insuf = len(df_insuf)
    total_insuf = df_insuf['Amount (ZMW)'].sum()
    n_insuf_missing_amount = int(df_insuf['Amount (ZMW)'].isna().sum())

    # -- Rejections --
    n_rej = len(df_rej)
    total_rej = df_rej['Amount (ZMW)'].sum()
    duplicate_mask = df_rej['Employee No'].duplicated(keep=False)
    n_rej_duplicate_employees = int(duplicate_mask.sum())

    # -- Implied total and validation --
    total_implied = total_successful + total_insuf + total_rej

    # -- Bank payment --
    pmec_fee = total_successful * PMEC_FEE_PCT
    expected_transfer = total_successful - pmec_fee

    # -- Optional: compare against actual bank transfer --
    implied_fee_pct = None
    transfer_discrepancy = None
    if actual_transfer is not None and actual_transfer > 0:
        implied_fee_pct = (total_successful - actual_transfer) / total_successful
        transfer_discrepancy = actual_transfer - expected_transfer

    # -- Rejection breakdown by category --
    rej_breakdown = (
        df_rej.groupby('Rejection Reason')
        .agg(Count=('Employee No', 'count'), Total_ZMW=('Amount (ZMW)', 'sum'))
        .reset_index()
        .sort_values('Count', ascending=False)
        .rename(columns={'Total_ZMW': 'Amount (ZMW)'})
    )

    return {
        'period': period,
        'n_successful': n_successful,
        'total_successful': total_successful,
        'n_insuf': n_insuf,
        'total_insuf': total_insuf,
        'n_insuf_missing_amount': n_insuf_missing_amount,
        'n_rej': n_rej,
        'total_rej': total_rej,
        'n_rej_duplicate_employees': n_rej_duplicate_employees,
        'total_implied': total_implied,
        'pmec_fee': pmec_fee,
        'expected_transfer': expected_transfer,
        'actual_transfer': actual_transfer,
        'implied_fee_pct': implied_fee_pct,
        'transfer_discrepancy': transfer_discrepancy,
        'rej_breakdown': rej_breakdown,
    }
