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
    df_state, df_category, df_fractile, df_cpi, df_pfce, val_report = load_all_datasets()
    assert not df_state.empty
    assert not df_category.empty
    assert not df_fractile.empty
    assert not df_cpi.empty
    assert not df_pfce.empty
    assert "composite_score" in val_report


def test_chart_generators_render():
    df_state, df_category, df_fractile, df_cpi, df_pfce, _ = load_all_datasets()

    fig1 = create_trend_trajectory_chart("Unimputed")
    assert fig1 is not None

    fig2 = create_fractile_curve_chart(df_fractile)
    assert fig2 is not None

    fig3 = create_state_bar_chart(df_state, "2023-24", "mpce_unimputed", "Both")
    assert fig3 is not None

    fig4 = create_disparity_scatter_chart(df_state, "2023-24", "mpce_unimputed")
    assert fig4 is not None

    fig5 = create_category_comparison_chart(df_category, "Rural", "Unimputed")
    assert fig5 is not None

    fig6 = create_cpi_trends_chart(df_cpi, "2024=100")
    assert fig6 is not None
