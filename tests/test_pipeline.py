"""
Automated unit tests for the research pipeline and dataset integrity.
Validates source-backed values, coverage, and mathematical consistency.
"""

import os
import pytest
import numpy as np
import pandas as pd
from src.pipeline import (
    build_state_mpce_dataset,
    build_category_shares_dataset,
    build_fractile_distribution_dataset,
    build_cpi_series_dataset,
    build_macro_pfce_dataset,
    run_pipeline
)


def test_state_mpce_dataset_integrity():
    df = build_state_mpce_dataset()
    assert not df.empty
    assert set(["state_name", "survey_round", "sector", "mpce_unimputed", "mpce_imputed"]).issubset(df.columns)
    
    # Check that published MPCE values are strictly positive
    assert (df["mpce_unimputed"].dropna() > 0).all()
    assert (df["mpce_imputed"].dropna() > 0).all()
    
    # Check that welfare imputation is non-negative where both exist
    comp = df.dropna(subset=["mpce_imputed", "mpce_unimputed"])
    assert (comp["mpce_imputed"] >= comp["mpce_unimputed"]).all()
    
    # Check All-India national numbers for 2023-24
    ai_23 = df[(df["state_name"] == "All-India") & (df["survey_round"] == "2023-24")]
    assert ai_23[ai_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 4122.0
    assert ai_23[ai_23["sector"] == "Rural"]["mpce_imputed"].values[0] == 4247.0
    assert ai_23[ai_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 6996.0
    assert ai_23[ai_23["sector"] == "Urban"]["mpce_imputed"].values[0] == 7078.0

    # Check verified corrected state figures from PIB PRID 2247612 and Press Note Report 592
    goa_23 = df[(df["state_name"] == "Goa") & (df["survey_round"] == "2023-24")]
    assert goa_23[goa_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 8048.0
    assert goa_23[goa_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 9726.0

    hp_23 = df[(df["state_name"] == "Himachal Pradesh") & (df["survey_round"] == "2023-24")]
    assert hp_23[hp_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 5825.0
    assert hp_23[hp_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 9223.0

    uk_23 = df[(df["state_name"] == "Uttarakhand") & (df["survey_round"] == "2023-24")]
    assert uk_23[uk_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 5003.0
    assert uk_23[uk_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 7486.0

    dnh_23 = df[(df["state_name"] == "Dadra & Nagar Haveli and Daman & Diu") & (df["survey_round"] == "2023-24")]
    assert dnh_23[dnh_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 4311.0
    assert dnh_23[dnh_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 6837.0

    haryana_23 = df[(df["state_name"] == "Haryana") & (df["survey_round"] == "2023-24")]
    assert haryana_23[haryana_23["sector"] == "Rural"]["mpce_unimputed"].values[0] == 5377.0
    assert haryana_23[haryana_23["sector"] == "Urban"]["mpce_unimputed"].values[0] == 8428.0

    # Check that Delhi 2023-24 retains explicit NaN rather than fabricated values
    delhi_23 = df[(df["state_name"] == "Delhi") & (df["survey_round"] == "2023-24")]
    assert pd.isna(delhi_23[delhi_23["sector"] == "Rural"]["mpce_unimputed"].values[0])
    assert pd.isna(delhi_23[delhi_23["sector"] == "Urban"]["mpce_unimputed"].values[0])

    # Check full 36 State/UT geographic accounting
    states_22 = df[df["survey_round"] == "2022-23"]["state_name"].unique()
    assert len(states_22) >= 37  # 36 States/UTs + All-India


def test_category_shares_food_distinctions():
    df = build_category_shares_dataset()
    assert not df.empty
    
    # 2022-23 Unimputed Food share: Rural 46.38%, Urban 39.16% (Statement 5)
    f_22 = df[(df["survey_round"] == "2022-23") & (df["broad_group"] == "Food") & (df["valuation"] == "Unimputed")].groupby("sector")["share_pct"].sum()
    assert abs(f_22["Rural"] - 46.38) <= 0.1
    assert abs(f_22["Urban"] - 39.16) <= 0.1
    
    # 2022-23 Imputed Food share: Rural 47.47%, Urban 39.70% (Statement 15)
    f_22_i = df[(df["survey_round"] == "2022-23") & (df["broad_group"] == "Food") & (df["valuation"] == "Imputed")].groupby("sector")["share_pct"].sum()
    assert abs(f_22_i["Rural"] - 47.47) <= 0.1
    assert abs(f_22_i["Urban"] - 39.70) <= 0.1

    # 2023-24 Unimputed Food share: Rural 47.04%, Urban 39.68% (Figures 4 & 5)
    f_23_u = df[(df["survey_round"] == "2023-24") & (df["broad_group"] == "Food") & (df["valuation"] == "Unimputed")].groupby("sector")["share_pct"].sum()
    assert abs(f_23_u["Rural"] - 47.04) <= 0.1
    assert abs(f_23_u["Urban"] - 39.68) <= 0.1
    
    # Sum of categories across each slice aggregates to 100% +/- 0.5%
    sums = df.groupby(["survey_round", "sector", "valuation"])["share_pct"].sum()
    for s in sums:
        assert abs(s - 100.0) <= 0.5


def test_fractile_distribution():
    df = build_fractile_distribution_dataset()
    assert not df.empty
    
    # Check bottom 5% and top 5% in 2023-24
    bot_23_r = df[(df["survey_round"] == "2023-24") & (df["sector"] == "Rural") & (df["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
    top_23_r = df[(df["survey_round"] == "2023-24") & (df["sector"] == "Rural") & (df["fractile_class"] == "95-100%")]["avg_mpce"].values[0]
    assert bot_23_r == 1677.0
    assert top_23_r == 10137.0
    assert top_23_r > bot_23_r


def test_cpi_series():
    df = build_cpi_series_dataset()
    assert not df.empty
    bases = df["base_year"].unique()
    assert "2012=100" in bases
    assert "2024=100" in bases
    
    # August 2026 data
    aug_26 = df[df["month_year"] == "2026-08"]
    assert not aug_26.empty
    combined = aug_26[aug_26["sector"] == "Combined"].iloc[0]
    assert combined["inflation_general_pct"] == 4.82
    assert combined["inflation_food_pct"] == 5.95


def test_end_to_end_pipeline():
    report = run_pipeline()
    assert report["composite_score"] >= 95.0
    assert report["failed"] == 0
    assert report["total_evaluated"] == 28
