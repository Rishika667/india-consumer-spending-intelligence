# Research Methodology & Technical Documentation — ConsumerLens India

**Product:** ConsumerLens India  
**Producer Agency:** National Sample Survey Office (NSSO), Ministry of Statistics and Programme Implementation (MoSPI), Government of India  
**Reference Document:** NSS Report No. 592 & No. 590  
**Current Date:** October 2026

---

## 1. Survey Architecture & Sampling Design

The Household Consumption Expenditure Survey (HCES) is India's principal official instrument for measuring living standards, household welfare, and commodity budget allocations.

### 1.1 Sample Stratification
- **Survey Round:** August 2023 to July 2024 (12 calendar months divided into 10 panels).
- **Sample Size:** 2,61,953 households (1,54,357 rural and 1,07,596 urban) spread across 14,827 First Stage Units (8,684 rural villages and 6,143 urban blocks).
- **Sampling Scheme:** Stratified Multi-Stage Design. First Stage Units (FSUs) selected with Simple Random Sampling Without Replacement (SRSWOR). Ultimate Stage Units (USUs) are sample households (18 per FSU).

### 1.2 The 3-Visit CAPI Innovation
In surveys prior to 2022-23 (such as the 68th round, 2011-12), consumption data across 347 items was collected in a single lengthy interview with a 30-day recall period, creating significant respondent fatigue and seasonal recall bias.

In HCES 2022-23 and 2023-24, MoSPI introduced an innovative 3-visit panel method using Computer Assisted Personal Interview (CAPI) software:
1. **Questionnaire FDQ (Food Items):** Canvassed in Month 1 of a quarter.
2. **Questionnaire CSQ (Consumables & Services):** Canvassed in Month 2.
3. **Questionnaire DGQ (Durable Goods):** Canvassed in Month 3.
4. **Questionnaire HCQ (Household Characteristics):** Demographics and auxiliary variables.

---

## 2. Valuation Framework: Dual Estimation Model

For HCES 2022-23 and 2023-24, MoSPI provides two parallel sets of estimates:

### 2.1 Without Imputation (Section A)
- Reflects out-of-pocket nominal cash expenditures and usual home produce / barter consumption.
- **2023-24 All-India Out-of-Pocket MPCE:**
  - Rural: ₹4,122 / month (+9.2% YoY)
  - Urban: ₹6,996 / month (+8.3% YoY)

### 2.2 With Imputation of Social Transfers (Section B)
- Imputes the local market value of in-kind goods received free of cost through government social welfare schemes:
  - *Food items:* Rice, Wheat/Atta, Millets, Pulses, Gram, Salt, Sugar, Edible Oil (e.g., under Pradhan Mantri Garib Kalyan Anna Yojana - PMGKY).
  - *Non-food items:* Laptop/PC, Tablet, Mobile Handset, Bicycle, Motorcycle/Scooty, School Uniforms, School Shoes.
- *Excluded Imputations:* Cashless healthcare (e.g., Ayushman Bharat PM-JAY) and fee waivers for schooling are not imputed due to valuation complexities in non-record-based surveys.
- **2023-24 All-India Welfare-Adjusted MPCE:**
  - Rural: ₹4,247 / month (+₹125/month welfare delta)
  - Urban: ₹7,078 / month (+₹82/month welfare delta)

### 2.3 Official Food Share Dynamics
- **2022-23 Published Shares (Without Imputation):** Rural 46.38%, Urban 39.17%.
- **2023-24 Published Shares (Without Imputation):** Rural 47.04%, Urban 39.68%.
- **2023-24 Published Shares (With Imputation):** Rural 48.43%, Urban 40.31%.
*(Food share is slightly higher with imputation because welfare schemes predominantly transfer foodgrains, boosting food spending value relative to non-food).*

---

## 3. Structural Divergence: HCES vs. National Accounts PFCE

Syndicated researchers must avoid confusing micro household survey estimates with macro national accounts:

| Conceptual Dimension | HCES Household Survey (NSSO) | Private Final Consumption Expenditure (PFCE, NAD) |
| :--- | :--- | :--- |
| **Statistical System** | Micro Sample Survey (261k households) | Macroeconomic National Income Accounts (SNA 2008) |
| **Coverage** | Resident private households only | Households + Non-Profit Institutions Serving Households (NPISH) |
| **Housing Rent** | Out-of-pocket rent paid only | Includes imputed rent on owner-occupied dwellings |
| **Financial Services** | Direct transaction charges | Includes FISIM (Financial Intermediation Services Indirectly Measured) |
| **Top-End Spending** | Under-reported by affluent top deciles | Captured via production, imports, and retail sales |
| **Divergence Magnitude** | Aggregated survey MPCE accounts for ~45–50% of aggregate national accounts PFCE | ₹178.6 lakh crore in FY 2023-24 (~60.2% of GDP) |

---

## 4. CPI Transition Framework (Base 2012=100 to Base 2024=100)

- **Release Date:** February 12, 2026 (Inaugural release) | Latest verified: August 2026 (PIB PRID 2310058).
- **Weighting Diagram:** Updated weights derived directly from HCES 2023-24 consumption patterns.
- **Item Expansion:** Expanded from 299 items (2012 base) to 358 items (2024 base), classifying items under COICOP 2018.
- **August 2026 Indicators:**
  - Headline Inflation: **4.82%** (Rural: 5.23%, Urban: 4.31%).
  - Consumer Food Price Index (CFPI): **5.95%** (Rural: 6.13%, Urban: 5.64%).
  - General Index: Combined 108.74, Rural 109.27, Urban 108.07.
- **Methodological Caution:** MoSPI explicitly mandates that direct splicing or mechanical ratio-linking between the 2012 and 2024 base series is invalid due to structural basket shifts.
