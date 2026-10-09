"""
Script to generate documented structured source CSVs in data/sources/
derived exclusively from verified official MoSPI releases.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_DIR = os.path.join(BASE_DIR, "data", "sources")
os.makedirs(SOURCES_DIR, exist_ok=True)

# ==============================================================================
# 1. STATE MPCE 2022-23 (Official MoSPI HCES Factsheet Report 590: Statements 8 & 18)
# ==============================================================================
state_data_2022_23 = [
    ("Andhra Pradesh", 4870, 6782, 4996, 6877),
    ("Arunachal Pradesh", 5276, 8636, 5300, 8649),
    ("Assam", 3432, 6136, 3546, 6210),
    ("Bihar", 3384, 4768, 3454, 4819),
    ("Chhattisgarh", 2466, 4483, 2575, 4557),
    ("Delhi", 6576, 8217, 6595, 8250),
    ("Goa", 7367, 8734, 7388, 8761),
    ("Gujarat", 3798, 6621, 3820, 6630),
    ("Haryana", 4859, 7911, 4912, 7948),
    ("Himachal Pradesh", 5561, 8075, 5573, 8083),
    ("Jharkhand", 2763, 4931, 2796, 4946),
    ("Karnataka", 4397, 7666, 4578, 7781),
    ("Kerala", 5924, 7078, 5960, 7102),
    ("Madhya Pradesh", 3113, 4987, 3158, 5011),
    ("Maharashtra", 4010, 6657, 4076, 6683),
    ("Manipur", 4360, 4880, 4370, 4902),
    ("Meghalaya", 3514, 6433, 3530, 6450),
    ("Mizoram", 5224, 7655, 5243, 7664),
    ("Nagaland", 4393, 7098, 4457, 7159),
    ("Odisha", 2950, 5187, 2996, 5223),
    ("Punjab", 5315, 6544, 5363, 6577),
    ("Rajasthan", 4263, 5913, 4348, 5970),
    ("Sikkim", 7731, 12105, 7787, 12125),
    ("Tamil Nadu", 5310, 7630, 5457, 7742),
    ("Telangana", 4802, 8158, 4959, 8251),
    ("Tripura", 5206, 7405, 5301, 7473),
    ("Uttarakhand", 4641, 7004, 4721, 7034),
    ("Uttar Pradesh", 3191, 5040, 3277, 5104),
    ("West Bengal", 3239, 5267, 3407, 5426),
    ("Andaman & N Islands", 7332, 10268, 7332, 10268),
    ("Chandigarh", 7467, 12575, 7467, 12577),
    ("Dadra & Nagar Haveli and Daman & Diu", 4184, 6298, 4229, 6306),
    ("Jammu & Kashmir", 4296, 6179, 4357, 6200),
    ("Ladakh", 4035, 6215, 4062, 6227),
    ("Lakshadweep", 5895, 5475, 5979, 5511),
    ("Puducherry", 6590, 7706, 6627, 7741),
    ("All-India", 3773, 6459, 3860, 6521)
]

rows_22 = []
for state, r_unimp, u_unimp, r_imp, u_imp in state_data_2022_23:
    rows_22.append({
        "state_name": state,
        "survey_round": "2022-23",
        "sector": "Rural",
        "mpce_unimputed": float(r_unimp),
        "mpce_imputed": float(r_imp),
        "welfare_delta": float(r_imp - r_unimp),
        "source_id": "MoSPI_HCES_2022-23_Report590",
        "table_ref": "Statement 8 & Statement 18",
        "status": "OFFICIAL_PUBLISHED",
        "notes": "Verified against NSS Report 590 Factsheet Statements 8 and 18"
    })
    rows_22.append({
        "state_name": state,
        "survey_round": "2022-23",
        "sector": "Urban",
        "mpce_unimputed": float(u_unimp),
        "mpce_imputed": float(u_imp),
        "welfare_delta": float(u_imp - u_unimp),
        "source_id": "MoSPI_HCES_2022-23_Report590",
        "table_ref": "Statement 8 & Statement 18",
        "status": "OFFICIAL_PUBLISHED",
        "notes": "Verified against NSS Report 590 Factsheet Statements 8 and 18"
    })

df_state_22 = pd.DataFrame(rows_22)
df_state_22.to_csv(os.path.join(SOURCES_DIR, "source_state_mpce_2022_23.csv"), index=False)
print(f"Saved source_state_mpce_2022_23.csv with {len(df_state_22)} rows")

# ==============================================================================
# 2. STATE MPCE 2023-24 (MoSPI PIB PRID 2247612 & Press Note Report 592 Figures 2,3,8,9)
# ==============================================================================
# Complete reconciliation across all 36 States/UTs + All-India:
# (state_name, rural_unimputed, urban_unimputed, rural_imputed, urban_imputed, notes)
state_data_2023_24 = [
    # 18 Major States (Both unimputed & imputed fully published in Press Note Figures 2, 3, 8, 9 & PRID 2247612)
    ("Andhra Pradesh", 5327.0, 7182.0, 5539.0, 7341.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Arunachal Pradesh", 5995.0, 9832.0, np.nan, np.nan, "PRID 2247612; Imputed not published in Report 592"),
    ("Assam", 3793.0, 6794.0, 3961.0, 6913.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Bihar", 3670.0, 5080.0, 3788.0, 5165.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Chhattisgarh", 2739.0, 4927.0, 2927.0, 5114.0, "PRID 2247612 & Press Note Fig 2,3,8,9 & Page 9"),
    ("Goa", 8048.0, 9726.0, np.nan, np.nan, "PRID 2247612; Corrected verified discrepancy; Imputed not published"),
    ("Gujarat", 4116.0, 7175.0, 4190.0, 7198.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Haryana", 5377.0, 8428.0, 5449.0, 8462.0, "Press Note Fig 2,3,8,9 (Major state); Corrected"),
    ("Himachal Pradesh", 5825.0, 9223.0, np.nan, np.nan, "PRID 2247612; Corrected verified discrepancy; Imputed not published"),
    ("Jharkhand", 2946.0, 5393.0, 3056.0, 5455.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Karnataka", 4903.0, 8076.0, 5068.0, 8169.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Kerala", 6611.0, 7783.0, 6673.0, 7834.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Madhya Pradesh", 3441.0, 5538.0, 3522.0, 5589.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Maharashtra", 4145.0, 7363.0, 4249.0, 7415.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Manipur", 4531.0, 5945.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Meghalaya", 3852.0, 7839.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Mizoram", 5963.0, 8709.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Nagaland", 5155.0, 8022.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Odisha", 3357.0, 5825.0, 3509.0, 5925.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Punjab", 5817.0, 7359.0, 5874.0, 7383.0, "Press Note Fig 2,3,8,9 (Major state)"),
    ("Rajasthan", 4510.0, 6574.0, 4626.0, 6640.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Sikkim", 9377.0, 13927.0, 9474.0, 13965.0, "PRID 2247612 (unimputed) & Press Note Page 9 (imputed)"),
    ("Tamil Nadu", 5701.0, 8165.0, 5872.0, 8325.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Telangana", 5435.0, 8978.0, 5675.0, 9131.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Tripura", 6259.0, 8034.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Uttarakhand", 5003.0, 7486.0, np.nan, np.nan, "PRID 2247612; Corrected verified discrepancy; Imputed not published"),
    ("Uttar Pradesh", 3481.0, 5395.0, 3578.0, 5474.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("West Bengal", 3620.0, 5775.0, 3815.0, 5903.0, "PRID 2247612 & Press Note Fig 2,3,8,9"),
    ("Andaman & N Islands", 7771.0, 10453.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Chandigarh", np.nan, np.nan, 8857.0, 13425.0, "Press Note Page 9 (imputed highest UT); Unimputed officially unpublished"),
    ("Dadra & Nagar Haveli and Daman & Diu", 4311.0, 6837.0, 4450.0, np.nan, "PRID 2247612; Corrected; Imputed rural 4450 from Page 9; urban imputed unpublished"),
    ("Jammu & Kashmir", 4774.0, 6327.0, np.nan, 6375.0, "PRID 2247612; Corrected; Imputed urban 6375 from Page 9; rural imputed unpublished"),
    ("Ladakh", 5010.0, 7533.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Lakshadweep", 6350.0, 6377.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Puducherry", 7598.0, 8637.0, np.nan, np.nan, "PRID 2247612; Imputed not published"),
    ("Delhi", np.nan, np.nan, np.nan, np.nan, "Officially unpublished in PRID 2247612 and Press Note Report 592"),
    ("All-India", 4122.0, 6996.0, 4247.0, 7078.0, "Press Note Table 1 & Table 2 & PRID 2247612")
]

rows_23 = []
for state, r_unimp, u_unimp, r_imp, u_imp, notes in state_data_2023_24:
    # Rural
    r_delta = (r_imp - r_unimp) if (pd.notnull(r_imp) and pd.notnull(r_unimp)) else np.nan
    r_status = "OFFICIAL_PUBLISHED" if pd.notnull(r_unimp) else "OFFICIALLY_UNAVAILABLE"
    rows_23.append({
        "state_name": state,
        "survey_round": "2023-24",
        "sector": "Rural",
        "mpce_unimputed": r_unimp,
        "mpce_imputed": r_imp,
        "welfare_delta": r_delta,
        "source_id": "MoSPI_HCES_2023-24_Report592_PIB2247612",
        "table_ref": "PIB PRID 2247612 & Press Note Fig 2,3,8,9, Page 9",
        "status": r_status,
        "notes": notes
    })
    # Urban
    u_delta = (u_imp - u_unimp) if (pd.notnull(u_imp) and pd.notnull(u_unimp)) else np.nan
    u_status = "OFFICIAL_PUBLISHED" if pd.notnull(u_unimp) else "OFFICIALLY_UNAVAILABLE"
    rows_23.append({
        "state_name": state,
        "survey_round": "2023-24",
        "sector": "Urban",
        "mpce_unimputed": u_unimp,
        "mpce_imputed": u_imp,
        "welfare_delta": u_delta,
        "source_id": "MoSPI_HCES_2023-24_Report592_PIB2247612",
        "table_ref": "PIB PRID 2247612 & Press Note Fig 2,3,8,9, Page 9",
        "status": u_status,
        "notes": notes
    })

df_state_23 = pd.DataFrame(rows_23)
df_state_23.to_csv(os.path.join(SOURCES_DIR, "source_state_mpce_2023_24.csv"), index=False)
print(f"Saved source_state_mpce_2023_24.csv with {len(df_state_23)} rows")

# ==============================================================================
# 3. CATEGORY SHARES (MoSPI Statement 5, Statement 15, and Press Note Figures 4,5,6,7)
# ==============================================================================
category_records = [
    # Food categories (Figures 4 & 5 of 2023-24 Press Note; Statements 5 & 15 of 2022-23 Factsheet)
    # (Category, BroadGroup, R22_unimp, U22_unimp, R22_imp, U22_imp, R23_unimp, U23_unimp)
    ("Beverages & Processed Food", "Food", 9.62, 10.64, 9.41, 10.53, 9.84, 11.09),
    ("Milk & Milk Products", "Food", 8.33, 7.22, 8.14, 7.15, 8.44, 7.19),
    ("Vegetables", "Food", 5.38, 3.80, 5.26, 3.76, 6.03, 4.12),
    ("Egg, Fish & Meat", "Food", 4.91, 3.57, 4.80, 3.54, 4.92, 3.56),
    ("Cereals & Substitutes", "Food", 4.91, 3.64, 6.92, 4.51, 4.99, 3.76),
    ("Fruits", "Food", 3.71, 3.80, 3.63, 3.77, 3.85, 3.87),
    ("Edible Oil", "Food", 3.59, 2.37, 3.52, 2.35, 2.77, 1.82),
    ("Other Food Items (Pulses, Sugar, Spices)", "Food", 5.93, 4.12, 5.79, 4.09, 6.20, 4.27),
    # Non-Food categories (Figures 6 & 7 of 2023-24 Press Note; Statements 5 & 15 of 2022-23 Factsheet)
    ("Conveyance / Transport", "Non-Food", 7.55, 8.59, 7.38, 8.51, 7.59, 8.46),
    ("Clothing, Bedding & Footwear", "Non-Food", 6.10, 5.41, 6.03, 5.38, 6.63, 5.66),
    ("Durable Goods", "Non-Food", 6.89, 7.17, 6.79, 7.13, 6.48, 6.87),
    ("Medical Care", "Non-Food", 7.13, 5.91, 6.96, 5.85, 6.83, 5.85),
    ("Fuel and Light", "Non-Food", 6.66, 6.26, 6.51, 6.20, 6.11, 5.59),
    ("Misc. Goods & Entertainment", "Non-Food", 6.21, 6.56, 6.07, 6.50, 6.22, 6.92),
    ("Education", "Non-Food", 3.30, 5.78, 3.23, 5.73, 3.24, 5.97),
    ("Consumer Services excl Conveyance", "Non-Food", 5.08, 5.92, 4.96, 5.86, 5.25, 5.72),
    ("Rent, Taxes & Other Non-Food", "Non-Food", 4.70, 9.23, 4.60, 9.17, 4.61, 9.26)
]

cat_rows = []
for cat, broad, r22_u, u22_u, r22_i, u22_i, r23_u, u23_u in category_records:
    # 2022-23 Unimputed
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2022-23", "sector": "Rural", "valuation": "Unimputed", "share_pct": r22_u, "source_id": "MoSPI_Report590", "table_ref": "Statement 5"})
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2022-23", "sector": "Urban", "valuation": "Unimputed", "share_pct": u22_u, "source_id": "MoSPI_Report590", "table_ref": "Statement 5"})
    # 2022-23 Imputed
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2022-23", "sector": "Rural", "valuation": "Imputed", "share_pct": r22_i, "source_id": "MoSPI_Report590", "table_ref": "Statement 15"})
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2022-23", "sector": "Urban", "valuation": "Imputed", "share_pct": u22_i, "source_id": "MoSPI_Report590", "table_ref": "Statement 15"})
    # 2023-24 Unimputed
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2023-24", "sector": "Rural", "valuation": "Unimputed", "share_pct": r23_u, "source_id": "MoSPI_Report592", "table_ref": "Figures 4, 5, 6, 7"})
    cat_rows.append({"category": cat, "broad_group": broad, "survey_round": "2023-24", "sector": "Urban", "valuation": "Unimputed", "share_pct": u23_u, "source_id": "MoSPI_Report592", "table_ref": "Figures 4, 5, 6, 7"})

df_cat = pd.DataFrame(cat_rows)
df_cat.to_csv(os.path.join(SOURCES_DIR, "source_category_shares.csv"), index=False)
print(f"Saved source_category_shares.csv with {len(df_cat)} rows")

# ==============================================================================
# 4. FRACTILE DISTRIBUTION (Statement 4 of 2022-23 & Figure 1 / Text of 2023-24)
# ==============================================================================
fractile_data = [
    # (fractile_class, r22, u22, r23, u23)
    ("0-5%", 1373, 2001, 1677, 2376),
    ("5-10%", 1782, 2607, 2085, 2980),
    ("10-20%", 2112, 3157, 2410, 3510),
    ("20-30%", 2454, 3762, 2740, 4120),
    ("30-40%", 2768, 4348, 3060, 4730),
    ("40-50%", 3094, 4963, 3390, 5380),
    ("50-60%", 3455, 5662, 3760, 6110),
    ("60-70%", 3887, 6524, 4210, 7030),
    ("70-80%", 4458, 7673, 4810, 8250),
    ("80-90%", 5356, 9582, 5760, 10280),
    ("90-95%", 6638, 12399, 7110, 13240),
    ("95-100%", 10501, 20824, 10137, 20310)
]

frac_rows = []
for fc, r22, u22, r23, u23 in fractile_data:
    frac_rows.append({"fractile_class": fc, "survey_round": "2022-23", "sector": "Rural", "avg_mpce": float(r22), "source_id": "MoSPI_Report590", "table_ref": "Statement 4"})
    frac_rows.append({"fractile_class": fc, "survey_round": "2022-23", "sector": "Urban", "avg_mpce": float(u22), "source_id": "MoSPI_Report590", "table_ref": "Statement 4"})
    frac_rows.append({"fractile_class": fc, "survey_round": "2023-24", "sector": "Rural", "avg_mpce": float(r23), "source_id": "MoSPI_Report592", "table_ref": "Figure 1 & Fractile Table"})
    frac_rows.append({"fractile_class": fc, "survey_round": "2023-24", "sector": "Urban", "avg_mpce": float(u23), "source_id": "MoSPI_Report592", "table_ref": "Figure 1 & Fractile Table"})

df_frac = pd.DataFrame(frac_rows)
df_frac.to_csv(os.path.join(SOURCES_DIR, "source_fractile_distribution.csv"), index=False)
print(f"Saved source_fractile_distribution.csv with {len(df_frac)} rows")

# ==============================================================================
# 5. CPI 2024 BASE COMPLETE MONTHLY TIME SERIES (CPI_Release_Aug2026 Table 10 & 2)
# ==============================================================================
# Jan-2025 to Aug-2026: 20 consecutive months from Table 10 of PIB PRID 2310058 / CPI August 2026 release
cpi_table_10 = [
    # (month_year, r_idx, u_idx, c_idx, r_inf, u_inf, c_inf, status)
    ("2025-01", 101.81, 101.49, 101.67, np.nan, np.nan, np.nan, "Final"),
    ("2025-02", 101.33, 101.30, 101.32, np.nan, np.nan, np.nan, "Final"),
    ("2025-03", 101.34, 101.47, 101.39, np.nan, np.nan, np.nan, "Final"),
    ("2025-04", 101.49, 101.71, 101.58, np.nan, np.nan, np.nan, "Final"),
    ("2025-05", 101.78, 102.06, 101.90, np.nan, np.nan, np.nan, "Final"),
    ("2025-06", 102.39, 102.66, 102.51, np.nan, np.nan, np.nan, "Final"),
    ("2025-07", 103.34, 103.36, 103.35, np.nan, np.nan, np.nan, "Final"),
    ("2025-08", 103.84, 103.60, 103.74, np.nan, np.nan, np.nan, "Final"),
    ("2025-09", 103.80, 103.66, 103.74, np.nan, np.nan, np.nan, "Final"),
    ("2025-10", 103.85, 103.61, 103.74, np.nan, np.nan, np.nan, "Final"),
    ("2025-11", 104.16, 103.83, 104.01, np.nan, np.nan, np.nan, "Final"),
    ("2025-12", 104.19, 103.98, 104.10, np.nan, np.nan, np.nan, "Final"),
    ("2026-01", 104.59, 104.28, 104.45, 2.73, 2.75, 2.74, "Final"),
    ("2026-02", 104.74, 104.36, 104.57, 3.37, 3.02, 3.21, "Final"),
    ("2026-03", 105.02, 104.62, 104.84, 3.63, 3.11, 3.40, "Final"),
    ("2026-04", 105.28, 104.92, 105.12, 3.74, 3.16, 3.48, "Final"),
    ("2026-05", 106.11, 105.66, 105.91, 4.25, 3.53, 3.93, "Final"),
    ("2026-06", 107.24, 106.69, 107.00, 4.74, 3.93, 4.38, "Final"),
    ("2026-07", 108.34, 107.45, 107.95, 4.84, 3.96, 4.45, "Final"),
    ("2026-08", 109.27, 108.07, 108.74, 5.23, 4.31, 4.82, "Provisional")
]

# CFPI values from Table 2 and Table 19 for July & August 2026
cfpi_map = {
    ("2026-07", "Rural"): (109.21, 5.79),
    ("2026-07", "Urban"): (109.70, 5.05),
    ("2026-07", "Combined"): (109.39, 5.52),
    ("2026-08", "Rural"): (110.70, 6.13),
    ("2026-08", "Urban"): (110.72, 5.64),
    ("2026-08", "Combined"): (110.71, 5.95)
}

cpi_rows = []
for m, r_idx, u_idx, c_idx, r_inf, u_inf, c_inf, status in cpi_table_10:
    for sector, idx_val, inf_val in [("Rural", r_idx, r_inf), ("Urban", u_idx, u_inf), ("Combined", c_idx, c_inf)]:
        cfpi_idx, cfpi_inf = cfpi_map.get((m, sector), (np.nan, np.nan))
        cpi_rows.append({
            "month_year": m,
            "base_year": "2024=100",
            "sector": sector,
            "cpi_general": idx_val,
            "cpi_food_cfpi": cfpi_idx,
            "inflation_general_pct": inf_val,
            "inflation_food_pct": cfpi_inf,
            "release_status": status,
            "source_id": "MoSPI_CPI_Release_Aug2026",
            "table_ref": "Table 10 & Table 2 / Table 19"
        })

df_cpi_2024 = pd.DataFrame(cpi_rows)
df_cpi_2024.to_csv(os.path.join(SOURCES_DIR, "source_cpi_monthly_2024_base.csv"), index=False)
print(f"Saved source_cpi_monthly_2024_base.csv with {len(df_cpi_2024)} rows")

# ==============================================================================
# 6. CPI 2012 BASE DISCONTINUED HISTORICAL BENCHMARKS (Discontinued Feb 2026)
# ==============================================================================
# Labeled explicitly as benchmark reference snapshots during HCES survey periods
cpi_2012_benchmarks = [
    {"month_year": "2023-08", "base_year": "2012=100", "sector": "Combined", "cpi_general": 186.2, "cpi_food_cfpi": 188.4, "inflation_general_pct": 6.83, "inflation_food_pct": 9.94, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Aug 2023"},
    {"month_year": "2023-12", "base_year": "2012=100", "sector": "Combined", "cpi_general": 185.7, "cpi_food_cfpi": 189.0, "inflation_general_pct": 5.69, "inflation_food_pct": 9.53, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Dec 2023"},
    {"month_year": "2024-04", "base_year": "2012=100", "sector": "Combined", "cpi_general": 186.7, "cpi_food_cfpi": 189.6, "inflation_general_pct": 4.83, "inflation_food_pct": 8.70, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Apr 2024"},
    {"month_year": "2024-07", "base_year": "2012=100", "sector": "Combined", "cpi_general": 191.9, "cpi_food_cfpi": 198.5, "inflation_general_pct": 3.54, "inflation_food_pct": 5.42, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Jul 2024"},
    {"month_year": "2024-12", "base_year": "2012=100", "sector": "Combined", "cpi_general": 190.5, "cpi_food_cfpi": 195.1, "inflation_general_pct": 5.22, "inflation_food_pct": 8.40, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Dec 2024"},
    {"month_year": "2025-06", "base_year": "2012=100", "sector": "Combined", "cpi_general": 194.1, "cpi_food_cfpi": 199.8, "inflation_general_pct": 4.10, "inflation_food_pct": 5.15, "release_status": "Final", "source_id": "MoSPI_CPI_Archive", "table_ref": "Press Release Jun 2025"}
]
df_cpi_2012 = pd.DataFrame(cpi_2012_benchmarks)
df_cpi_2012.to_csv(os.path.join(SOURCES_DIR, "source_cpi_historical_2012_base_snapshot.csv"), index=False)
print(f"Saved source_cpi_historical_2012_base_snapshot.csv with {len(df_cpi_2012)} rows")

# ==============================================================================
# 7. MACRO PFCE BENCHMARKS (National Accounts Statistics FY 2011-12 to FY 2023-24)
# ==============================================================================
pfce_records = [
    {"fiscal_year": "2011-12", "pfce_current_inr_cr": 4914108, "pfce_constant_inr_cr": 4914108, "share_of_gdp_pct": 56.2, "source_id": "MoSPI_NAS", "table_ref": "NAS Statement 1"},
    {"fiscal_year": "2020-21", "pfce_current_inr_cr": 11845600, "pfce_constant_inr_cr": 7564200, "share_of_gdp_pct": 59.8, "source_id": "MoSPI_NAS", "table_ref": "NAS Statement 1"},
    {"fiscal_year": "2021-22", "pfce_current_inr_cr": 14012300, "pfce_constant_inr_cr": 8412500, "share_of_gdp_pct": 59.6, "source_id": "MoSPI_NAS", "table_ref": "NAS Statement 1"},
    {"fiscal_year": "2022-23", "pfce_current_inr_cr": 16054200, "pfce_constant_inr_cr": 9015400, "share_of_gdp_pct": 60.1, "source_id": "MoSPI_NAS", "table_ref": "NAS Statement 1"},
    {"fiscal_year": "2023-24", "pfce_current_inr_cr": 17862000, "pfce_constant_inr_cr": 9380000, "share_of_gdp_pct": 60.2, "source_id": "MoSPI_NAS", "table_ref": "NAS Statement 1"}
]
df_pfce = pd.DataFrame(pfce_records)
df_pfce.to_csv(os.path.join(SOURCES_DIR, "source_macro_pfce.csv"), index=False)
print(f"Saved source_macro_pfce.csv with {len(df_pfce)} rows")
