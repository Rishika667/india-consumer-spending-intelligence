# Source Reconciliation & Verification Matrix — ConsumerLens India
**Bidirectional verification comparing structured observations in `data/sources/*.csv` against preserved raw government releases in `data/raw/`.**

- **Total Benchmark Records Checked:** 42
- **Records Matched Against Source Evidence:** 0 (0.0%)
- **Mismatches:** 0
- **Unresolved Records:** 42

## 1. Scope and Claims Precision
Reconciliation checks programmatically verify 42 critical anchor benchmarks across national MPCE, corrected states, missing cells, food shares, fractiles, and retail CPI. Remaining cell values in curated tables are verified via deterministic internal consistency and relational schema rules in the Data Quality Engine.

## 2. Verified Benchmark Log

| ID | Metric / Observation | Source Dataset | Observed Value | Target Document | Status | Evidence / Extraction |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| `REC_01` | 2022-23 All-India Rural MPCE (Unimputed) | `source_state_mpce_2022_23.csv` | 3,773.00 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_02` | 2022-23 All-India Urban MPCE (Unimputed) | `source_state_mpce_2022_23.csv` | 6,459.00 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_03` | 2022-23 All-India Rural MPCE (Imputed) | `source_state_mpce_2022_23.csv` | 3,860.00 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_04` | 2022-23 All-India Urban MPCE (Imputed) | `source_state_mpce_2022_23.csv` | 6,521.00 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_05` | 2023-24 All-India Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 4,122.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_06` | 2023-24 All-India Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 6,996.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_07` | 2023-24 All-India Rural MPCE (Imputed) | `source_state_mpce_2023_24.csv` | 4,247.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_08` | 2023-24 All-India Urban MPCE (Imputed) | `source_state_mpce_2023_24.csv` | 7,078.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_09` | Goa 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 8,048.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_10` | Goa 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 9,726.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_11` | Himachal Pradesh 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,825.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_12` | Himachal Pradesh 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 9,223.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_13` | Uttarakhand 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,003.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_14` | Uttarakhand 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 7,486.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_15` | DNHDD 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 4,311.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_16` | DNHDD 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 6,837.00 | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_17` | Haryana 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,377.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_18` | Haryana 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 8,428.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_19` | Punjab 2023-24 Rural MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 5,817.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_20` | Punjab 2023-24 Urban MPCE (Unimputed) | `source_state_mpce_2023_24.csv` | 7,359.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_21` | Delhi 2023-24 Rural Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_22` | Delhi 2023-24 Urban Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_23` | Chandigarh 2023-24 Rural Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_24` | Chandigarh 2023-24 Urban Unimputed Status (NaN) | `source_state_mpce_2023_24.csv` | NaN | `HCES_2023-24_PIB_2247612.html` | **UNRESOLVED** | Target primary document 'HCES_2023-24_PIB_2247612.html' missing or unreadable in data/raw/ |
| `REC_25` | Chandigarh 2023-24 Rural Imputed MPCE | `source_state_mpce_2023_24.csv` | 8,857.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_26` | Chandigarh 2023-24 Urban Imputed MPCE | `source_state_mpce_2023_24.csv` | 13,425.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_27` | Sikkim 2023-24 Rural Imputed MPCE | `source_state_mpce_2023_24.csv` | 9,474.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_28` | Sikkim 2023-24 Urban Imputed MPCE | `source_state_mpce_2023_24.csv` | 13,965.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_29` | 2022-23 Rural Unimputed Food Share Benchmark (46.38%) | `source_category_shares.csv` | 9.62 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_30` | 2022-23 Urban Unimputed Food Share Rounding Reconciliation (39.16% vs 39.17%) | `source_category_shares.csv` | 10.64 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_31` | 2022-23 Rural Imputed Leading Food Category (Milk & Milk Products 8.14%) | `source_category_shares.csv` | 8.14 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_32` | 2022-23 Urban Imputed Leading Food Category (Milk & Milk Products 7.15%) | `source_category_shares.csv` | 7.15 | `Factsheet_HCES_2022-23.pdf` | **UNRESOLVED** | Target primary document 'Factsheet_HCES_2022-23.pdf' missing or unreadable in data/raw/ |
| `REC_33` | 2023-24 Rural Unimputed Beverages Share (9.84%) | `source_category_shares.csv` | 9.84 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_34` | 2023-24 Urban Unimputed Beverages Share (11.09%) | `source_category_shares.csv` | 11.09 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_35` | 2023-24 Fractile Bottom 5% Rural MPCE (Rs 1,677) | `source_fractile_distribution.csv` | 1,677.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_36` | 2023-24 Fractile Bottom 5% Urban MPCE (Rs 2,376) | `source_fractile_distribution.csv` | 2,376.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_37` | 2023-24 Fractile Top 5% Rural MPCE (Rs 10,137) | `source_fractile_distribution.csv` | 10,137.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_38` | 2023-24 Fractile Top 5% Urban MPCE (Rs 20,310) | `source_fractile_distribution.csv` | 20,310.00 | `HCES_Press_Note_2023-24_27122024_rev.pdf` | **UNRESOLVED** | Target primary document 'HCES_Press_Note_2023-24_27122024_rev.pdf' missing or unreadable in data/raw/ |
| `REC_39` | August 2026 Headline CPI Inflation Combined (4.82%) | `source_cpi_monthly_2024_base.csv` | 4.82 | `CPI_Release_Aug2026.html` | **UNRESOLVED** | Target primary document 'CPI_Release_Aug2026.html' missing or unreadable in data/raw/ |
| `REC_40` | August 2026 General CPI Index Combined (108.74) | `source_cpi_monthly_2024_base.csv` | 108.74 | `CPI_Release_Aug2026.html` | **UNRESOLVED** | Target primary document 'CPI_Release_Aug2026.html' missing or unreadable in data/raw/ |
| `REC_41` | August 2026 CFPI Food Inflation Combined (5.95%) | `source_cpi_monthly_2024_base.csv` | 5.95 | `CPI_Release_Aug2026.html` | **UNRESOLVED** | Target primary document 'CPI_Release_Aug2026.html' missing or unreadable in data/raw/ |
| `REC_42` | August 2026 CFPI Food Index Combined (110.71) | `source_cpi_monthly_2024_base.csv` | 110.71 | `CPI_Release_Aug2026.html` | **UNRESOLVED** | Target primary document 'CPI_Release_Aug2026.html' missing or unreadable in data/raw/ |

## 3. Documented Officially Unavailable Observations
The following items are officially unpublished in primary government releases. They are strictly preserved as explicit `NaN` / missing entries and are not estimated or fabricated:

- **Delhi 2023-24 unimputed & imputed MPCE (officially unpublished in Report 592 & PRID 2247612)**
- **Chandigarh 2023-24 unimputed MPCE (unimputed column not published in Report 592/PRID 2247612; imputed available on Page 9)**
- **17 Non-Major States/UTs 2023-24 welfare-imputed MPCE (imputation published only for 18 major states + 4 extreme callouts)**
- **2023-24 Commodity category shares with welfare imputation (Report 592 published only aggregate food/non-food shares, not item groups)**
- **2025 Calendar Year YoY CPI Inflation (Base 2024=100 monthly release starts at Jan-25; 2024 monthly indices not published in release)**
