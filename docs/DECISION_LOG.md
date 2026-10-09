# Decision Log — ConsumerLens India
**India Consumer Spending Intelligence & Data Quality Engine**  
**Repository:** `https://github.com/Rishika667/india-consumer-spending-intelligence.git`  
**Current Date:** October 2026

This document records the architectural, methodological, and data engineering decisions made for **ConsumerLens India**. Each decision includes the problem context, chosen decision, alternatives considered and rejected, supporting evidence, unresolved issues, and fallback mechanisms.

---

## Decision 1: Primary Consumption Dataset — Official Published NSS Report No. 592 Tables vs. NADA Unit-Level Microdata

- **Status:** APPROVED & IMPLEMENTED
- **Context:** HCES 2023-24 collects household spending across 261,953 households. We need to determine the primary ingestion foundation for state, regional, fractile, and category spending analytics.
- **Decision:** Establish the verified MoSPI NSS Report No. 592 / PIB Factsheet (Statements 1 to 8, Figures 1 to 9, and Press Note) as the primary, production-grade tabular dataset. Simultaneously, engineer the pipeline to accept optional unit-level microdata CSV/Parquet extracts if provided locally by an authenticated researcher.
- **Rejected Alternatives:**
  - *Alternative A: Rely exclusively on unauthenticated web-scraping of `microdata.gov.in`.* Rejected because MoSPI's NADA microdata portal explicitly requires authenticated user registration and session login (`/auth/login?destination=catalog/237/get-microdata`), blocking headless open-source pipelines.
  - *Alternative B: Synthetic/simulated microdata generation.* Rejected because synthetic microdata violates research integrity principles and does not represent official government statistics.
  - *Alternative C: Using only outdated 2011-12 (68th round) microdata.* Rejected because 2011-12 data is more than a decade old and precedes significant structural transformations in Indian household spending.
- **Evidence:** 
  - Live probe of `https://microdata.gov.in/NADA/index.php/catalog/237/get-microdata` confirmed HTTP redirect to `/auth/login`.
  - MoSPI Press Note (`HCES_Press_Note_2023-24_27122024_rev.pdf`) and PIB PRID 2088390 provide complete, verified figures for All-India and 18 major States, plus extreme States/UTs, across rural and urban sectors, fractile deciles, and detailed commodity groups.
- **Unresolved Issues:** The detailed multi-variable cross-tabulations (e.g., district-level or specific occupation codes) are only available in unit-level microdata.
- **Fallback:** If a user possesses authenticated microdata, a modular `MicrodataAdapter` interface will parse unit-level records into the analytical schema. Otherwise, the app runs deterministically on the verified MoSPI official dataset.

---

## Decision 2: Decoupled Architectural Separation Between Household Expenditure (HCES) and Price Indices (CPI)

- **Status:** APPROVED & IMPLEMENTED
- **Context:** End users often conflate expenditure growth with volume growth or price inflation. A syndicated research associate must maintain strict methodological boundaries between expenditure surveys and price indices.
- **Decision:** Architect the dashboard into strictly separate tabs/modules: Section 1-3 for Household Expenditure (HCES), Section 4 for Price Context (CPI), and Section 6 for Methodology. CPI data is explicitly labelled as **"Separate Macroeconomic Price Context"** with unambiguous disclaimer banners stating that CPI movements must not be interpreted as causal drivers of HCES spending changes.
- **Rejected Alternatives:**
  - *Alternative A: Deflating state-level HCES 2023-24 spending using state-level CPI indices to present "real" state expenditure.* Rejected because MoSPI explicitly cautions against ad-hoc spatial deflation; state CPI series have differing baseline weights and price collection baskets that are not calibrated for spatial cost-of-living parity.
  - *Alternative B: Merging HCES and CPI into a unified composite metric.* Rejected as methodologically ungrounded and statistically invalid.
- **Evidence:** MoSPI Methodological Note on CPI and HCES emphasizes that HCES measures out-of-pocket nominal consumption expenditure, while CPI measures the price trajectory of a fixed basket of goods.
- **Unresolved Issues:** Users often ask "how much of MPCE growth was real vs inflation?". 
- **Fallback:** Provide the official all-India constant-price MPCE comparison computed by MoSPI (using 2011-12 base CPI deflator as officially published in Table 1 & Table 2) alongside a clear educational note on deflation boundaries: Rural constant MPCE rose from ₹1,430 (2011-12) to ₹2,079 (2023-24 unimputed) and ₹2,142 (imputed); Urban constant MPCE rose from ₹2,630 (2011-12) to ₹3,632 (2023-24 unimputed) and ₹3,674 (imputed).

---

## Decision 3: CPI Base-Year Transition Strategy (Base 2012=100 vs. Base 2024=100)

- **Status:** APPROVED & IMPLEMENTED
- **Context:** MoSPI introduced the revised CPI series with Base 2024=100 in early 2026 (first release on February 12, 2026; latest verified release August 2026 with headline inflation 4.82%), updating the basket to 358 items and incorporating HCES 2023-24 weights. Historical time-series data up to 2025 operates under Base 2012=100.
- **Decision:** Support both series in Section 4 (Price Context) as distinct sub-modules:
  1. *Historical Price Trends (2014–2025, Base 2012=100):* Used for long-term longitudinal inflation dynamics.
  2. *Modern Transition Series (Base 2024=100, August 2026 release):* Highlights the updated weighting diagram derived from HCES 2023-24, COICOP 2018 classification, and inclusion of modern consumption items (e.g., streaming services, online markets).
  3. Include a prominent methodological alert noting that MoSPI prohibits direct splicing or chaining between the two series without statistical adjustment.
- **Rejected Alternatives:**
  - *Alternative A: Mechanically splicing the 2012 and 2024 series with a simple ratio multiplier.* Rejected because item baskets, market samples (1,465 rural + 1,395 urban + 12 online), and classification systems (COICOP 2018) differ fundamentally.
  - *Alternative B: Ignoring the 2024 base series completely.* Rejected because demonstrating knowledge of the 2026 base revision is critical for an institutional-grade research analyst profile.
- **Evidence:** Official MoSPI notification on Base Revision and PIB PRID 2310058 (August 2026 release).
- **Unresolved Issues:** The 2024-base series has a shorter historical time horizon.
- **Fallback:** Present the 2024-base series primarily through its weighting diagram and August 2026 release readouts, while maintaining the 2012=100 series for multi-year trend analysis.

---

## Decision 4: Treatment of National Accounts Statistics (PFCE)

- **Status:** APPROVED & IMPLEMENTED
- **Context:** The prompt specifies including official national accounts / Private Final Consumption Expenditure (PFCE) data *only if it adds useful, compatible context*.
- **Decision:** Include PFCE strictly as an educational and methodological comparison module within Section 6 (Methodology & Downloads), rather than blending it into the main consumption dashboard. Highlight the persistent divergence between macro-level PFCE (domestic absorption: ₹178.6 lakh crore in 2023-24, ~60.2% of GDP) and micro-level HCES (household survey out-of-pocket spending).
- **Rejected Alternatives:**
  - *Alternative A: Combining PFCE and HCES on the same time-series chart.* Rejected because PFCE includes non-profit institutions serving households (NPISH), imputed owner-occupied rent, and FISIM, whereas HCES covers only surveyed resident households.
  - *Alternative B: Omitting PFCE entirely.* Rejected because explaining the HCES vs PFCE divergence is a hallmark of institutional economic research and demonstrates rigorous understanding of Indian official statistics.
- **Evidence:** Reserve Bank of India (RBI) and MoSPI technical papers consistently document that household survey estimates typically account for ~45–50% of aggregate national accounts PFCE due to conceptual differences and top-fractile under-reporting.
- **Unresolved Issues:** PFCE data is only available at the national level, with no state-wise disaggregation.
- **Fallback:** Confine PFCE to national-level conceptual comparison tables with clear reconciliation notes.

---

## Decision 5: Tech Stack, Dependencies & Hosting Architecture

- **Status:** APPROVED & IMPLEMENTED
- **Context:** The application must be fast, interactive, reproducible, zero-cost, recruiter-ready, and devoid of paid APIs, proprietary keys, or runtime LLM dependencies.
- **Decision:**
  - **Core Runtime:** Python 3.11
  - **Data Processing:** `pandas` (>= 2.0.0), `numpy` (>= 1.24.0)
  - **Interactive UI:** `streamlit` (>= 1.30.0)
  - **Visualizations:** `plotly` (>= 5.18.0)
  - **Testing:** `pytest` (>= 8.0.0)
  - **Data Storage:** Normalized CSV and Parquet files stored locally under `data/processed/` with raw preservation in `data/raw/`
  - **Zero external API dependencies:** Pipeline operates 100% offline using deterministic ingested datasets.
- **Rejected Alternatives:**
  - *Alternative A: Calling external LLM APIs (OpenAI, Gemini) at runtime to generate chart commentary.* Rejected by project constraints (no paid APIs, no runtime LLM dependency, no secrets).
  - *Alternative B: Complex full-stack React/Node + FastAPI setup.* Rejected because Streamlit provides the standard research-analyst environment, rapid reproducibility, and native Python data science integration.
- **Evidence:** Streamlit + Plotly delivers sub-second load times, interactive cross-filtering, clean tabular exports, and zero deployment friction on Streamlit Community Cloud or local environments.
- **Unresolved Issues:** None.
- **Fallback:** Use `@st.cache_data` for all data ingestion, transformations, and calculation routines to guarantee instantaneous UI responsiveness.

---

## Decision 6: Deterministic Data Quality Engine & Composite Quality Scoring Formulation

- **Status:** APPROVED & IMPLEMENTED
- **Context:** The product requires a transparent, reproducible data-quality engine evaluating completeness, validity, uniqueness, internal consistency, and provenance. Black-box or subjective quality scores must be avoided.
- **Decision:** Implement a deterministic Data Quality Engine (`src/quality_engine.py`) that executes 25+ automated validation rules. The Composite Quality Score (CQS) is calculated via a published, transparent mathematical formula:
  $$\text{CQS} = \sum_{k=1}^{M} w_k \cdot \left( \frac{\text{Passed Checks}_k}{\text{Total Applicable Checks}_k} \right) \times 100$$
  where weights $w_k$ are explicitly assigned:
  - Completeness ($w_1 = 0.25$): No missing values in mandatory primary keys (State, Sector, Year, Indicator).
  - Validity ($w_2 = 0.25$): Value ranges within economic plausibility (e.g., MPCE > 0, expenditure shares $\in [0, 100]$).
  - Uniqueness ($w_3 = 0.15$): Zero duplicate records on primary composite key `(State, Sector, Round, Indicator)`.
  - Internal Consistency ($w_4 = 0.20$): Item group shares sum to $100\% \pm 0.1\%$; Imputed MPCE $\ge$ Unimputed MPCE.
  - Provenance ($w_5 = 0.15$): Validated cryptographic SHA-256 hash matching raw source release.
  Untested dimensions are explicitly excluded from both numerator and denominator with transparent logging.
- **Rejected Alternatives:**
  - *Alternative A: Subjective heuristic scoring (e.g., arbitrarily giving "95/100").* Rejected as unprofessional and unscientific.
  - *Alternative B: Conflating statistical sampling error (SE/RSE) with data pipeline quality.* Rejected because data quality measures pipeline integrity and data hygiene, whereas statistical sampling error reflects survey design and sample size.
- **Evidence:** Statistical Data Quality frameworks (IMF DQAF, Eurostat Code of Practice).
- **Unresolved Issues:** None.
- **Fallback:** Explicitly separate "Pipeline Quality Score" from "Survey Sampling Reliability" in documentation.

---

## Decision 7: Dual Valuation Model (Without Imputation vs. With Welfare Imputation) and Food Share Distinctions

- **Status:** APPROVED & IMPLEMENTED
- **Context:** In HCES 2022-23 and 2023-24, MoSPI introduced an innovative estimation method providing two parallel figures:
  1. *Without Imputation:* Out-of-pocket spending only.
  2. *With Imputation:* Includes imputed market value of goods received free of cost via government welfare schemes (PMGKY foodgrains, uniforms, textbooks, laptops, bicycles).
- **Decision:** Equip the UI with a persistent, global toggle: **"Expenditure Valuation: Out-of-Pocket Only (Without Imputation) vs. Including Social Welfare Imputation"**.
  Strictly implement the verified official food share distinctions:
  - **HCES 2022–23 published food shares:** Rural: 46.38%, Urban: 39.17% (without imputation); Rural: 47.47%, Urban: 39.70% (with imputation).
  - **HCES 2023–24 without social-transfer imputation:** Rural: 47.04%, Urban: 39.68%.
  - **HCES 2023–24 with imputation:** Rural: 48.43%, Urban: 40.31%.
- **Rejected Alternatives:**
  - *Alternative A: Conflating 2022-23 unimputed food share (46.38%) with 2023-24 unimputed food share (47.04%).* Rejected and corrected during audit.
  - *Alternative B: Silently averaging or mixing imputed and unimputed figures.* Rejected as methodologically invalid.
- **Evidence:** MoSPI Press Note (`HCES_Press_Note_2023-24_27122024_rev.pdf`), Figures 4 & 5, and PIB PRID 2088390.
- **Unresolved Issues:** None.
- **Fallback:** Default the toggle to "Out-of-Pocket Only (Without Imputation)" with a prominent contextual pill explaining the welfare imputation delta.

---

## Decision 8: Data Ingestion Architecture & Provenance

- **Status:** APPROVED & IMPLEMENTED
- **Context:** Data must be easily verifiable, auditable, and reproducible across different machines without internet flakiness.
- **Decision:** Establish a two-tiered repository directory structure:
  - `data/raw/`: Preserves original source extracts with exact names, metadata manifests, and SHA-256 checksums (`checksums.sha256`).
  - `data/processed/`: Structured, schema-validated, tidy CSV and Parquet files ready for analytical ingestion.
  - `src/pipeline.py`: Fully reproducible script that transforms `data/raw/` into `data/processed/` and generates an automated validation audit log (`docs/VALIDATION_REPORT.json`).
- **Rejected Alternatives:**
  - *Alternative A: Hardcoding numbers directly in Streamlit UI files.* Rejected as anti-pattern violating software engineering best practices.
  - *Alternative B: Dynamically scraping PIB/MoSPI portals on every user click.* Rejected due to latency, potential downtime of government servers, and rate limits.
- **Evidence:** Standard reproducible research pipeline guidelines (FAIR data principles).
- **Unresolved Issues:** None.
- **Fallback:** Complete offline fixture datasets bundled in `data/raw/` ensure 100% offline reproducibility.

---

## Decision 9: Audit-Led Data Repair, Geographic Reconciliation, and Decoupled Structured Ingestion

- **Status:** APPROVED & IMPLEMENTED
- **Context:** An audit identified data defects: incomplete state accounting in 2023–24 (26 states instead of 36), discrepancies in state observations (Goa, Himachal Pradesh, Uttarakhand, Dadra & Nagar Haveli and Daman & Diu, Haryana), synthetic values invented where data was unpublished, hardcoded python lists in pipeline.py, a 28-vs-29 QC check count discrepancy, unharmonized state filtering in the Regional Explorer, and missing CFPI in the CPI view.
- **Decision:**
  1. **Source Decoupling & Structured Ingestion:** Replaced code literals with documented, tabular source CSVs in `data/sources/` with explicit `source_id` and `table_ref` fields.
  2. **Complete Geographic Reconciliation:** Incorporated official parliamentary statement `PIB PRID 2247612` (providing 32 States/UTs) cross-referenced with `HCES Press Note Report 592` (providing Haryana, Punjab, and All-India). Corrected Goa (Rural ₹8,048, Urban ₹9,726), Himachal Pradesh (Rural ₹5,825, Urban ₹9,223), Uttarakhand (Rural ₹5,003, Urban ₹7,486), Dadra & Nagar Haveli and Daman & Diu (Rural ₹4,311, Urban ₹6,837), and Haryana (Rural ₹5,377, Urban ₹8,428).
  3. **Strict Non-Fabrication of Unpublished Figures:** Retained explicit `NaN` / missing indicators for Delhi (2023–24), Chandigarh unimputed (2023–24), and smaller states/UTs whose welfare imputation was not published in Report 592. Removed synthetic 2023–24 imputed category shares and restricted comparisons to the official unimputed series.
  4. **Complete CPI Monthly Series & CFPI:** Extracted the 20-month monthly series (Jan 2025 – Aug 2026) from Table 10 of the August 2026 release, and integrated Consumer Food Price Index (CFPI) data from Table 2 and Table 19 alongside headline inflation.
  5. **QC Check Count Reconciliation:** Aligned the Quality Engine to exactly 28 rules across 5 dimensions, and introduced a Data Availability Register to report coverage transparently without penalizing officially unpublished cells.
  6. **UI Harmonization:** Linked the state filter selection consistently across the Regional Explorer bar chart, disparity scatter plot, and data table.
- **Rejected Alternatives:**
  - *Alternative A: Imputing missing state observations through statistical regression.* Rejected because official statistical reporting must not present simulated values as government data.
  - *Alternative B: Retaining 29 checks by adding ad-hoc rules.* Rejected in favor of exact reconciliation to the documented 28-rule blueprint.
- **Evidence:** PIB PRID 2247612, MoSPI NSS Report No. 592 Press Note, and PIB PRID 2310058.
- **Unresolved Issues:** None.
- **Fallback:** Automated unit tests in `tests/test_pipeline.py` and `tests/test_quality_engine.py` enforce non-regression on verified figures.

---

## Decision 10: Final Gap Closure — Defensible Pipeline Validation Score, Practical Source Reconciliation, and UI Polish

- **Status:** APPROVED & IMPLEMENTED
- **Context:** To ensure the highest institutional research standard, the project required:
  1. Renaming the quality score to avoid false certainty (asserting pipeline hygiene rather than survey sampling representativeness).
  2. Demonstrating practical source reconciliation without fragile PDF web scrapers.
  3. Accurately characterizing the 2024-base CPI monthly series and inflation windows.
  4. Fully harmonizing UI state filters with quick cohort selectors and dynamic commentary.
- **Decision:**
  1. **Score Naming & Methodological Disclaimer:** Renamed the composite metric to **Pipeline Validation Score** (100.0%, 28/28 checks passed). Added explicit disclaimers across the UI and JSON reports stating that the validation score measures deterministic pipeline hygiene, schema constraints, and aggregation consistency, and does not assert statistical sampling precision or representativeness of NSSO surveys.
  2. **Practical Source Reconciliation Engine (`scripts/reconcile_sources.py`):** Implemented an automated reconciliation script verifying 23 key curated benchmarks directly against the extracted text of preserved primary source PDFs and HTML documents in `data/raw/`. Achieved a 100.0% match rate (23/23 benchmarks verified), outputting `docs/SOURCE_RECONCILIATION.json` and `docs/SOURCE_RECONCILIATION.md`.
  3. **CPI 2024-Base Coverage Transparency:** Documented the exact official availability: 20 months of general price index (January 2025 – August 2026), 8 months of YoY general inflation (January 2026 – August 2026), and 2 months of CFPI food inflation (July & August 2026). Clarified that 2024 monthly indices were not published by MoSPI in Table 10 of PIB PRID 2310058, strictly preventing false claims of complete historical inflation.
  4. **Harmonized UI & Quick Selectors:** Enhanced the Regional Explorer in `app.py` with quick cohort buttons ("All 36 Geographies", "18 Major States", "Clear All") synchronizing the multiselect, bar chart, disparity scatter plot, and data table. Connected dynamic commentary in Section 1 to the valuation toggle, ensuring all textual findings match the active data mode.
  5. **Data Decoupling & Downloads:** Decoupled national growth trajectory visualization into `data/sources/source_national_trajectory.csv` and `data/processed/national_trajectory.csv`, and provided download buttons for all datasets and audit artifacts in Section 6.
- **Rejected Alternatives:**
  - *Alternative A: Claiming automated end-to-end PDF scraping.* Rejected because government PDF layouts vary across tables and fragile heuristic scrapers break easily. Transparent curated source tables backed by deterministic text reconciliation offer far higher analytical integrity.
  - *Alternative B: Extrapolating CPI 2024 inflation backward into 2025.* Rejected to prevent inventing official economic statistics.
- **Evidence:** `scripts/reconcile_sources.py`, `docs/SOURCE_RECONCILIATION.json`, `docs/VALIDATION_REPORT.json`.
- **Unresolved Issues:** None.
- **Fallback:** Regression test suite in `tests/` continuously validates pipeline integrity, chart generators, and quality engine behavior.

---
*End of Decision Log.*


