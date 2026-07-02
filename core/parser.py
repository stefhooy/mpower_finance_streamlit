import pandas as pd
import re


def _detect_period(lines: list[str]) -> str:
    """Return the first 6-digit YYYYMM code found in the file, or '' if none."""
    for line in lines:
        match = re.search(r'\b(20\d{4})\b', line)
        if match:
            return match.group(1)
    return ''


def parse_successful_txt(file) -> pd.DataFrame:
    """Parse the PMEC successful payment fixed-width text file.

    Args:
        file: file-like object from st.file_uploader (or open() in tests)

    Returns:
        DataFrame with columns:
            Personnel Area, Personnel SubArea, Employee No,
            Name, NRC No, Period, Amount (ZMW), Status
    """
    raw = file.read()
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8', errors='replace')
    lines = raw.splitlines()

    period = _detect_period(lines)
    if not period:
        raise ValueError(
            "Could not detect a period code (YYYYMM) in the text file. "
            "Check that you uploaded the correct successful payments file."
        )

    rows = []
    for line in lines:
        if not line.startswith('|'):
            continue
        if period not in line:
            continue
        if 'Total' in line or 'Area' in line:
            continue

        content = line.strip().strip('|')
        parts = content.split()
        if len(parts) < 8:
            continue

        try:
            amount = float(parts[-4].replace(',', ''))
            pers_area = parts[0]
            pers_subarea = parts[1]
            empl_no = parts[2]

            nrc = ''
            name_parts = []
            for p in parts[4:]:
                if '/' in p:
                    nrc = p
                    break
                name_parts.append(p)
            name = ' '.join(name_parts)

            period_val = parts[-6] if parts[-6].startswith('20') else period

            rows.append({
                'Personnel Area': pers_area,
                'Personnel SubArea': pers_subarea,
                'Employee No': empl_no,
                'Name': name,
                'NRC No': nrc,
                'Period': period_val,
                'Amount (ZMW)': amount,
                'Status': 'Successful',
            })
        except (IndexError, ValueError):
            continue

    if not rows:
        raise ValueError(
            f"No payment rows found for period {period}. "
            "Check that the file is the successful payments report."
        )

    return pd.DataFrame(rows)


def parse_insufficient_funds_xlsx(file) -> pd.DataFrame:
    """Parse the PMEC insufficient funds Excel file.

    Returns:
        DataFrame with columns:
            Employee No, Name, Personnel SubArea,
            Start Date, End Date, Amount (ZMW), Reason, Status
    """
    df = pd.read_excel(file)
    df = df.dropna(how='all')
    df.columns = df.columns.str.strip()

    required = {'Employee No.', 'Employee Name', 'Amount'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Insufficient funds file is missing expected columns: {missing}. "
            "Check that you uploaded the correct file."
        )

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Status'] = 'Insufficient Funds'

    out = df[['Employee No.', 'Employee Name', 'Personnel SubArea Text',
              'Start Date', 'End Date', 'Amount', 'Reason', 'Status']].copy()
    out.columns = ['Employee No', 'Name', 'Personnel SubArea',
                   'Start Date', 'End Date', 'Amount (ZMW)', 'Reason', 'Status']
    return out.reset_index(drop=True)


def parse_rejections_xlsx(file) -> pd.DataFrame:
    """Parse the PMEC rejections Excel file.

    Returns:
        DataFrame with columns:
            Employee No, Name, Start Date, End Date,
            Amount (ZMW), Rejection Reason, Status
    """
    df = pd.read_excel(file)
    df = df.dropna(how='all')

    required = {'PERNR', 'FIRST NAME', 'SURNAME', 'BETRG', 'COMMENTS'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Rejections file is missing expected columns: {missing}. "
            "Check that you uploaded the correct file."
        )

    df['BETRG'] = pd.to_numeric(df['BETRG'], errors='coerce')
    df['Status'] = 'Rejected'
    df['Name'] = df['FIRST NAME'].str.strip() + ' ' + df['SURNAME'].str.strip()

    out = df[['PERNR', 'Name', 'BEGDA', 'ENDDA',
              'BETRG', 'COMMENTS', 'Status']].copy()
    out.columns = ['Employee No', 'Name', 'Start Date', 'End Date',
                   'Amount (ZMW)', 'Rejection Reason', 'Status']
    return out.reset_index(drop=True)
