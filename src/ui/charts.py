"""
ConsumerLens India — High-Quality Plotly Chart Generators
Engineered for syndicated research reports: restrained palette, clean formatting, and legible typography.
"""

import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


PRIMARY_NAVY = "#1e3a8a"
SLATE_GREY = "#64748b"
EMERALD_GREEN = "#059669"
AMBER_ACCENT = "#d97706"
PURPLE_ACCENT = "#7c3aed"
LIGHT_BG = "#f8fafc"


def format_chart_layout(fig, title: str = "", height: int = 450):
    fig.update_layout(
        title={"text": title, "font": {"size": 15, "color": "#0f172a", "family": "Inter, sans-serif"}},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin={"l": 40, "r": 30, "t": 60, "b": 40},
        height=height,
        font={"family": "Inter, sans-serif", "color": "#334155", "size": 12},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        hoverlabel={"bgcolor": "#1e293b", "font_size": 12, "font_color": "#ffffff"}
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9", zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f1f5f9", zeroline=False)
    return fig


def create_trend_trajectory_chart(df_traj=None, valuation_mode: str = "Unimputed") -> go.Figure:
    """
    Shows national consumption trajectory across survey rounds (2011-12, 2022-23, 2023-24).
    Compares current prices vs constant (2011-12) prices using official Table 1 & Table 2.
    Built directly from structured dataset national_trajectory.csv.
    """
    if isinstance(df_traj, str):
        valuation_mode = df_traj
        df_traj = None
    if df_traj is None or (isinstance(df_traj, pd.DataFrame) and df_traj.empty):
        traj_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "processed", "national_trajectory.csv")
        if os.path.exists(traj_path):
            df_traj = pd.read_csv(traj_path)

    val_filter = "Imputed" if "imputed" in valuation_mode.lower() and "un" not in valuation_mode.lower() else "Unimputed"
    sub = df_traj[df_traj["valuation"] == val_filter] if df_traj is not None and not df_traj.empty else pd.DataFrame()
    
    if sub.empty:
        fig = go.Figure()
        return format_chart_layout(fig, f"All-India MPCE Growth ({val_filter})", 440)

    years = sub[sub["sector"] == "Urban"]["survey_round"].tolist()
    urban_curr = sub[sub["sector"] == "Urban"]["mpce_current_inr"].tolist()
    rural_curr = sub[sub["sector"] == "Rural"]["mpce_current_inr"].tolist()
    urban_const = sub[sub["sector"] == "Urban"]["mpce_constant_2011_12_inr"].tolist()
    rural_const = sub[sub["sector"] == "Rural"]["mpce_constant_2011_12_inr"].tolist()

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years, y=urban_curr, name="Urban MPCE (Current ₹)", marker_color="#2563eb",
        hovertemplate="Urban Current: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=years, y=rural_curr, name="Rural MPCE (Current ₹)", marker_color="#10b981",
        hovertemplate="Rural Current: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=years, y=urban_const, mode="lines+markers", name="Urban Real (2011-12 ₹)",
        line={"color": "#1d4ed8", "width": 3, "dash": "dash"}, marker={"size": 8},
        hovertemplate="Urban Constant: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=years, y=rural_const, mode="lines+markers", name="Rural Real (2011-12 ₹)",
        line={"color": "#047857", "width": 3, "dash": "dash"}, marker={"size": 8},
        hovertemplate="Rural Constant: ₹%{y:,.0f}<extra></extra>"
    ))

    return format_chart_layout(fig, f"All-India MPCE Growth: Current vs Constant (2011-12) Prices ({val_filter})", 440)


def create_fractile_curve_chart(df_fractile: pd.DataFrame, selected_round: str = "2023-24") -> go.Figure:
    """
    Renders the fractile distribution across 12 fractile classes / percentile groups (0-5% to 95-100%).
    Dynamic across selected survey round.
    """
    df_rnd = df_fractile[df_fractile["survey_round"] == selected_round]
    if df_rnd.empty:
        df_rnd = df_fractile[df_fractile["survey_round"] == "2023-24"]
        selected_round = "2023-24"

    fig = px.line(
        df_rnd,
        x="fractile_class",
        y="avg_mpce",
        color="sector",
        markers=True,
        color_discrete_map={"Rural": "#10b981", "Urban": "#2563eb"},
        labels={"fractile_class": "Fractile Class (Percentile Group)", "avg_mpce": "Average MPCE (₹/month)", "sector": "Sector"}
    )
    fig.update_traces(line={"width": 3}, marker={"size": 7})

    if selected_round == "2023-24":
        bot_r = df_rnd[(df_rnd["sector"] == "Rural") & (df_rnd["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
        bot_u = df_rnd[(df_rnd["sector"] == "Urban") & (df_rnd["fractile_class"] == "0-5%")]["avg_mpce"].values[0]
        fig.add_annotation(
            x="0-5%", y=bot_u, text=f"Bottom 5%: Rural ₹{bot_r:,.0f} (+22.1% YoY), Urban ₹{bot_u:,.0f} (+18.7% YoY)",
            showarrow=True, arrowhead=2, ax=40, ay=-40, font={"size": 11, "color": "#0f172a"},
            bgcolor="#f1f5f9", bordercolor="#cbd5e1"
        )
    return format_chart_layout(fig, f"Consumption Distribution across Fractile Classes ({selected_round})", 420)


def create_state_bar_chart(df_state: pd.DataFrame, selected_round: str = "2023-24", valuation_col: str = "mpce_unimputed", sector_view: str = "Both") -> go.Figure:
    """
    Creates a ranked horizontal bar chart of states and union territories.
    Gracefully handles missing observations.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    filtered = filtered.dropna(subset=[valuation_col])

    if filtered.empty:
        fig = go.Figure()
        fig.add_annotation(text="No published data available for selected filters", showarrow=False, font={"size": 14})
        return format_chart_layout(fig, "State & UT Consumption Ranking — No Data Available", 400)

    if sector_view in ["Rural", "Urban"]:
        filtered = filtered[filtered["sector"] == sector_view]
        filtered = filtered.sort_values(by=valuation_col, ascending=True)
        fig = px.bar(
            filtered,
            y="state_name",
            x=valuation_col,
            orientation="h",
            color_discrete_sequence=["#10b981" if sector_view == "Rural" else "#2563eb"],
            labels={"state_name": "State / UT", valuation_col: "MPCE (₹/month)"}
        )
    else:
        # Grouped horizontal bars sorted by Urban MPCE (falling back to Rural if Urban missing)
        piv = filtered.pivot(index="state_name", columns="sector", values=valuation_col)
        sort_col = "Urban" if "Urban" in piv.columns else "Rural"
        order = piv.sort_values(by=sort_col, ascending=True).index.tolist()
        fig = px.bar(
            filtered,
            y="state_name",
            x=valuation_col,
            color="sector",
            barmode="group",
            orientation="h",
            category_orders={"state_name": order},
            color_discrete_map={"Rural": "#10b981", "Urban": "#2563eb"},
            labels={"state_name": "State / UT", valuation_col: "MPCE (₹/month)", "sector": "Sector"}
        )

    val_label = "With Welfare Transfers" if "imputed" in valuation_col and "un" not in valuation_col else "Out-of-Pocket"
    chart_height = max(400, min(850, len(filtered["state_name"].unique()) * 26))
    return format_chart_layout(fig, f"State & UT Consumption Ranking — {selected_round} ({val_label})", chart_height)


def create_disparity_scatter_chart(df_state: pd.DataFrame, selected_round: str = "2023-24", valuation_col: str = "mpce_unimputed") -> go.Figure:
    """
    Plots Rural MPCE vs Urban MPCE with parity line (1:1) and national benchmark.
    Harmonized with the state filter selection.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    pivoted = filtered.pivot(index="state_name", columns="sector", values=valuation_col).dropna().reset_index()

    if pivoted.empty:
        fig = go.Figure()
        fig.add_annotation(text="No paired Rural-Urban observations available for selected filters", showarrow=False, font={"size": 14})
        return format_chart_layout(fig, f"Urban-Rural Consumption Disparity & Convergence ({selected_round})", 400)

    pivoted["ratio"] = (pivoted["Urban"] / pivoted["Rural"]).round(2)

    fig = px.scatter(
        pivoted,
        x="Rural",
        y="Urban",
        text="state_name",
        hover_data={"Rural": ":,.0f", "Urban": ":,.0f", "ratio": True},
        color="ratio",
        color_continuous_scale="Blues",
        labels={"Rural": "Rural MPCE (₹/month)", "Urban": "Urban MPCE (₹/month)", "ratio": "Urban/Rural Ratio"}
    )
    fig.update_traces(textposition="top center", marker={"size": 10})
    
    # Compute dynamic national benchmark ratio for selected round & valuation
    ai_rows = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] == "All-India")]
    r_ai = ai_rows[ai_rows["sector"] == "Rural"][valuation_col].values
    u_ai = ai_rows[ai_rows["sector"] == "Urban"][valuation_col].values
    
    if len(r_ai) > 0 and len(u_ai) > 0 and pd.notnull(r_ai[0]) and pd.notnull(u_ai[0]) and r_ai[0] > 0:
        nat_ratio = u_ai[0] / r_ai[0]
    else:
        val_name = "imputed" if "imputed" in valuation_col and "un" not in valuation_col else "unimputed"
        defaults = {
            ("2023-24", "unimputed"): 6996.0 / 4122.0,
            ("2023-24", "imputed"): 7078.0 / 4247.0,
            ("2022-23", "unimputed"): 6459.0 / 3773.0,
            ("2022-23", "imputed"): 6521.0 / 3860.0
        }
        nat_ratio = defaults.get((selected_round, val_name), 1.70)

    val_label = "With Transfers" if "imputed" in valuation_col and "un" not in valuation_col else "Out-of-Pocket"
    benchmark_label = f"National {nat_ratio:.2f}× Benchmark ({selected_round}, {val_label})"

    max_val = max(pivoted["Rural"].max(), pivoted["Urban"].max()) * 1.05
    fig.add_trace(go.Scatter(
        x=[0, max_val / nat_ratio], y=[0, max_val], mode="lines",
        line={"color": "#94a3b8", "dash": "dot"}, name=benchmark_label
    ))
    return format_chart_layout(fig, f"Urban-Rural Consumption Disparity & Convergence ({selected_round})", 540)


def create_category_comparison_chart(df_category: pd.DataFrame, selected_sector: str = "Rural", valuation_filter: str = "Unimputed") -> go.Figure:
    """
    Plots commodity shares comparing 2022-23 vs 2023-24.
    If Imputed is selected, displays 2022-23 Imputed shares alongside clear annotation
    that 2023-24 item-level imputed shares were not published by MoSPI.
    """
    filtered = df_category[(df_category["sector"] == selected_sector) & (df_category["valuation"] == valuation_filter)]
    
    if filtered[filtered["survey_round"] == "2023-24"].empty:
        # Only 2022-23 available for this valuation
        order = filtered.sort_values(by="share_pct", ascending=True)["category"].tolist()
        fig = px.bar(
            filtered,
            y="category",
            x="share_pct",
            color="survey_round",
            orientation="h",
            category_orders={"category": order},
            color_discrete_map={"2022-23": "#0284c7"},
            labels={"category": "Commodity Group", "share_pct": "Share of MPCE (%)", "survey_round": "Survey Round"}
        )
        fig.add_annotation(
            text="Note: MoSPI did NOT publish item-group category breakdown with welfare imputation for 2023-24.<br>Comparisons are restricted to the official Unimputed basis (Figures 4–7).",
            xref="paper", yref="paper", x=0.5, y=-0.15, showarrow=False,
            font={"size": 11, "color": "#b91c1c"}
        )
        return format_chart_layout(fig, f"Commodity Budget Allocation: 2022-23 ({selected_sector}, {valuation_filter})", 620)

    order = filtered[filtered["survey_round"] == "2023-24"].sort_values(by="share_pct", ascending=True)["category"].tolist()
    
    fig = px.bar(
        filtered,
        y="category",
        x="share_pct",
        color="survey_round",
        barmode="group",
        orientation="h",
        category_orders={"category": order},
        color_discrete_map={"2022-23": "#94a3b8", "2023-24": "#0284c7"},
        labels={"category": "Commodity Group", "share_pct": "Share of MPCE (%)", "survey_round": "Survey Round"}
    )
    return format_chart_layout(fig, f"Commodity Budget Allocation: 2022-23 vs 2023-24 ({selected_sector}, {valuation_filter})", 620)


def create_cpi_trends_chart(df_cpi: pd.DataFrame, base_selection: str = "2024=100") -> go.Figure:
    """
    Plots CPI inflation trends including BOTH Headline General Inflation and CFPI Food Inflation.
    """
    filtered = df_cpi[df_cpi["base_year"] == base_selection]
    
    fig = go.Figure()

    if base_selection == "2024=100":
        # 2024 Base monthly series: Plot YoY inflation for Combined, Rural, Urban
        combined_inf = filtered[(filtered["sector"] == "Combined") & (filtered["inflation_general_pct"].notnull())]
        rural_inf = filtered[(filtered["sector"] == "Rural") & (filtered["inflation_general_pct"].notnull())]
        urban_inf = filtered[(filtered["sector"] == "Urban") & (filtered["inflation_general_pct"].notnull())]

        # General Headline Inflation lines
        fig.add_trace(go.Scatter(
            x=combined_inf["month_year"], y=combined_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Combined)",
            line={"color": "#0f172a", "width": 3}, marker={"size": 8}
        ))
        fig.add_trace(go.Scatter(
            x=rural_inf["month_year"], y=rural_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Rural)",
            line={"color": "#10b981", "width": 2}, marker={"size": 6}
        ))
        fig.add_trace(go.Scatter(
            x=urban_inf["month_year"], y=urban_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Urban)",
            line={"color": "#2563eb", "width": 2}, marker={"size": 6}
        ))

        # CFPI Food Inflation points (Jul-26 and Aug-26 from Table 2 & 19)
        cfpi_data = filtered[(filtered["sector"] == "Combined") & (filtered["inflation_food_pct"].notnull())]
        if not cfpi_data.empty:
            fig.add_trace(go.Scatter(
                x=cfpi_data["month_year"], y=cfpi_data["inflation_food_pct"],
                mode="lines+markers", name="CFPI Food Inflation (Combined)",
                line={"color": "#d97706", "width": 3, "dash": "dash"}, marker={"size": 10, "symbol": "diamond"}
            ))
    else:
        # Base 2012=100 Historical Benchmarks
        comb_12 = filtered[filtered["sector"] == "Combined"]
        fig.add_trace(go.Scatter(
            x=comb_12["month_year"], y=comb_12["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Base 2012)",
            line={"color": "#0f172a", "width": 3}, marker={"size": 8}
        ))
        fig.add_trace(go.Scatter(
            x=comb_12["month_year"], y=comb_12["inflation_food_pct"],
            mode="lines+markers", name="CFPI Food Inflation (Base 2012)",
            line={"color": "#d97706", "width": 3, "dash": "dash"}, marker={"size": 8, "symbol": "diamond"}
        ))

    return format_chart_layout(fig, f"MoSPI Consumer Price Index (CPI) Inflation & CFPI — Base {base_selection}", 440)
