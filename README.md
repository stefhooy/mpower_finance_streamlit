# MPower PMEC Reconciliation App

A Streamlit web application that automates the monthly PMEC payment reconciliation for MPower Ventures Zambia. Upload the three government return files for any month and get a structured Excel reconciliation output instantly, with no technical knowledge required.

---

## What it does

Each month, the Zambian government processes MPower's payroll deduction submissions and returns three files. This app reads all three, runs the reconciliation logic, and produces a downloadable Excel workbook with a full breakdown of successful payments, insufficient funds, rejections, and the expected bank transfer amount.

---

## Input files

The app expects the three files that Misozi receives from PMEC each month:

| File | Format | Description |
|---|---|---|
| Successful payment report | `.txt` | Fixed-width government export. Filter by period code (e.g. `202604`). Fields extracted by position: Personnel Area, SubArea, Employee No, Name, NRC, Period, Amount (ZMW). |
| Insufficient funds list | `.xlsx` | Employees whose salary headroom fell below the 30% threshold. Key columns: Employee No., Employee Name, Start Date, End Date, Amount, Reason. Amount can be blank — treated as missing, not zero. |
| Rejection list | `.xlsx` | Hard rejections. SAP/PMEC column names: PERNR, LGART, ENDDA, BEGDA, BETRG, COMMENTS (rejection reason). Known reasons: SEPARATEES, LOCKED, DEATH, DISMISSAL, TERMINATION OF SERVICE, RETIREMENT AT MANDATORY AGE, RESIGNATION WITH NOTICE, UNPAID LEAVE, INVALID EMPLOYEE NUMBER, INVALID END DATE, EXISTING RECORD. |

---

## Output

A five-sheet Excel workbook:

1. **Reconciliation Summary** — totals by category, PMEC fee calculation, expected bank transfer, validation check, and data quality flags
2. **Successful Payments** — full parsed record from the .txt file
3. **Insufficient Funds** — cleaned record from the .xlsx file
4. **Rejections** — cleaned record with rejection reason per employee
5. **Rejection Breakdown** — count and total ZMW per rejection reason category

An optional input field allows the user to enter the actual bank transfer amount received. If provided, the app calculates the implied PMEC fee percentage and flags any discrepancy against the assumed 2% rate.

---

## Data safety

The application is stateless. No data is written to a database, a file system, or any external storage. Uploaded files are processed entirely in memory within the session and discarded when the browser tab is closed. The downloaded Excel file is the only output that leaves the app.

This design was chosen deliberately given that the PMEC files contain Zambian government payroll data (employee identifiers, salary deduction amounts, employment status). The app handles this data in a fully closed pipeline: it enters at upload, is processed in memory, and exits only as the aggregated Excel reconciliation.

---

## Known data quality issues handled

- Insufficient funds records with no amount recorded are flagged in the output, not dropped
- Employees appearing more than once in the rejection file (known PMEC export issue) are flagged, not silently deduplicated
- The successful payment .txt file uses positional parsing — a validation step checks row counts and totals before writing output
- SEPARATEES and LOCKED rejection codes: meanings unconfirmed as of June 2026. A note is shown in the UI until clarified by Misozi.

---

## Setup

```bash
pip install streamlit pandas openpyxl
streamlit run app.py
```

Python 3.9 or later recommended.

---

## Project context

This app wraps the reconciliation logic originally written in `Documents/build_recon.py`, which produced `Deliverable_2_Friday/PMEC_Reconciliation_April2026.xlsx`. The Streamlit interface replaces the hardcoded file paths with a file upload UI so the finance team can run the reconciliation for any month without needing a Python environment.

MPower Ventures AG — Zambia Finance Team  
Internship Deliverable 3, April to June 2026
