"""
ConsumerLens India — UI Layout, Presentation & Data-Narrative Consistency Regression Tests
Verifies that visual presentation, chart margins, categorical axes,
selective scatter labeling, within-round fractile consistency, food-share anchors,
and state values strictly adhere to official MoSPI evidence.
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


def test_fractile_top_to_bottom_ratios_consistency(app_data):
    """
    Verifies consistent within-round top-to-bottom fractile ratios:
    - 2023-24: Rural = 10,137 / 1,677 = 6.04x; Urban = 20,310 / 2,376 = 8.55x
    - 2022-23: Rural = 10,501 / 1,373 = 7.65x; Urban = 20,824 / 2,001 = 10.41x
    Never mixes years.
    """
    _, _, df_fractile, _, _, _, _ = app_data

    # 2023-24 within-round calculations
    f23_r_bot = df_fractile[(df_fractile["survey_round"] == "2023-24") & (df_fractile["sector"] == "Rural") & (df_fractile["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
    f23_r_top = df_fractile[(df_fractile["survey_round"] == "2023-24") & (df_fractile["sector"] == "Rural") & (df_fractile["fractile_class"] == "95-100%")]["avg_mpce"].values[0]
    f23_u_bot = df_fractile[(df_fractile["survey_round"] == "2023-24") & (df_fractile["sector"] == "Urban") & (df_fractile["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
    f23_u_top = df_fractile[(df_fractile["survey_round"] == "2023-24") & (df_fractile["sector"] == "Urban") & (df_fractile["fractile_class"] == "95-100%")]["avg_mpce"].values[0]

    assert f23_r_bot == 1677.0
    assert f23_r_top == 10137.0
    assert f23_u_bot == 2376.0
    assert f23_u_top == 20310.0

    r_ratio_23 = round(f23_r_top / f23_r_bot, 2)
    u_ratio_23 = round(f23_u_top / f23_u_bot, 2)
    assert r_ratio_23 == 6.04
    assert u_ratio_23 == 8.55

    # 2022-23 within-round calculations
    f22_r_bot = df_fractile[(df_fractile["survey_round"] == "2022-23") & (df_fractile["sector"] == "Rural") & (df_fractile["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
    f22_r_top = df_fractile[(df_fractile["survey_round"] == "2022-23") & (df_fractile["sector"] == "Rural") & (df_fractile["fractile_class"] == "95-100%")]["avg_mpce"].values[0]
    f22_u_bot = df_fractile[(df_fractile["survey_round"] == "2022-23") & (df_fractile["sector"] == "Urban") & (df_fractile["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
    f22_u_top = df_fractile[(df_fractile["survey_round"] == "2022-23") & (df_fractile["sector"] == "Urban") & (df_fractile["fractile_class"] == "95-100%")]["avg_mpce"].values[0]

    assert f22_r_bot == 1373.0
    assert f22_r_top == 10501.0
    assert f22_u_bot == 2001.0
    assert f22_u_top == 20824.0

    r_ratio_22 = round(f22_r_top / f22_r_bot, 2)
    u_ratio_22 = round(f22_u_top / f22_u_bot, 2)
    assert r_ratio_22 == 7.65
    assert u_ratio_22 == 10.41


def test_food_share_benchmarks_and_valuation_anchors(app_data):
    """
    Verifies verified food share benchmarks:
    - 2022-23 rural was ALREADY below 50% (46.38% unimputed, 47.47% imputed).
    - 2023-24 rural food share increased to 47.04% unimputed and 48.43% imputed.
    - 2022-23 urban is 39.16% (category sum) / 39.17% aggregate unimputed, 39.70% imputed.
    - 2023-24 urban is 39.68% unimputed, 40.31% imputed aggregate.
    """
    _, df_category, _, _, _, _, _ = app_data

    # Food sums from category shares dataset
    f_22_r_unimp = df_category[(df_category["survey_round"] == "2022-23") & (df_category["sector"] == "Rural") & (df_category["valuation"] == "Unimputed") & (df_category["broad_group"] == "Food")]["share_pct"].sum()
    f_23_r_unimp = df_category[(df_category["survey_round"] == "2023-24") & (df_category["sector"] == "Rural") & (df_category["valuation"] == "Unimputed") & (df_category["broad_group"] == "Food")]["share_pct"].sum()
    f_22_u_unimp = df_category[(df_category["survey_round"] == "2022-23") & (df_category["sector"] == "Urban") & (df_category["valuation"] == "Unimputed") & (df_category["broad_group"] == "Food")]["share_pct"].sum()
    f_23_u_unimp = df_category[(df_category["survey_round"] == "2023-24") & (df_category["sector"] == "Urban") & (df_category["valuation"] == "Unimputed") & (df_category["broad_group"] == "Food")]["share_pct"].sum()

    assert round(f_22_r_unimp, 2) == 46.38
    assert round(f_23_r_unimp, 2) == 47.04
    assert round(f_22_u_unimp, 2) == 39.16
    assert round(f_23_u_unimp, 2) == 39.68

    # Assert rural food share was already below 50% in 2022-23
    assert f_22_r_unimp < 50.0
    # Assert rural food share rose slightly between rounds
    assert f_23_r_unimp > f_22_r_unimp

    # Cereal share between rounds
    cer_22_r = df_category[(df_category["survey_round"] == "2022-23") & (df_category["sector"] == "Rural") & (df_category["category"].str.contains("Cereals"))]["share_pct"].values[0]
    cer_23_r = df_category[(df_category["survey_round"] == "2023-24") & (df_category["sector"] == "Rural") & (df_category["category"].str.contains("Cereals"))]["share_pct"].values[0]
    assert cer_22_r == 4.91
    assert cer_23_r == 4.99
    # Cereal share rose slightly between 2022-23 and 2023-24
    assert cer_23_r >= cer_22_r


def test_regional_state_mpce_integrity(app_data):
    """
    Verifies official 2023-24 state figures in state_mpce.csv match official MoSPI Report 592 Table 1:
    - Sikkim: Rural 9377, Urban 13927 (Ratio: 1.49x)
    - Goa: Rural 8048, Urban 9726 (Ratio: 1.21x)
    - Andaman & N Islands: Rural 7771, Urban 10453 (Ratio: 1.35x)
    - Arunachal Pradesh: Rural 5995, Urban 9832 (Ratio: 1.64x)
    - Kerala: Rural 6611, Urban 7783 (Ratio: 1.18x)
    - Jharkhand: Rural 2946, Urban 5393 (Ratio: 1.83x)
    - Meghalaya: Rural 3852, Urban 7839 (Ratio: 2.04x)
    - Punjab: Rural 5817, Urban 7359 (Ratio: 1.27x)
    - Chhattisgarh: Rural 2739, Urban 4927 (Ratio: 1.80x)
    - Odisha: Rural 3357, Urban 5825 (Ratio: 1.74x)
    - Bihar: Rural 3670, Urban 5080 (Ratio: 1.38x)
    - Delhi & Chandigarh rural: NaN in 2023-24 unimputed
    """
    df_state, _, _, _, _, _, _ = app_data
    st_23 = df_state[df_state["survey_round"] == "2023-24"]

    def get_val(state, sec):
        return st_23[(st_23["state_name"] == state) & (st_23["sector"] == sec)]["mpce_unimputed"].values[0]

    assert get_val("Sikkim", "Rural") == 9377.0
    assert get_val("Sikkim", "Urban") == 13927.0
    assert get_val("Goa", "Rural") == 8048.0
    assert get_val("Goa", "Urban") == 9726.0
    assert get_val("Andaman & N Islands", "Rural") == 7771.0
    assert get_val("Andaman & N Islands", "Urban") == 10453.0
    assert get_val("Arunachal Pradesh", "Rural") == 5995.0
    assert get_val("Arunachal Pradesh", "Urban") == 9832.0
    assert get_val("Kerala", "Rural") == 6611.0
    assert get_val("Kerala", "Urban") == 7783.0
    assert get_val("Jharkhand", "Rural") == 2946.0
    assert get_val("Jharkhand", "Urban") == 5393.0
    assert get_val("Meghalaya", "Rural") == 3852.0
    assert get_val("Meghalaya", "Urban") == 7839.0
    assert get_val("Punjab", "Rural") == 5817.0
    assert get_val("Punjab", "Urban") == 7359.0
    assert get_val("Chhattisgarh", "Rural") == 2739.0
    assert get_val("Chhattisgarh", "Urban") == 4927.0
    assert get_val("Odisha", "Rural") == 3357.0
    assert get_val("Odisha", "Urban") == 5825.0
    assert get_val("Bihar", "Rural") == 3670.0
    assert get_val("Bihar", "Urban") == 5080.0

    # Ratios
    assert round(get_val("Meghalaya", "Urban") / get_val("Meghalaya", "Rural"), 2) == 2.04
    assert round(get_val("Kerala", "Urban") / get_val("Kerala", "Rural"), 2) == 1.18
    assert round(get_val("Punjab", "Urban") / get_val("Punjab", "Rural"), 2) == 1.27

    delhi_r = st_23[(st_23["state_name"] == "Delhi") & (st_23["sector"] == "Rural")]["mpce_unimputed"].values[0]
    assert pd.isna(delhi_r)


def test_narrative_factual_consistency_and_no_cliches():
    """
    Verifies that app.py contains no generic AI reporting clichés,
    no unverified 1811 figure, and no false 'first-time' food share claims.
    """
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    banned_cliches = [
        "Sustained Consumption Momentum",
        "Descriptive Shift in Budget Allocations",
        "Distributional Focus"
    ]
    for cliche in banned_cliches:
        assert cliche not in content, f"Found banned generic AI cliché: '{cliche}' in app.py"

    # Verify unverified 1811 figure is NOT in app.py
    assert "1811" not in content, "Found unverified figure 1811 in app.py"
    assert "1,811" not in content, "Found unverified figure 1,811 in app.py"

    # Verify false 'first-time' claim is NOT in app.py
    assert "first time in official NSS" not in content.lower(), "Found false 'first-time' sub-50% food share claim in app.py"
    assert "for the first time in official" not in content.lower(), "Found false 'first-time' sub-50% food share claim in app.py"

    # Must contain verified analytical briefing titles
    assert "render_insight_card" in content
    assert "Spending Dynamics: Ratio Compression vs. Expanding Absolute Rupee Gap" in content
    assert "Social Welfare Imputation: In-Kind Valuation vs. Liquid Purchasing Power" in content
    assert "Food Budget Share Dynamics: Long-Term Shifts and Valuation Differences" in content
    assert "Distributional Spread: Bottom-Fractile Growth and Upper-Quintile Depth" in content


def test_chart_tickformat_formatting_integrity(app_data):
    """
    Verifies that all charts in src/ui/charts.py use valid single-comma tickformat=",.0f"
    and that no malformed ',,.0f' remains in the codebase.
    """
    df_state, df_category, df_fractile, _, _, df_traj, _ = app_data
    charts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "ui", "charts.py")
    with open(charts_path, "r", encoding="utf-8") as f:
        charts_code = f.read()

    assert ",,.0f" not in charts_code, "Found malformed tickformat ',,.0f' in src/ui/charts.py"

    fig_traj = create_trend_trajectory_chart(df_traj, "Unimputed")
    assert fig_traj.layout.yaxis.tickformat == ",.0f"

    fig_frac = create_fractile_curve_chart(df_fractile, "2023-24")
    assert fig_frac.layout.yaxis.tickformat == ",.0f"

    fig_state = create_state_bar_chart(df_state, "2023-24", "mpce_unimputed", "Both")
    assert fig_state.layout.xaxis.tickformat == ",.0f"

    fig_disp = create_disparity_scatter_chart(df_state, "2023-24", "mpce_unimputed")
    assert fig_disp.layout.xaxis.tickformat == ",.0f"
    assert fig_disp.layout.yaxis.tickformat == ",.0f"


def test_overview_layout_and_button_labels():
    """
    Verifies that app.py uses 4 KPI columns for consumption indicators,
    includes the executive takeaway, and provides clean quick-selection button labels.
    """
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 4 columns for consumption KPIs
    assert "st.columns(4)" in content, "Overview must use 4 KPI columns for consumption indicators"
    assert "render_executive_takeaway" in content, "Overview must include executive takeaway callout"

    # Clean button labels (no emoji prefixes)
    assert 'qc1.button("All Geographies"' in content, "Expected 'All Geographies' button"
    assert 'qc2.button("Major States"' in content, "Expected 'Major States' button"
    assert 'qc3.button("Clear"' in content, "Expected 'Clear' button"


def test_category_comparison_cross_round_preservation(app_data):
    """
    Verifies that create_category_comparison_chart preserves cross-round comparison
    (both 2022-23 and 2023-24 present) even when called with 'Imputed' valuation.
    """
    _, df_category, _, _, _, _, _ = app_data
    for sec in ["Rural", "Urban"]:
        fig_unimp = create_category_comparison_chart(df_category, sec, "Unimputed")
        rounds_unimp = {tr.name for tr in fig_unimp.data if hasattr(tr, "name")}
        assert "2022-23" in rounds_unimp and "2023-24" in rounds_unimp

        fig_imp = create_category_comparison_chart(df_category, sec, "Imputed")
        rounds_imp = {tr.name for tr in fig_imp.data if hasattr(tr, "name")}
        assert "2022-23" in rounds_imp and "2023-24" in rounds_imp
