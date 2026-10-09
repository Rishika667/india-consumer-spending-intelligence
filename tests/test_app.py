"""
Automated unit and integration tests for Streamlit application components,
chart generators, data loading, cohort selectors, and dynamic analytics.
"""

import os
import json
import pytest
import pandas as pd
from app import load_all_datasets
from src.ui.charts import (
    create_trend_trajectory_chart,
    create_fractile_curve_chart,
    create_state_bar_chart,
    create_disparity_scatter_chart,
    create_category_comparison_chart,
    create_cpi_trends_chart
)


def test_app_data_loading():
    """Verify that all six processed datasets and the validation report load successfully."""
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, val_report = load_all_datasets()
    assert not df_state.empty
    assert not df_category.empty
    assert not df_fractile.empty
    assert not df_cpi.empty
    assert not df_pfce.empty
    assert not df_traj.empty
    assert "composite_score" in val_report or "pipeline_validation_score" in val_report
    assert val_report.get("total_evaluated", 0) == 28


def test_chart_generators_render():
    """Verify that all primary Plotly chart generators produce valid figures."""
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, _ = load_all_datasets()

    # Trend trajectory
    fig1a = create_trend_trajectory_chart(df_traj, "Unimputed")
    assert fig1a is not None
    fig1b = create_trend_trajectory_chart("Imputed")
    assert fig1b is not None

    # Fractile curve
    fig2 = create_fractile_curve_chart(df_fractile)
    assert fig2 is not None

    # State bar chart (Both, Rural, Urban)
    fig3a = create_state_bar_chart(df_state, "2023-24", "mpce_unimputed", "Both")
    assert fig3a is not None
    fig3b = create_state_bar_chart(df_state, "2023-24", "mpce_imputed", "Rural")
    assert fig3b is not None

    # Disparity scatter plot
    fig4 = create_disparity_scatter_chart(df_state, "2023-24", "mpce_unimputed")
    assert fig4 is not None
    has_ratio_trace = any("Benchmark" in str(tr.name) for tr in fig4.data)
    assert has_ratio_trace

    # Category budget shares
    fig5a = create_category_comparison_chart(df_category, "Rural", "Unimputed")
    assert fig5a is not None
    fig5b = create_category_comparison_chart(df_category, "Urban", "Imputed")
    assert fig5b is not None

    # CPI trends
    fig6a = create_cpi_trends_chart(df_cpi, "2024=100")
    assert fig6a is not None
    fig6b = create_cpi_trends_chart(df_cpi, "2012=100")
    assert fig6b is not None


def test_cpi_dynamic_metrics_extraction():
    """Verify dynamic extraction of August 2026 CPI headline numbers and coverage counts."""
    _, _, _, df_cpi, _, _, _ = load_all_datasets()
    cpi_2024 = df_cpi[df_cpi["base_year"] == "2024=100"]
    assert not cpi_2024.empty

    latest_month = cpi_2024["month_year"].max()
    assert latest_month == "2026-08"

    cpi_latest = cpi_2024[cpi_2024["month_year"] == latest_month]
    c_comb = cpi_latest[cpi_latest["sector"] == "Combined"]
    assert len(c_comb) == 1
    assert c_comb["inflation_general_pct"].values[0] == 4.82
    assert c_comb["cpi_general"].values[0] == 108.74
    assert c_comb["cpi_food_cfpi"].values[0] == 110.71
    assert c_comb["inflation_food_pct"].values[0] == 5.95

    # Check coverage counts
    num_idx = cpi_2024[cpi_2024["cpi_general"].notnull()]["month_year"].nunique()
    num_yoy = cpi_2024[cpi_2024["inflation_general_pct"].notnull()]["month_year"].nunique()
    num_cfpi = cpi_2024[cpi_2024["inflation_food_pct"].notnull()]["month_year"].nunique()
    assert num_idx == 20
    assert num_yoy == 8
    assert num_cfpi == 2


def test_rural_urban_disparity_dynamic_ratios():
    """Verify that disparity scatter benchmark line adapts dynamically to selected round and valuation."""
    df_state, _, _, _, _, _, _ = load_all_datasets()

    # 2023-24 Unimputed: 6996 / 4122 ~ 1.70x
    fig_23_u = create_disparity_scatter_chart(df_state, "2023-24", "mpce_unimputed")
    trace_23_u = [tr for tr in fig_23_u.data if "Benchmark" in str(tr.name)][0]
    assert "1.70" in trace_23_u.name

    # 2023-24 Imputed: 7078 / 4247 ~ 1.67x
    fig_23_i = create_disparity_scatter_chart(df_state, "2023-24", "mpce_imputed")
    trace_23_i = [tr for tr in fig_23_i.data if "Benchmark" in str(tr.name)][0]
    assert "1.67" in trace_23_i.name

    # 2022-23 Unimputed: 6459 / 3773 ~ 1.71x
    fig_22_u = create_disparity_scatter_chart(df_state, "2022-23", "mpce_unimputed")
    trace_22_u = [tr for tr in fig_22_u.data if "Benchmark" in str(tr.name)][0]
    assert "1.71" in trace_22_u.name

    # 2022-23 Imputed: 6521 / 3860 ~ 1.69x
    fig_22_i = create_disparity_scatter_chart(df_state, "2022-23", "mpce_imputed")
    trace_22_i = [tr for tr in fig_22_i.data if "Benchmark" in str(tr.name)][0]
    assert "1.69" in trace_22_i.name


def test_empty_filters_and_graceful_handling():
    """Verify that empty filter selections do not crash chart generators."""
    empty_df = pd.DataFrame(columns=["state_name", "survey_round", "sector", "mpce_unimputed", "mpce_imputed"])

    # State bar chart with empty data
    fig_empty_bar = create_state_bar_chart(empty_df, "2023-24", "mpce_unimputed", "Both")
    assert fig_empty_bar is not None
    assert any("No published data available" in str(ann.text) for ann in fig_empty_bar.layout.annotations)

    # Disparity scatter plot with empty data
    fig_empty_scatter = create_disparity_scatter_chart(empty_df, "2023-24", "mpce_unimputed")
    assert fig_empty_scatter is not None
    assert any("No paired Rural-Urban observations" in str(ann.text) for ann in fig_empty_scatter.layout.annotations)


def test_geographic_cohort_subsets():
    """Verify that 18 major states cohort is a valid subset of all tracked geographies."""
    df_state, _, _, _, _, _, _ = load_all_datasets()
    all_states = sorted(list(df_state[df_state["state_name"] != "All-India"]["state_name"].unique()))
    assert len(all_states) == 36

    MAJOR_STATES = [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Gujarat", "Haryana",
        "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha",
        "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
    ]
    assert len(MAJOR_STATES) == 18
    assert set(MAJOR_STATES).issubset(set(all_states))


def test_missing_state_observations_availability():
    """Verify that Delhi and Chandigarh retain explicit NaN and are detected without false corruption flags."""
    df_state, _, _, _, _, _, _ = load_all_datasets()
    delhi_23 = df_state[(df_state["state_name"] == "Delhi") & (df_state["survey_round"] == "2023-24")]
    assert len(delhi_23) == 2
    assert pd.isna(delhi_23["mpce_unimputed"].values[0])
    assert pd.isna(delhi_23["mpce_imputed"].values[0])

    chd_23 = df_state[(df_state["state_name"] == "Chandigarh") & (df_state["survey_round"] == "2023-24")]
    assert len(chd_23) == 2
    assert pd.isna(chd_23["mpce_unimputed"].values[0])
    # Imputed is published on page 9
    assert pd.notna(chd_23["mpce_imputed"].values[0])


def test_reconciliation_json_fields_and_evidence():
    """Verify that SOURCE_RECONCILIATION.json matches schema rendered in app.py Section 5."""
    rec_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "SOURCE_RECONCILIATION.json")
    assert os.path.exists(rec_path)
    with open(rec_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "reconciliation_checks" in data
    checks = data["reconciliation_checks"]
    assert len(checks) >= 42

    required_cols = {"check_id", "metric", "dataset", "observed_value", "primary_source_doc", "table_ref", "status", "source_evidence"}
    for c in checks:
        assert required_cols.issubset(c.keys())
        assert c["status"] == "MATCH"
        assert len(c["source_evidence"]) > 0


def test_download_payloads_content():
    """Verify that all analytical datasets produce valid non-empty CSV export payloads."""
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, _ = load_all_datasets()

    csv_state = df_state.to_csv(index=False)
    assert len(csv_state) > 100
    assert "state_name,survey_round,sector" in csv_state

    csv_cat = df_category.to_csv(index=False)
    assert len(csv_cat) > 100
    assert "category,broad_group,survey_round" in csv_cat

    csv_frac = df_fractile.to_csv(index=False)
    assert len(csv_frac) > 100
    assert "fractile_class,survey_round,sector" in csv_frac

    csv_cpi = df_cpi.to_csv(index=False)
    assert len(csv_cpi) > 100
    assert "month_year,base_year,sector" in csv_cpi
