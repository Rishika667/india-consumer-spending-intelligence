# ConsumerLens India 🇮🇳
**India Household Consumer Spending Intelligence & Data Quality Engine**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65-red.svg)](https://streamlit.io/)
[![Pipeline Validation](https://img.shields.io/badge/Pipeline%20Validation-100%25%20(28%2F28%20Checks)-brightgreen.svg)](#pipeline-validation-engine)
[![Source Reconciliation](https://img.shields.io/badge/Source%20Reconciliation-100%25%20(23%2F23%20Matched)-blue.svg)](#source-reconciliation-engine)
[![Tests Passing](https://img.shields.io/badge/Tests-9%20Passed-emerald.svg)](#testing-and-verification)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Data License: OGDL-India](https://img.shields.io/badge/Data%20License-OGDL--India-orange.svg)](https://data.gov.in/)

An institutional-grade, audit-ready research intelligence platform analyzing official household consumption expenditure patterns, rural-urban disparities, commodity basket allocations, and retail price dynamics in India. Built with Python, pandas, Streamlit, and Plotly.

---

## 🏛️ Executive Summary

**ConsumerLens India** is designed to demonstrate professional secondary-source research, quantitative triangulation, and deterministic data governance relevant to a **Syndicated Research Associate** or **Quantitative Macro Analyst**.

The application analyzes the official **Household Consumption Expenditure Survey (HCES) 2023–24** (NSS Report No. 592 & PIB PRID 2247612) and **HCES 2022–23** (NSS Report No. 590) released by the National Sample Survey Office (NSSO), Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Official retail inflation from the transitioned **Consumer Price Index (Base 2024=100)** is integrated as decoupled macroeconomic context.

---

## 🔍 Key Empirical Insights

- **Sustained Rural Consumption Momentum:** Average nominal Monthly Per Capita Consumption Expenditure (MPCE) reached **₹4,122** in rural India (+9.2% YoY) and **₹6,996** in urban India (+8.3% YoY).
- **Disparity Compression:** The urban-to-rural consumption premium narrowed to **1.70×** (69.7%), down from 1.71× in 2022–23 and 1.84× in 2011–12.
- **Bottom-Fractile Growth:** The bottom 5% fractile class recorded notable percentage increases nationwide: **+22.1% in rural areas** (₹1,677) and **+18.7% in urban areas** (₹2,376).
- **Descriptive Shift in Spending Allocations:** Non-food spending accounts for **52.96% rural and 60.30% urban** budgets. Within food, spending has shifted toward processed refreshments, milk, and vegetables relative to basic cereals (**4.99% rural, 3.76% urban**).
- **Social Transfer Imputation Impact:** Imputing the value of free welfare goods (PMGKY foodgrains, school uniforms, cycles, computers) raises rural MPCE to **₹4,247** (+₹125/month) and urban MPCE to **₹7,078** (+₹82/month).
- **Food Share Distinctions:**
  - *HCES 2022–23 (unimputed):* Rural 46.38%, Urban 39.16% (Statement 5)
  - *HCES 2022–23 (with welfare imputation):* Rural 47.47%, Urban 39.70% (Statement 15)
  - *HCES 2023–24 (unimputed):* Rural 47.04%, Urban 39.68% (Figures 4 & 5)
  - *HCES 2023–24 (with welfare imputation aggregate):* Rural 48.43%, Urban 40.31% (Report 592 text; item-level group breakdown unpublished by MoSPI)
- **CPI 2024-Base Coverage:** 20-month General Index series (January 2025 – August 2026), 8 months of YoY general inflation (January 2026 – August 2026, headline 4.82% in Aug 2026), and 2 months of CFPI food inflation (July & August 2026, 5.95% in Aug 2026). YoY inflation is available for 8 months because 2024 monthly indices were not published in Table 10 of PIB PRID 2310058.

---

## 🛠️ System Architecture & Zero-Cost Stack

- **Data Ingestion & Pipeline:** Python 3.11, pandas, NumPy (`src/pipeline.py`) ingesting from structured source tables (`data/sources/`)
- **Deterministic Pipeline Validation Engine:** Exactly 28 automated checks across 5 dimensions (`src/quality_engine.py`)
- **Primary Source Reconciliation Engine:** Automated benchmark reconciliation against raw PDFs/HTML (`scripts/reconcile_sources.py`)
- **Interactive UI & Visualizations:** Streamlit, Plotly Express & Graph Objects (`app.py`, `src/ui/`)
- **Testing:** Pytest test suite (`tests/`)
- **Zero Cost Guarantee:** Zero paid APIs, zero runtime LLM dependencies, zero proprietary keys. Operates 100% offline with preserved raw source files and SHA-256 cryptographic verification.

```
india-consumer-spending-intelligence/
├── app.py                      # Master Streamlit Research Application
├── conftest.py                 # Pytest configuration
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── build_source_tables.py  # Generates curated source tables in data/sources/
│   └── reconcile_sources.py    # Reconciles 23 primary benchmarks against raw documents
├── src/
│   ├── pipeline.py             # Data ingestion, transformation & ETL
│   ├── quality_engine.py       # Deterministic 28-rule validation engine
│   └── ui/
│       ├── components.py       # Reusable CSS, KPI cards, disclaimer banners
│       └── charts.py           # Polished Plotly chart generators (CFPI + state harmonized)
├── tests/
│   ├── test_pipeline.py        # Pipeline & data integrity tests
│   ├── test_quality_engine.py  # 28-check QC audit & corruption detection tests
│   └── test_app.py             # UI loader and chart rendering tests
├── data/
│   ├── raw/                    # Preserved official MoSPI PDFs & HTML releases
│   │   ├── checksums.sha256    # Cryptographic SHA-256 hashes
│   │   ├── HCES_Press_Note_2023-24_27122024_rev.pdf
│   │   ├── HCES_2023-24_PIB_2247612.html
│   │   ├── HCES_2023-24_PIB_2088390.html
│   │   ├── Factsheet_HCES_2022-23.pdf
│   │   ├── Factsheet_HCES_2023-24_PIB.pdf
│   │   └── CPI_Release_Aug2026.html
│   ├── sources/                # Structured, documented source CSVs with table refs
│   │   ├── source_state_mpce_2022_23.csv
│   │   ├── source_state_mpce_2023_24.csv
│   │   ├── source_category_shares.csv
│   │   ├── source_fractile_distribution.csv
│   │   ├── source_national_trajectory.csv
│   │   ├── source_cpi_monthly_2024_base.csv
│   │   ├── source_cpi_historical_2012_base_snapshot.csv
│   │   └── source_macro_pfce.csv
│   └── processed/              # Normalized analytical datasets
│       ├── state_mpce.csv
│       ├── category_shares.csv
│       ├── fractile_distribution.csv
│       ├── national_trajectory.csv
│       ├── cpi_series.csv
│       └── macro_pfce.csv
└── docs/
    ├── PROJECT_BLUEPRINT.md    # Master architecture & specifications
    ├── SOURCE_REGISTER.csv     # Official MoSPI source register & metadata
    ├── SOURCE_RECONCILIATION.md# Primary source reconciliation audit report
    ├── SOURCE_RECONCILIATION.json# Machine-readable benchmark reconciliation log
    ├── DECISION_LOG.md         # Architecture decision records (ADRs 1–10)
    ├── VALIDATION_REPORT.json  # Machine-readable automated 28-rule audit log
    ├── DATA_DICTIONARY.md      # Field definitions and data types
    ├── METHODOLOGY.md          # Survey design, CAPI 3-visit, HCES vs PFCE
    └── RESEARCH_BRIEF.md       # Executive research brief for analysts
```

---

## 🧪 Pipeline Validation Engine

The deterministic validation engine audits datasets against exactly 28 checks across five dimensions:

$$\text{Pipeline Validation Score} = \sum_{k=1}^{5} w_k \cdot \left( \frac{\sum_{i=1}^{N_k} \mathbb{I}(\text{Check}_{k,i} = \text{PASS})}{N_k} \right) \times 100 = 100.0\%$$

- **Completeness ($w_1 = 0.25$):** 6 checks passed (100.0%)
- **Validity ($w_2 = 0.25$):** 6 checks passed (100.0%)
- **Uniqueness ($w_3 = 0.15$):** 4 checks passed (100.0%)
- **Internal Consistency ($w_4 = 0.20$):** 7 checks passed (100.0%)
- **Provenance ($w_5 = 0.15$):** 5 checks passed (100.0%)

> **Methodological Disclaimer:** The Pipeline Validation Score evaluates automated data pipeline hygiene, deterministic schema constraints, aggregation consistency, and cryptographic file matching. It does **not** assert statistical sampling precision, representativeness, or absolute accuracy of the underlying MoSPI NSSO survey design.

---

## 🔍 Source Reconciliation Engine

Key curated benchmarks are programmatically verified against preserved primary source documents using `scripts/reconcile_sources.py`:

- **Total Primary Benchmarks Checked:** 23
- **Primary Source Documents Searched:** `HCES_Press_Note_2023-24_27122024_rev.pdf`, `Factsheet_HCES_2022-23.pdf`, `HCES_2023-24_PIB_2247612.html`, `CPI_Release_Aug2026.html`
- **Matched Records:** 23 / 23 (100.0% Match Rate)
- **Verified Discrepancies Reconciled:** Goa, Himachal Pradesh, Uttarakhand, Dadra & Nagar Haveli and Daman & Diu, Haryana, Punjab, Delhi (explicit NaN).

---

## 🚀 Setup & Local Run Instructions

### 1. Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Rishika667/india-consumer-spending-intelligence.git
cd india-consumer-spending-intelligence

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Source Verification & Reconciliation
```bash
python scripts/reconcile_sources.py
```

### 4. Run Data Pipeline & Quality Engine
```bash
python src/pipeline.py
```

### 5. Launch Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 6. Run Automated Tests
```bash
python -m pytest -v tests/
```

---

## 📚 Official Source Citations
1. **MoSPI HCES 2023–24:** NSS Report No. 592 & PIB PRID 2247612 (Dec 27, 2024 / Aug 2025).
2. **MoSPI HCES 2022–23:** NSS Report No. 590 & Factsheet, Feb / Jun 2024.
3. **MoSPI CPI (Base 2024=100):** PIB PRID 2310058 (August 2026 release).
4. **MoSPI National Accounts Statistics:** Private Final Consumption Expenditure (PFCE), 2023–24.

---

## ⚖️ License
- **Code:** [MIT License](https://opensource.org/licenses/MIT)
- **Data:** [Open Government Data License - India (OGDL-India)](https://data.gov.in/)
