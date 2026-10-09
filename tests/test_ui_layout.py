"""
ConsumerLens India — UI Layout & Chart Presentation Regression Tests
Verifies that visual presentation, chart margins, categorical axes,
selective scatter labeling, and research briefs meet syndicated standards.
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
    create_cpi_trends_chart,
    format_chart_layout
)


@pytest.fixture(scope="module")
def app_data():
    return load_all_datasets()


def test_trajectory_chart_axis_is_categorical(app_data):
    """
    Regression test for Defect 1: The MPCE trajectory chart must NOT display
    datetime ticks. The x-axis must be explicitly categorical with discrete survey rounds.
    """
    _, _, _, _, _, df_traj, _ = app_data

    for val_mode in ["Unimputed", "Imputed"]:
        fig = create_trend_trajectory_chart(df_traj, val_mode)
        assert fig is not None

        # Verify x-axis is explicitly typed as category
        assert fig.layout.xaxis.type == "category", "Trajectory x-axis must be explicitly categorical"

        # Verify tickvals are discrete survey round strings
        tickvals = list(fig.layout.xaxis.tickvals)
        assert "2011-12" in tickvals
        assert "2022-23" in tickvals
        assert "2023-24" in tickvals

        # Verify traces: 2 bars (Nominal) and 2 lines (Real 2011-12)
        bar_traces = [tr for tr in fig.data if tr.type == "bar"]
        scatter_traces = [tr for tr in fig.data if tr.type == "scatter"]
        assert len(bar_traces) == 2, "Expected 2 bar traces (Urban Nominal, Rural Nominal)"
        assert len(scatter_traces) == 2, "Expected 2 scatter traces (Urban Real, Rural Real)"

        # Verify barmode is group
        assert fig.layout.barmode == "group"

        # Verify legend is positioned below without colliding with title
        assert fig.layout.legend.yanchor == "top"
        assert fig.layout.legend.y <= 0, "Legend must be placed below plot to avoid colliding with title"


def test_disparity_scatter_selective_labeling(app_data):
    """
    Regression test for Defect 2: The rural-urban scatter plot must NOT display
    overlapping state names on every single point. It must use interactive hover details
    and selectively label only prominent frontier outliers.
    """
    df_state, _, _, _, _, _, _ = app_data

    for rnd in ["2023-24", "2022-23"]:
        for val_col in ["mpce_unimputed", "mpce_imputed"]:
            fig = create_disparity_scatter_chart(df_state, rnd, val_col)
            assert fig is not None

            # Find the scatter trace for states
            state_trace = [tr for tr in fig.data if tr.name == "States / UTs"][0]

            # Hovertemplate must contain state name, rural MPCE, urban MPCE, and ratio
            hover_tmpl = state_trace.hovertemplate
            assert "Rural MPCE" in hover_tmpl
            assert "Urban MPCE" in hover_tmpl
            assert "Urban/Rural Ratio" in hover_tmpl

            # Check text labels: only a restrained subset of frontier outliers must be non-empty
            text_labels = state_trace.text
            non_empty_labels = [lbl for lbl in text_labels if lbl and str(lbl).strip()]
            total_points = len(text_labels)

            assert total_points >= 18, f"Expected at least 18 state points plotted for {rnd} {val_col}, got {total_points}"
            assert len(non_empty_labels) <= 8, f"Selective labeling must be <= 8 labels, got {len(non_empty_labels)}"
            assert len(non_empty_labels) > 0, "Expected at least 1-2 frontier states labeled"

            # Benchmark line must be present
            benchmark_traces = [tr for tr in fig.data if "Benchmark" in tr.name]
            assert len(benchmark_traces) == 1, "Expected dynamic national benchmark line"

            # Parity line (1.00x) must be present
            parity_traces = [tr for tr in fig.data if "Parity" in tr.name]
            assert len(parity_traces) == 1, "Expected 1.00x parity reference line"


def test_category_comparison_margins_and_units(app_data):
    """
    Regression test for Defect 3: Category comparison chart must reserve adequate
    left margin (>= 180px) for commodity names and explicitly state MPCE share units.
    """
    _, df_category, _, _, _, _, _ = app_data

    for sector in ["Rural", "Urban"]:
        for val in ["Unimputed", "Imputed"]:
            fig = create_category_comparison_chart(df_category, sector, val)
            assert fig is not None

            # Verify generous left margin
            assert fig.layout.margin.l >= 180, f"Left margin must be >= 180 for commodity names, got {fig.layout.margin.l}"

            # Verify x-axis title states % of MPCE
            x_title = fig.layout.xaxis.title.text
            assert "% of MPCE" in x_title or "Share of MPCE" in x_title


def test_state_bar_chart_margins_and_empty_handling(app_data):
    """
    Verifies that state bar chart handles long state names with adequate left margin,
    and returns a valid informative figure when given an empty selection.
    """
    df_state, _, _, _, _, _, _ = app_data

    # Standard render
    fig = create_state_bar_chart(df_state, "2023-24", "mpce_unimputed", "Both")
    assert fig.layout.margin.l >= 180, "Left margin must be >= 180 for state names"

    # Empty selection handling
    empty_df = pd.DataFrame(columns=["state_name", "survey_round", "sector", "mpce_unimputed", "mpce_imputed"])
    fig_empty = create_state_bar_chart(empty_df, "2023-24", "mpce_unimputed", "Rural")
    assert fig_empty is not None
    assert any("No published data available" in str(ann.text) for ann in fig_empty.layout.annotations)


def test_fractile_curve_layout(app_data):
    """
    Verifies that fractile curve chart has categorical x-axis, distinct rural and urban traces,
    and centered legend below plot.
    """
    _, _, df_fractile, _, _, _, _ = app_data
    fig = create_fractile_curve_chart(df_fractile, "2023-24")
    assert fig.layout.xaxis.type == "category"

    traces = {tr.name: tr for tr in fig.data}
    assert "Rural Households" in traces
    assert "Urban Households" in traces
    assert traces["Rural Households"].line.color != traces["Urban Households"].line.color

    assert fig.layout.legend.yanchor == "top"
    assert fig.layout.legend.y <= 0


def test_narrative_quality_no_ai_cliches():
    """
    Verifies that app.py contains no generic AI reporting clichés,
    and includes the structured 4-dimension analytical brief cards.
    """
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generic AI cliché phrases that must NOT appear as section headers or titles
    banned_cliches = [
        "Sustained Consumption Momentum",
        "Descriptive Shift in Budget Allocations",
        "Distributional Focus"
    ]
    for cliche in banned_cliches:
        assert cliche not in content, f"Found banned generic AI cliché: '{cliche}' in app.py"

    # Must contain structured insight brief components
    assert "render_insight_card" in content
    assert "Urban–Rural Divergence: Ratio Compression vs. Expanding Rupee Gap" in content
    assert "Social Welfare Imputation: Consumption Absorption vs. Cash Liquidity" in content
    assert "Structural Budget Transition: The Sub-50% Rural Food Pivot" in content
    assert "Distributional Inequality: High Percentage Growth Off an Ultra-Low Base" in content
