"""
Unit tests for Streamlit application loading and chart generator components.
"""

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
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, val_report = load_all_datasets()
    assert not df_state.empty
    assert not df_category.empty
    assert not df_fractile.empty
    assert not df_cpi.empty
    assert not df_pfce.empty
    assert not df_traj.empty
    assert "composite_score" in val_report or "pipeline_validation_score" in val_report


def test_chart_generators_render():
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, _ = load_all_datasets()

    # Test both with explicit dataframe and string mode
    fig1a = create_trend_trajectory_chart(df_traj, "Unimputed")
    assert fig1a is not None

    fig1b = create_trend_trajectory_chart("Imputed")
    assert fig1b is not None

    fig2 = create_fractile_curve_chart(df_fractile)
    assert fig2 is not None

    fig3 = create_state_bar_chart(df_state, "2023-24", "mpce_unimputed", "Both")
    assert fig3 is not None

    fig4 = create_disparity_scatter_chart(df_state, "2023-24", "mpce_unimputed")
    assert fig4 is not None
    # Verify dynamic ratio trace is present
    has_ratio_trace = any("Benchmark" in str(tr.name) for tr in fig4.data)
    assert has_ratio_trace

    fig5 = create_category_comparison_chart(df_category, "Rural", "Unimputed")
    assert fig5 is not None

    fig6 = create_cpi_trends_chart(df_cpi, "2024=100")
    assert fig6 is not None


def test_cpi_dynamic_metrics_extraction():
    _, _, _, df_cpi, _, _, _ = load_all_datasets()
    cpi_2024 = df_cpi[df_cpi["base_year"] == "2024=100"]
    assert not cpi_2024.empty

    latest_month = cpi_2024["month_year"].max()
    assert latest_month == "2026-08"

    cpi_latest = cpi_2024[cpi_2024["month_year"] == latest_month]
    c_gen = cpi_latest[cpi_latest["sector"] == "Combined"]
    assert len(c_gen) == 1
    assert c_gen["inflation_general_pct"].values[0] == 4.82
    assert c_gen["cpi_general"].values[0] == 108.74
    assert c_gen["cpi_food_cfpi"].values[0] == 110.71
    assert c_gen["inflation_food_pct"].values[0] == 5.95

