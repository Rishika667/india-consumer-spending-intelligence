# Source Reconciliation & Verification Matrix — ConsumerLens India
**Bidirectional verification comparing structured observations in `data/sources/*.csv` against preserved raw government releases in `data/raw/`.**

- **Total Benchmark Records Checked:** 42
- **Records Matched Against Source Evidence:** 42 (100.0%)
- **Mismatches:** 0
- **Unresolved Records:** 0

## 1. Scope and Claims Precision
Reconciliation checks programmatically verify 42 critical anchor benchmarks across national MPCE, corrected states, missing cells, food shares, fractiles, and retail CPI. Remaining cell values in curated tables are verified via deterministic internal consistency and relational schema rules in the Data Quality Engine.

## 2. Verified Benchmark Log

| ID | Metric / Observation | Source Dataset | Observed Value | Target Document | Status | Evidence / Extraction |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| `REC_01` | 2022-23 All-India Rural MPCE (Unimputed) | `source_state_mpce_2022_23.csv` | 3,773.00 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 8 page 14: all-India Rural 3,773, Urban 6,459 |
| `REC_02` | 2022-23 All-India Urban MPCE (Unimputed) | `source_state_mpce_2022_23.csv` | 6,459.00 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 8 page 14: all-India Urban 6,459 |
| `REC_03` | 2022-23 All-India Rural MPCE (Imputed) | `source_state_mpce_2022_23.csv` | 3,860.00 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 18 page 22: All-India Rural 3,860 |
| `REC_04` | 2022-23 All-India Urban MPCE (Imputed) | `source_state_mpce_2022_23.csv` | 6,521.00 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 18 page 22: All-India Urban 6,521 |
| `REC_05` | 2023-24 All-India Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 4,122.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Table 1: Rural 4,122 |
| `REC_06` | 2023-24 All-India Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 6,996.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Table 1: Urban 6,996 |
| `REC_07` | 2023-24 All-India Rural MPCE (Imputed) | `source_state_mpce_2023_24.csv` | 4,247.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Table 2: Rural 4,247 |
| `REC_08` | 2023-24 All-India Urban MPCE (Imputed) | `source_state_mpce_2023_24.csv` | 7,078.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Table 2: Urban 7,078 |
| `REC_09` | Goa 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 8,048.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Goa Rural = 8048.0 |
| `REC_10` | Goa 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 9,726.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Goa Urban = 9726.0 |
| `REC_11` | Himachal Pradesh 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,825.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Himachal Pradesh Rural = 5825.0 |
| `REC_12` | Himachal Pradesh 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 9,223.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Himachal Pradesh Urban = 9223.0 |
| `REC_13` | Uttarakhand 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,003.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Uttarakhand Rural = 5003.0 |
| `REC_14` | Uttarakhand 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 7,486.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Uttarakhand Urban = 7486.0 |
| `REC_15` | DNHDD 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 4,311.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Dadra & Nagar Haveli and Daman & Diu Rural = 4311.0 |
| `REC_16` | DNHDD 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 6,837.00 | `HCES_2023-24_PIB_2247612.html` | **MATCH** | PRID 2247612 Table 4 Statement 1: Dadra & Nagar Haveli and Daman & Diu Urban = 6837.0 |
| `REC_17` | Haryana 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,377.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Figure 2: Haryana = 5,377 |
| `REC_18` | Haryana 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 8,428.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Figure 3: Haryana = 8,428 |
| `REC_19` | Punjab 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,817.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Figure 2: Punjab = 5,817 |
| `REC_20` | Punjab 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 7,359.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Figure 3: Punjab = 7,359 |
| `REC_21` | Delhi 2023-24 Rural Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **MATCH** | Delhi is officially omitted/unpublished in PRID 2247612 Table 4 and Report 592 Figures 2 & 3 |
| `REC_22` | Delhi 2023-24 Urban Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **MATCH** | Delhi is officially omitted/unpublished in PRID 2247612 Table 4 and Report 592 Figures 2 & 3 |
| `REC_23` | Chandigarh 2023-24 Rural Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **MATCH** | Chandigarh unimputed MPCE is officially omitted/unpublished in PRID 2247612 and Report 592 Fig 2 & 3 |
| `REC_24` | Chandigarh 2023-24 Urban Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **MATCH** | Chandigarh unimputed MPCE is officially omitted/unpublished in PRID 2247612 and Report 592 Fig 2 & 3 |
| `REC_25` | Chandigarh 2023-24 Rural Imputed MPCE | `source_state_mpce_2023_24.csv` | 8,857.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 page 9: Chandigarh Rural Imputed 8,857 |
| `REC_26` | Chandigarh 2023-24 Urban Imputed MPCE | `source_state_mpce_2023_24.csv` | 13,425.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 page 9: Chandigarh Urban Imputed 13,425 |
| `REC_27` | Sikkim 2023-24 Rural Imputed MPCE | `source_state_mpce_2023_24.csv` | 9,474.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 page 9: Sikkim Rural Imputed 9,474 |
| `REC_28` | Sikkim 2023-24 Urban Imputed MPCE | `source_state_mpce_2023_24.csv` | 13,965.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 page 9: Sikkim Urban Imputed 13,965 |
| `REC_29` | 2022-23 Rural Unimputed Food Share Benchmark (46.38%) | `source_category_shares.csv` | 9.62 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 5: Beverages & Processed Food Rural = 9.62% (Food Total = 46.38%) |
| `REC_30` | 2022-23 Urban Unimputed Food Share Rounding Reconciliation (39.16% vs 39.17%) | `source_category_shares.csv` | 10.64 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 5: Beverages Urban = 10.64%; Food group sum = 39.16% vs published aggregate 39.17% (0.01% rounding) |
| `REC_31` | 2022-23 Rural Imputed Leading Food Category (Milk & Milk Products 8.14%) | `source_category_shares.csv` | 8.14 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 15: Milk & Milk Products Rural Imputed = 8.14% (Total Food = 47.47%) |
| `REC_32` | 2022-23 Urban Imputed Leading Food Category (Milk & Milk Products 7.15%) | `source_category_shares.csv` | 7.15 | `Factsheet_HCES_2022-23.pdf` | **MATCH** | Statement 15: Milk & Milk Products Urban Imputed = 7.15% (Total Food = 39.70%) |
| `REC_33` | 2023-24 Rural Unimputed Beverages Share (9.84%) | `source_category_shares.csv` | 9.84 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Figure 4 Page 7: beverages & processed food Rural = 9.84% |
| `REC_34` | 2023-24 Urban Unimputed Beverages Share (11.09%) | `source_category_shares.csv` | 11.09 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Figure 5 Page 7: beverages & processed food Urban = 11.09% |
| `REC_35` | 2023-24 Fractile Bottom 5% Rural MPCE (Rs 1,677) | `source_fractile_distribution.csv` | 1,677.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Page 4: Bottom 5% Rural = Rs. 1,677 |
| `REC_36` | 2023-24 Fractile Bottom 5% Urban MPCE (Rs 2,376) | `source_fractile_distribution.csv` | 2,376.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Page 4: Bottom 5% Urban = Rs. 2,376 |
| `REC_37` | 2023-24 Fractile Top 5% Rural MPCE (Rs 10,137) | `source_fractile_distribution.csv` | 10,137.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Page 4: Top 5% Rural = Rs. 10,137 |
| `REC_38` | 2023-24 Fractile Top 5% Urban MPCE (Rs 20,310) | `source_fractile_distribution.csv` | 20,310.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **MATCH** | Report 592 Page 4: Top 5% Urban = Rs. 20,310, |
| `REC_39` | August 2026 Headline CPI Inflation Combined (4.82%) | `source_cpi_monthly_2024_base.csv` | 4.82 | `CPI_Release_Aug2026.html` | **MATCH** | CPI Table 1: August 2026 CPI General Combined Inflation = 4.82% |
| `REC_40` | August 2026 General CPI Index Combined (108.74) | `source_cpi_monthly_2024_base.csv` | 108.74 | `CPI_Release_Aug2026.html` | **MATCH** | CPI Table 1: August 2026 CPI General Combined Index = 108.74 |
| `REC_41` | August 2026 CFPI Food Inflation Combined (5.95%) | `source_cpi_monthly_2024_base.csv` | 5.95 | `CPI_Release_Aug2026.html` | **MATCH** | CPI Table 1: August 2026 CFPI Combined Food Inflation = 5.95% |
| `REC_42` | August 2026 CFPI Food Index Combined (110.71) | `source_cpi_monthly_2024_base.csv` | 110.71 | `CPI_Release_Aug2026.html` | **MATCH** | CPI Table 1: August 2026 CFPI Combined Food Index = 110.71 |

## 3. Documented Officially Unavailable Observations
The following items are officially unpublished in primary government releases. They are strictly preserved as explicit `NaN` / missing entries and are not estimated or fabricated:

- **Delhi 2023-24 unimputed & imputed MPCE (officially unpublished in Report 592 & PRID 2247612)**
- **Chandigarh 2023-24 unimputed MPCE (unimputed column not published in Report 592/PRID 2247612; imputed available on Page 9)**
- **17 Non-Major States/UTs 2023-24 welfare-imputed MPCE (imputation published only for 18 major states + 4 extreme callouts)**
- **2023-24 Commodity category shares with welfare imputation (Report 592 published only aggregate food/non-food shares, not item groups)**
- **2025 Calendar Year YoY CPI Inflation (Base 2024=100 monthly release starts at Jan-25; 2024 monthly indices not published in release)**
