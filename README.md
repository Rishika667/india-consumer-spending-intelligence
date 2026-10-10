# ConsumerLens India 🇮🇳
**India Household Consumer Spending Intelligence & Data Quality Engine**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65-red.svg)](https://streamlit.io/)
[![Pipeline Validation](https://img.shields.io/badge/Pipeline%20Validation-100%25%20(28%2F28%20Checks)-brightgreen.svg)](#pipeline-validation-engine)
[![Source Reconciliation](https://img.shields.io/badge/Source%20Reconciliation-100%25%20(42%2F42%20Matched)-blue.svg)](#source-reconciliation-engine)
[![Tests Passing](https://img.shields.io/badge/Tests-Passing-emerald.svg)](#testing-and-verification)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Data License: OGDL-India](https://img.shields.io/badge/Data%20License-OGDL--India-orange.svg)](https://data.gov.in/)

An editorial research intelligence application analyzing official Indian household consumption expenditure patterns, rural-urban disparities, commodity basket allocations, and retail price dynamics. Built with Python, pandas, Streamlit, and Plotly for secondary research and macroeconomic analysis.

---

## 🏛️ Executive Summary

**ConsumerLens India** is designed to demonstrate professional secondary-source research, quantitative triangulation, and deterministic data governance relevant to a **Syndicated Research Associate** or **Quantitative Macro Analyst**.

The application analyzes the official **Household Consumption Expenditure Survey (HCES) 2023–24** (NSS Report No. 592 & PIB PRID 2247612) and **HCES 2022–23** (NSS Report No. 590) released by the National Sample Survey Office (NSSO), Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Official retail inflation from the transitioned **Consumer Price Index (Base 2024=100)** is integrated as decoupled macroeconomic context.

*Note: ConsumerLens India is designed to run locally or self-hosted in a Python 3.11 environment with zero paid external APIs or runtime LLM dependencies.*

---

## 🔍 Key Empirical Insights

- **Nominal Rural and Urban MPCE Growth:** Average nominal Monthly Per Capita Consumption Expenditure (MPCE) reached **₹4,122** in rural India (+9.2% YoY) and **₹6,996** in urban India (+8.3% YoY). Deflated to constant 2011–12 prices, real MPCE stands at **₹2,079 rural** and **₹3,632 urban**.
- **Ratio Compression vs. Expanding Rupee Gap:** The national urban-to-rural consumption premium narrowed to **1.70×** (69.7% premium), down from 1.71× in 2022–23 and 1.84× in 2011–12 (and 1.67× under welfare imputation). However, the absolute monthly per-capita spending gap widened to **₹2,874/month** (up from ₹2,686 in 2022–23).
- **State Coverage Rigor:** 34 States/UTs published for out-of-pocket (unimputed) MPCE in 2023-24 (with Delhi and Chandigarh retained as explicit unpublished cells), and 36 States/UTs published with social welfare imputation.
- **Bottom-Fractile Growth & Quintile Concentration:** The bottom 5% fractile class recorded notable percentage increases nationwide: **+22.1% in rural areas** (₹1,677) and **+18.7% in urban areas** (₹2,376). Within 2023–24, the top-to-bottom MPCE ratio was **6.04× rural** (top 5%: ₹10,137) and **8.55× urban** (top 5%: ₹20,310).
- **Budget Allocation Observations:** Non-food spending accounts for **52.96% rural and 60.30% urban** unimputed budgets. The rural food share was already below 50% in 2022–23 (46.38% unimputed, 47.47% imputed), rising slightly to 47.04% unimputed and 48.43% imputed in 2023–24. Within food, beverages and processed goods represent the largest share (**9.84% rural, 11.09% urban**), while cereal shares edged up to **4.99% rural and 3.76% urban** between rounds.
- **Social Transfer Imputation Impact:** Imputing the value of free welfare goods (PMGKY foodgrains, school uniforms, cycles, computers) at local market prices raises rural MPCE to **₹4,247** (+₹125/month) and urban MPCE to **₹7,078** (+₹82/month). Fractile-level and item-level imputed series were not published for 2023–24.
- **Food Share Distinctions:**
  - *HCES 2022–23 (unimputed):* Rural 46.38%, Urban 39.16% (Statement 5 category sum; published aggregate is 39.17%)
  - *HCES 2022–23 (with welfare imputation):* Rural 47.47%, Urban 39.70% (Statement 15)
  - *HCES 2023–24 (unimputed):* Rural 47.04%, Urban 39.68% (Figures 4 & 5)
  - *HCES 2023–24 (with welfare imputation aggregate):* Rural 48.43%, Urban 40.31% (Report 592 text; item-level group breakdown unpublished by MoSPI)
- **CPI 2024-Base Coverage:** 20-month General Index series (January 2025 – August 2026), 8 months of YoY general inflation (January 2026 – August 2026, headline 4.82% in Aug 2026), and 2 months of CFPI food inflation (July & August 2026, 5.95% in Aug 2026). YoY inflation is available for 8 months because 2024 monthly indices were not published in Table 10 of PIB PRID 2310058.

---

## 🛠️ System Architecture & Stack

- **Data Ingestion & Pipeline:** Python 3.11, pandas, NumPy (`src/pipeline.py`) ingesting from structured source tables (`data/sources/`)
- **Deterministic Pipeline Validation Engine:** Exactly 28 automated checks across 5 dimensions (`src/quality_engine.py`)
- **Primary Source Reconciliation Engine:** Automated benchmark reconciliation against raw PDFs/HTML (`scripts/reconcile_sources.py`)
- **Interactive UI & Visualizations:** Streamlit, Plotly Express & Graph Objects (`app.py`, `src/ui/`)
- **Continuous Integration:** GitHub Actions (`.github/workflows/ci.yml`)
- **Testing:** Pytest test suite (`tests/`)
- **Self-Contained & Reproducible Architecture:** Requires no paid APIs, runtime LLM dependencies, or external credential services. Operates offline with preserved official raw source extracts, deterministic data transformations, and cryptographic SHA-256 verification.

```
india-consumer-spending-intelligence/
├── app.py                      # Master Streamlit Research Application
├── conftest.py                 # Pytest configuration
├── requirements.txt            # Python dependencies
├── LICENSE                     # Dual licensing (MIT Code + OGDL-India Data)
├── scripts/
│   ├── build_source_tables.py  # Generates curated source tables in data/sources/
│   └── reconcile_sources.py    # Bidirectionally reconciles 42 benchmarks against raw docs
├── src/
│   ├── pipeline.py             # Data ingestion, transformation & ETL
│   ├── quality_engine.py       # Deterministic 28-rule validation engine
│   └── ui/
│       ├── components.py       # Reusable CSS, KPI cards, disclaimer banners
│       └── charts.py           # Polished Plotly chart generators (CFPI + state harmonized)
├── tests/
│   ├── test_pipeline.py        # Pipeline & data integrity tests
│   ├── test_quality_engine.py  # 28-check QC audit & corruption detection tests
│   ├── test_reconciliation.py  # Source reconciliation gate & corruption tests
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
    ├── DECISION_LOG.md         # Architecture decision records (ADRs 1–11)
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

- **Total Primary Benchmarks Checked:** 42 machine-checked benchmarks
- **Primary Source Documents Searched:** `HCES_Press_Note_2023-24_27122024_rev.pdf`, `Factsheet_HCES_2022-23.pdf`, `HCES_2023-24_PIB_2247612.html`, `CPI_Release_Aug2026.html`
- **Matched Records:** 42 / 42 (100.0% Match Rate)
- **Verified Discrepancies Reconciled:** Goa, Himachal Pradesh, Uttarakhand, Dadra & Nagar Haveli and Daman & Diu, Haryana, Punjab, Delhi (explicit NaN), Chandigarh (unimputed explicit NaN), 2022-23 urban food share 39.16% (category sum) vs 39.17% (aggregate).

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

### 7. Streamlit Community Cloud Deployment
To host this application publicly at zero cost:
1. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"** and specify the following deployment parameters:
   - **Repository:** `Rishika667/india-consumer-spending-intelligence`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Deploy!"**. The platform automatically installs dependencies from `requirements.txt` and serves the application on a public URL.

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
