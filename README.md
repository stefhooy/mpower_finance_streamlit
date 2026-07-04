# MPower PMEC Reconciliation App

![African geometric design](assets/african_design_1.png)

<p align="center">
  <img src="assets/mpower_africa_logo.jpg" alt="MPower Ventures AG" height="100">
</p>

A Streamlit web application that automates the monthly PMEC payment reconciliation for MPower Ventures Zambia. Upload the three government return files for any month and get a structured Excel reconciliation output instantly, with no technical knowledge required.

---

## What it does

Each month, the Zambian government processes MPower's payroll deduction submissions and returns three files. This app reads all three, runs the reconciliation logic, and produces a downloadable Excel workbook with a full breakdown of successful payments, insufficient funds, rejections, and the expected bank transfer amount.

---

## Input files

The app expects the three files that Misozi receives from PMEC each month:

| File | Format | Description |
|---|---|---|
| Successful payment report | `.txt` | Fixed-width government export, e.g. `E892 - MPower Ventures Zambia.txt`. Rows beginning with a pipe character that contain the period code (e.g. `202604`) are parsed by position: Personnel Area, SubArea, Employee No, Name, NRC, Period, Amount (ZMW). |
| Insufficient funds list | `.xlsx` | Employees whose salary headroom fell below the 30% threshold, e.g. `E892.xlsx`. Required columns: Employee No., Employee Name, Personnel SubArea Text, Start Date, End Date, Amount, Reason. Amount can be blank, treated as missing rather than zero. |
| Rejection list | `.xlsx` | Hard rejections, e.g. `E892 R.xlsx`. SAP/PMEC column names: PERNR, FIRST NAME, SURNAME, BEGDA, ENDDA, BETRG, COMMENTS. Known reasons: SEPARATEES, LOCKED, DEATH, DISMISSAL, TERMINATION OF SERVICE, RETIREMENT AT MANDATORY AGE, RESIGNATION WITH NOTICE, UNPAID LEAVE, INVALID EMPLOYEE NUMBER, INVALID END DATE, EXISTING RECORD. |

---

## Output

A seven-sheet Excel workbook, downloaded directly from the browser:

| Sheet | Contents |
|---|---|
| `1_Reconciliation_Summary` | Totals by category, PMEC fee calculation, expected bank transfer, and data quality flags |
| `2_Successful_Payments` | Full parsed record from the .txt file |
| `3_Insufficient_Funds` | Cleaned record from the insufficient funds .xlsx |
| `4_Rejections` | Cleaned record with rejection reason per employee |
| `5a_Success_Breakdown` | Successful payments grouped by Personnel Area |
| `5b_Insuf_Breakdown` | Insufficient funds grouped by Reason |
| `5c_Rejection_Breakdown` | Rejections grouped by rejection category |

The PMEC fee percentage defaults to 2% but can be changed in the UI before running if the rate differs that month.

---

## UI overview

The app is designed for non-technical users:

- **Header** with the MPower logo
- **Step-by-step guide** explaining which file goes where
- **File upload section** with one slot per file, accepting only the correct format
- **PMEC fee input** to override the default 2% rate if needed
- **Reconciliation dashboard** showing totals, the expected bank transfer card, data quality flags, and breakdown tabs
- **Green Excel download button** to save the workbook

---

## Data safety

The application is stateless. No data is written to a database, a file system, or any external storage. Uploaded files are processed entirely in memory within the session and discarded when the browser tab is closed. The downloaded Excel file is the only output that leaves the app.

This design was chosen deliberately given that the PMEC files contain Zambian government payroll data (employee identifiers, salary deduction amounts, employment status). The app handles this data in a fully closed pipeline: it enters at upload, is processed in memory, and exits only as the aggregated Excel reconciliation.

---

## Known data quality issues handled

- Insufficient funds records with no amount recorded are flagged in the output, not dropped
- Employees appearing more than once in the rejection file (known PMEC export issue) are flagged, not silently deduplicated
- The successful payment .txt file uses positional parsing with period-code detection via regex so it works for any future month without code changes
- SEPARATEES and LOCKED rejection codes: meanings unconfirmed as of June 2026. A note is shown in the file guide until clarified with PMEC directly.

---

## Setup

Requires Python 3.10 or later. Uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# 1. Create the virtual environment
uv venv

# 2. Activate it (Windows)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
uv sync

# 4. Run the app
streamlit run app.py
```

Dependencies are declared in `pyproject.toml`:

```toml
[project]
dependencies = [
    "streamlit>=1.35.0",
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",
]
```

---

## Project structure

```text
mpower_finance_streamlit/
├── app.py                    # Streamlit entry point
├── pyproject.toml            # uv dependencies
├── .streamlit/
│   └── config.toml           # Dark theme config
├── assets/
│   ├── mpower_africa_logo.jpg
│   └── african_design_1.png
├── core/
│   ├── parser.py             # Parses all three PMEC return files
│   ├── reconcile.py          # Reconciliation logic and breakdowns
│   └── export.py             # Builds the 7-sheet Excel workbook
└── ui/
    ├── styles.py             # Dark navy + African geometric CSS
    ├── upload.py             # File uploaders and fee input
    └── summary.py            # Reconciliation dashboard rendering
```

---

## Project context

This app wraps the reconciliation logic originally written in `build_recon.py`, which produced the April 2026 Excel reconciliation. The Streamlit interface replaces hardcoded file paths with a file upload UI so Misozi and the finance team can run the reconciliation for any month without needing a Python environment.

MPower Ventures AG — Zambia Finance Team
Internship Deliverable 3, April to June 2026
