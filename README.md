# ConsumerLens India 🇮🇳
**India Household Consumer Spending Intelligence & Data Quality Engine**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65-red.svg)](https://streamlit.io/)
[![Quality Score](https://img.shields.io/badge/Data%20Quality%20Score-100%25-brightgreen.svg)](#data-quality-engine)
[![Tests Passing](https://img.shields.io/badge/Tests-9%20Passed-emerald.svg)](#testing-and-verification)
[![License: Open Govt](https://img.shields.io/badge/Data%20License-OGDL--India-orange.svg)](https://data.gov.in/)

An institutional-grade, audit-ready research intelligence platform analyzing official household consumption expenditure patterns, rural-urban disparities, commodity basket allocations, and inflation dynamics in India. Built with Python, pandas, Streamlit, and Plotly.

---

## 🏛️ Executive Summary

**ConsumerLens India** is designed to demonstrate professional secondary-source research, quantitative triangulation, and deterministic data governance relevant to a **Syndicated Research Associate** or **Quantitative Macro Analyst**.

The application analyzes the official **Household Consumption Expenditure Survey (HCES) 2023–24** (NSS Report No. 592) and **HCES 2022–23** (NSS Report No. 590) released by the National Sample Survey Office (NSSO), Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Official retail inflation from the transitioned **Consumer Price Index (Base 2024=100)** is integrated as decoupled macroeconomic context.

---

## 🔍 Key Empirical Insights

- **Sustained Rural Consumption Momentum:** Average nominal Monthly Per Capita Consumption Expenditure (MPCE) reached **₹4,122** in rural India (+9.2% YoY) and **₹6,996** in urban India (+8.3% YoY).
- **Disparity Compression:** The urban-to-rural consumption premium narrowed to **1.70×** (69.7%), down from 1.71× in 2022–23 and 1.84× in 2011–12.
- **Pro-Poor Bottom-Decile Surge:** The bottom 5% of India's population experienced the fastest consumption growth nationwide: **+22.1% in rural areas** (₹1,677) and **+18.7% in urban areas** (₹2,376).
- **Structural Basket Modernization:** Non-food spending dominates total expenditures (**52.96% rural, 60.32% urban**). Beverages & processed food is now the #1 food spending category nationwide (**9.84% rural, 11.09% urban**), surpassing traditional cereals (**4.99% rural, 3.76% urban**).
- **Social Transfer Imputation Impact:** Imputing the value of free welfare goods (PMGKY foodgrains, school uniforms, cycles, computers) raises rural MPCE to **₹4,247** (+₹125/month) and urban MPCE to **₹7,078** (+₹82/month).
- **Food Share Distinctions:**
  - *HCES 2022–23 (unimputed):* Rural 46.38%, Urban 39.17%
  - *HCES 2023–24 (unimputed):* Rural 47.04%, Urban 39.68%
  - *HCES 2023–24 (with welfare imputation):* Rural 48.43%, Urban 40.31%

---

## 🛠️ System Architecture & Zero-Cost Stack

- **Data Ingestion & Pipeline:** Python 3.11, pandas, NumPy (`src/pipeline.py`)
- **Deterministic Data Quality Engine:** 28 automated checks across 5 dimensions (`src/quality_engine.py`)
- **Interactive UI & Visualizations:** Streamlit, Plotly Express & Graph Objects (`app.py`, `src/ui/`)
- **Testing:** Pytest test suite (`tests/`)
- **Zero Cost Guarantee:** Zero paid APIs, zero runtime LLM dependencies, zero proprietary keys. Operates 100% offline with preserved raw source files and SHA-256 cryptographic verification.

```
india-consumer-spending-intelligence/
├── app.py                      # Master Streamlit Research Application
├── conftest.py                 # Pytest configuration
├── requirements.txt            # Python dependencies
├── src/
│   ├── pipeline.py             # Data ingestion, transformation & ETL
│   ├── quality_engine.py       # Deterministic 28-rule QC engine & CQS formula
│   └── ui/
│       ├── components.py       # Reusable CSS, KPI cards, disclaimer banners
│       └── charts.py           # Polished Plotly chart generators
├── tests/
│   ├── test_pipeline.py        # Pipeline & data integrity tests
│   ├── test_quality_engine.py  # Quality score & corruption detection tests
│   └── test_app.py             # UI loader and chart rendering tests
├── data/
│   ├── raw/                    # Preserved official MoSPI PDFs & HTML releases
│   │   ├── checksums.sha256    # Cryptographic SHA-256 hashes
│   │   ├── HCES_Press_Note_2023-24_27122024_rev.pdf
│   │   ├── Factsheet_HCES_2022-23.pdf
│   │   └── CPI_Release_Aug2026.html
│   └── processed/              # Normalized analytical datasets (CSV & Parquet ready)
│       ├── state_mpce.csv
│       ├── category_shares.csv
│       ├── fractile_distribution.csv
│       ├── cpi_series.csv
│       └── macro_pfce.csv
└── docs/
    ├── PROJECT_BLUEPRINT.md    # Master architecture & specifications
    ├── SOURCE_REGISTER.csv     # Official MoSPI source register & metadata
    ├── DECISION_LOG.md         # Architecture decision records (ADRs)
    ├── VALIDATION_REPORT.json  # Machine-readable automated QC audit log
    ├── DATA_DICTIONARY.md      # Field definitions and data types
    ├── METHODOLOGY.md          # Survey design, CAPI 3-visit, HCES vs PFCE
    └── RESEARCH_BRIEF.md       # Executive research brief for analysts
```

---

## 🧪 Data Quality Engine & Audit Matrix

The built-in engine evaluates 28 deterministic checks across five dimensions:

$$\text{CQS} = \sum_{k=1}^{5} w_k \cdot \left( \frac{\sum_{i=1}^{N_k} \mathbb{I}(\text{Check}_{k,i} = \text{PASS})}{N_k} \right) \times 100 = 100.0\%$$

- **Completeness ($w_1 = 0.25$):** 6 checks passed (100.0%)
- **Validity ($w_2 = 0.25$):** 6 checks passed (100.0%)
- **Uniqueness ($w_3 = 0.15$):** 4 checks passed (100.0%)
- **Internal Consistency ($w_4 = 0.20$):** 8 checks passed (100.0%)
- **Provenance ($w_5 = 0.15$):** 5 checks passed (100.0%)

Full audit records are saved to [`docs/VALIDATION_REPORT.json`](docs/VALIDATION_REPORT.json).

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

### 3. Run Data Pipeline & Quality Engine
```bash
python src/pipeline.py
```

### 4. Launch Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 5. Run Automated Tests
```bash
python -m pytest -v tests/
```

---

## 📚 Official Source Citations
1. **MoSPI HCES 2023–24:** NSS Report No. 592 & Press Note, Dec 27, 2024.
2. **MoSPI HCES 2022–23:** NSS Report No. 590 & Factsheet, Feb / Jun 2024.
3. **MoSPI CPI (Base 2024=100):** PIB PRID 2310058 (August 2026 release).
4. **MoSPI National Accounts Statistics:** Private Final Consumption Expenditure (PFCE), 2023–24.

---
*Authored by Senior Research Analyst & Data Engineer for ConsumerLens India.*
