# Data Dictionary — ConsumerLens India
**India Consumer Spending Intelligence & Data Quality Engine**  
**Repository:** `https://github.com/Rishika667/india-consumer-spending-intelligence.git`

This document defines all fields, data types, standard units, and definitions across the normalized analytical datasets stored in `data/processed/`.

---

## 1. Dataset: `state_mpce.csv`
Contains state/UT-level Monthly Per Capita Consumption Expenditure (MPCE) across rural and urban sectors and survey rounds.

| Field Name | Data Type | Units / Format | Definition & Analytical Context |
| :--- | :--- | :--- | :--- |
| `state_name` | String | Standard State/UT Name | Name of the Indian State or Union Territory, or "All-India" national benchmark. |
| `survey_round` | String | e.g., `2022-23`, `2023-24` | Survey reference period (`2022-23`: Aug 2022–Jul 2023; `2023-24`: Aug 2023–Jul 2024). |
| `sector` | String | `Rural` / `Urban` | Sector designation based on NSS sample stratification. |
| `mpce_unimputed` | Float | INR (₹) / month / person | Average Monthly Per Capita Consumption Expenditure, excluding social welfare transfers. |
| `mpce_imputed` | Float | INR (₹) / month / person | Average MPCE including the imputed market value of in-kind welfare items (PMGKY foodgrains, school uniforms, cycles, digital devices). |
| `welfare_delta` | Float | INR (₹) / month / person | Computed transfer value: $\text{mpce\_imputed} - \text{mpce\_unimputed}$. |
| `source_id` | String | Identifier | Official MoSPI publication report ID (e.g., `MoSPI_HCES_2023-24_Report592`). |

---

## 2. Dataset: `category_shares.csv`
Contains the percentage expenditure breakdown across 17 detailed commodity groups.

| Field Name | Data Type | Units / Format | Definition & Analytical Context |
| :--- | :--- | :--- | :--- |
| `category` | String | Group Name | Specific expenditure category (e.g., *Beverages & Processed Food*, *Conveyance*). |
| `broad_group` | String | `Food` / `Non-Food` | Broad macroeconomic classification. |
| `survey_round` | String | `2022-23` / `2023-24` | Survey reference period. |
| `sector` | String | `Rural` / `Urban` | Geographic sector. |
| `valuation` | String | `Unimputed` / `Imputed` | Valuation basis (out-of-pocket vs with welfare transfers). |
| `share_pct` | Float | Percentage (%) | Percentage contribution of the category to total household MPCE. |

---

## 3. Dataset: `fractile_distribution.csv`
Contains the average MPCE across 12 fractile percentile classes.

| Field Name | Data Type | Units / Format | Definition & Analytical Context |
| :--- | :--- | :--- | :--- |
| `fractile_class` | String | e.g., `0-5%`, `5-10%`, ..., `95-100%` | Population fractile class ranked by household MPCE. |
| `survey_round` | String | `2022-23` / `2023-24` | Survey round. |
| `sector` | String | `Rural` / `Urban` | Sector. |
| `avg_mpce` | Float | INR (₹) / month / person | Mean MPCE for households falling within the specified fractile percentile. |

---

## 4. Dataset: `cpi_series.csv`
Contains monthly Consumer Price Index numbers and Year-over-Year inflation rates.

| Field Name | Data Type | Units / Format | Definition & Analytical Context |
| :--- | :--- | :--- | :--- |
| `month_year` | String | `YYYY-MM` | Reference month. |
| `base_year` | String | `2012=100` / `2024=100` | Base year series. |
| `sector` | String | `Rural` / `Urban` / `Combined` | Geographic sector. |
| `cpi_general` | Float | Index Points | Headline Consumer Price Index. |
| `cpi_food_cfpi` | Float | Index Points | Consumer Food Price Index (CFPI). |
| `inflation_general_pct` | Float | Percentage (%) | Year-over-Year retail inflation rate for General CPI. |
| `inflation_food_pct` | Float | Percentage (%) | Year-over-Year retail food inflation rate for CFPI. |

---

## 5. Dataset: `macro_pfce.csv`
Contains macroeconomic Private Final Consumption Expenditure (PFCE) benchmarks from National Accounts Statistics.

| Field Name | Data Type | Units / Format | Definition & Analytical Context |
| :--- | :--- | :--- | :--- |
| `fiscal_year` | String | `YYYY-YY` | Fiscal year (April to March). |
| `pfce_current_inr_cr` | Float | INR Crore | PFCE at current market prices. |
| `pfce_constant_inr_cr` | Float | INR Crore | PFCE at constant (2011-12) prices. |
| `share_of_gdp_pct` | Float | Percentage (%) | PFCE contribution as a percentage of nominal GDP. |
