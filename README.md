# Retail Data Cleaning & Analytics

An end-to-end Python data cleaning and analytics project built using **Python, Pandas, Matplotlib, and Streamlit**.

The project processes retail transaction data, identifies data quality issues, removes duplicate records, generates reports, and provides an interactive analytics dashboard.

## Project Overview

The project uses the Online Retail dataset to demonstrate a practical data cleaning and analytics workflow.

### Key Features

- Data auditing and quality assessment
- Duplicate record detection and removal
- Missing value analysis
- Data type conversion and standardization
- Data validation and quality reporting
- Automated Excel and CSV report generation
- Interactive Streamlit dashboard
- Retail sales and revenue analysis
- Country-wise transaction analysis
- Dataset filtering and CSV downloads

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- OpenPyXL
- Git and GitHub

## Project Structure

```text
Retail-data-cleaning-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── visualizations/
│
├── screenshots/
│
├── src/
│   ├── clean_data.py
│   ├── generate_report.py
│   └── visualize_data.py
│
├── dashboard.py
├── data_audit.py
├── main.py
├── requirements.txt
└── README.md
```

## Data Cleaning Results

| Metric | Result |
|---|---:|
| Original Records | 541,909 |
| Final Records | 536,641 |
| Duplicates Removed | 5,268 |
| Remaining Duplicates | 0 |
| Missing Customer IDs | 135,037 |
| Missing Descriptions | 1,454 |
| Countries Covered | 38 |

Missing values and business-relevant records such as returns and cancelled invoices are retained and reported rather than blindly deleted.

## Dashboard Features

The Streamlit dashboard includes:

1. Executive Overview
2. Data Quality Analysis
3. Retail Sales Analysis
4. Dataset Explorer

## How to Run

Clone the repository:

```bash
git clone https://github.com/Suriya2404/Retail-data-cleaning-analytics.git
```

Navigate into the project:

```bash
cd Retail-data-cleaning-analytics
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard.py
```

## Dataset

Dataset: Online Retail

Source: UCI Machine Learning Repository / Kaggle distribution.

The raw and processed datasets are excluded from this repository to keep the GitHub repository lightweight.

## Author

**Suriya**

B.Tech – Computer Science (AI & ML)

GitHub: https://github.com/Suriya2404

---

*Built as a practical data cleaning and analytics portfolio project.*