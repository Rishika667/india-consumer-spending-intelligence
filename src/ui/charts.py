"""
ConsumerLens India — High-Quality Plotly Chart Generators
Engineered for syndicated research reports: restrained palette, clean formatting,
legible typography, non-colliding legends, and responsive margins.
"""

import os
from typing import Optional, Dict, Any
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
TEXT_DARK = "#0f172a"
TEXT_MUTED = "#334155"
GRID_COLOR = "#f1f5f9"


def format_chart_layout(
    fig: go.Figure,
    title: str = "",
    height: int = 450,
    margin: Optional[Dict[str, int]] = None,
    legend_pos: str = "bottom"
) -> go.Figure:
    """
    Standardizes layout parameters across all dashboard charts to prevent title,
    legend, and axis label collisions across screen widths.
    """
    if margin is None:
        if legend_pos == "bottom":
            margin = {"l": 65, "r": 30, "t": 55, "b": 75}
        elif legend_pos == "top":
            margin = {"l": 65, "r": 30, "t": 85, "b": 45}
        else:
            margin = {"l": 65, "r": 30, "t": 55, "b": 45}

    legend_cfg: Dict[str, Any] = {
        "orientation": "h",
        "font": {"size": 11, "family": "Inter, sans-serif"},
        "bgcolor": "rgba(255, 255, 255, 0.85)",
        "bordercolor": "rgba(226, 232, 240, 0.7)",
        "borderwidth": 1
    }

    if legend_pos == "bottom":
        legend_cfg.update({"yanchor": "top", "y": -0.22, "xanchor": "center", "x": 0.5})
    elif legend_pos == "top":
        legend_cfg.update({"yanchor": "bottom", "y": 1.04, "xanchor": "right", "x": 1.0})
    elif legend_pos == "none":
        legend_cfg = {"visible": False}

    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 14, "color": TEXT_DARK, "family": "Inter, sans-serif"},
            "x": 0.01,
            "xanchor": "left",
            "y": 0.98,
            "yanchor": "top"
        },
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=margin,
        height=height,
        font={"family": "Inter, sans-serif", "color": TEXT_MUTED, "size": 11},
        legend=legend_cfg,
        hoverlabel={"bgcolor": "#1e293b", "font_size": 12, "font_color": "#ffffff"}
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=GRID_COLOR, zeroline=False, automargin=True)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=GRID_COLOR, zeroline=False, automargin=True)
    return fig


def create_trend_trajectory_chart(df_traj=None, valuation_mode: str = "Unimputed") -> go.Figure:
    """
    Shows national consumption trajectory across survey rounds (2011-12, 2022-23, 2023-24).
    Compares current prices vs constant (2011-12) prices using official Table 1 & Table 2.
    Explicitly enforces categorical x-axis to prevent datetime auto-parsing.
    """
    if isinstance(df_traj, str):
        valuation_mode = df_traj
        df_traj = None
    if df_traj is None or (isinstance(df_traj, pd.DataFrame) and df_traj.empty):
        traj_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data", "processed", "national_trajectory.csv"
        )
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
        x=years,
        y=urban_curr,
        name="Urban MPCE (Current ₹)",
        marker_color="#2563eb",
        hovertemplate="<b>Urban (Current)</b><br>Round: %{x}<br>MPCE: ₹%{y:,.0f}/month<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=years,
        y=rural_curr,
        name="Rural MPCE (Current ₹)",
        marker_color="#10b981",
        hovertemplate="<b>Rural (Current)</b><br>Round: %{x}<br>MPCE: ₹%{y:,.0f}/month<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=years,
        y=urban_const,
        mode="lines+markers",
        name="Urban Real (2011-12 ₹)",
        line={"color": "#1d4ed8", "width": 2.5, "dash": "dash"},
        marker={"size": 8, "symbol": "diamond"},
        hovertemplate="<b>Urban Real (2011-12 Prices)</b><br>Round: %{x}<br>MPCE: ₹%{y:,.0f}/month<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=years,
        y=rural_const,
        mode="lines+markers",
        name="Rural Real (2011-12 ₹)",
        line={"color": "#047857", "width": 2.5, "dash": "dash"},
        marker={"size": 8, "symbol": "circle"},
        hovertemplate="<b>Rural Real (2011-12 Prices)</b><br>Round: %{x}<br>MPCE: ₹%{y:,.0f}/month<extra></extra>"
    ))

    fig.update_layout(barmode="group")
    fig.update_xaxes(
        type="category",
        tickmode="array",
        tickvals=years,
        ticktext=years,
        title_text="Survey Round / Reference Year",
        automargin=True
    )
    fig.update_yaxes(
        title_text="Monthly Per Capita Expenditure (₹)",
        tickformat=",,.0f",
        automargin=True
    )

    val_desc = "With In-Kind Welfare Transfers" if val_filter == "Imputed" else "Out-of-Pocket"
    return format_chart_layout(
        fig,
        f"All-India MPCE Growth: Current vs. Constant (2011-12) Prices ({val_desc})",
        height=450,
        legend_pos="bottom"
    )


def create_fractile_curve_chart(df_fractile: pd.DataFrame, selected_round: str = "2023-24") -> go.Figure:
    """
    Renders the fractile distribution across 12 fractile classes / percentile groups (0-5% to 95-100%).
    Dynamic across selected survey round with clear rural/urban visual distinction and bottom-fractile callout.
    """
    df_rnd = df_fractile[df_fractile["survey_round"] == selected_round]
    if df_rnd.empty:
        df_rnd = df_fractile[df_fractile["survey_round"] == "2023-24"]
        selected_round = "2023-24"

    fig = go.Figure()

    r_data = df_rnd[df_rnd["sector"] == "Rural"]
    u_data = df_rnd[df_rnd["sector"] == "Urban"]

    if not r_data.empty:
        fig.add_trace(go.Scatter(
            x=r_data["fractile_class"],
            y=r_data["avg_mpce"],
            mode="lines+markers",
            name="Rural Households",
            line={"color": "#059669", "width": 2.5},
            marker={"size": 7, "symbol": "circle"},
            hovertemplate="<b>Rural</b><br>Fractile: %{x}<br>Avg MPCE: ₹%{y:,.0f}/month<extra></extra>"
        ))

    if not u_data.empty:
        fig.add_trace(go.Scatter(
            x=u_data["fractile_class"],
            y=u_data["avg_mpce"],
            mode="lines+markers",
            name="Urban Households",
            line={"color": "#2563eb", "width": 2.5},
            marker={"size": 7, "symbol": "diamond"},
            hovertemplate="<b>Urban</b><br>Fractile: %{x}<br>Avg MPCE: ₹%{y:,.0f}/month<extra></extra>"
        ))

    fig.update_xaxes(
        type="category",
        tickangle=-25,
        title_text="Fractile Class (Percentile Cohort)",
        automargin=True
    )
    fig.update_yaxes(
        title_text="Average MPCE (₹/month)",
        tickformat=",,.0f",
        automargin=True
    )

    if selected_round == "2023-24" and not r_data.empty and not u_data.empty:
        r_bot = r_data[r_data["fractile_class"] == "0-5%"]["avg_mpce"].values
        u_bot = u_data[u_data["fractile_class"] == "0-5%"]["avg_mpce"].values
        if len(r_bot) > 0 and len(u_bot) > 0:
            fig.add_annotation(
                x="0-5%",
                y=float(u_bot[0]),
                text=f"Bottom 5%: Rural ₹{r_bot[0]:,.0f} (+22.1% YoY) | Urban ₹{u_bot[0]:,.0f} (+18.7% YoY)",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor="#64748b",
                ax=55,
                ay=-55,
                font={"size": 10, "color": "#0f172a"},
                bgcolor="rgba(248, 250, 252, 0.95)",
                bordercolor="#cbd5e1",
                borderwidth=1
            )

    return format_chart_layout(
        fig,
        f"Consumption Distribution across Fractile Classes ({selected_round})",
        height=450,
        legend_pos="bottom"
    )


def create_state_bar_chart(
    df_state: pd.DataFrame,
    selected_round: str = "2023-24",
    valuation_col: str = "mpce_unimputed",
    sector_view: str = "Both"
) -> go.Figure:
    """
    Creates a ranked horizontal bar chart of states and union territories.
    Gracefully handles missing observations and reserves adequate margin for state names.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    filtered = filtered.dropna(subset=[valuation_col])

    if filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No published data available for selected geographic filter",
            showarrow=False,
            font={"size": 13, "color": "#64748b"}
        )
        return format_chart_layout(fig, "State & UT Consumption Ranking — No Data Available", 400)

    if sector_view in ["Rural", "Urban"]:
        filtered = filtered[filtered["sector"] == sector_view]
        filtered = filtered.sort_values(by=valuation_col, ascending=True)
        fig = px.bar(
            filtered,
            y="state_name",
            x=valuation_col,
            orientation="h",
            color_discrete_sequence=["#059669" if sector_view == "Rural" else "#2563eb"],
            labels={"state_name": "State / UT", valuation_col: "MPCE (₹/month)"}
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>" + f"{sector_view} MPCE: ₹%{{x:,.0f}}/month<extra></extra>"
        )
    else:
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
            color_discrete_map={"Rural": "#059669", "Urban": "#2563eb"},
            labels={"state_name": "State / UT", valuation_col: "MPCE (₹/month)", "sector": "Sector"}
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b> (%{data.name})<br>MPCE: ₹%{x:,.0f}/month<extra></extra>"
        )

    fig.update_xaxes(title_text="Monthly Per Capita Expenditure (₹/month)", tickformat=",,.0f", automargin=True)
    fig.update_yaxes(title_text="State / Union Territory", automargin=True)

    val_label = "With Welfare Transfers" if "imputed" in valuation_col and "un" not in valuation_col else "Out-of-Pocket"
    num_states = len(filtered["state_name"].unique())
    chart_height = max(420, min(860, num_states * 28 + 120))

    return format_chart_layout(
        fig,
        f"State & UT Consumption Ranking — {selected_round} ({val_label})",
        height=chart_height,
        margin={"l": 190, "r": 35, "t": 60, "b": 50},
        legend_pos="top" if sector_view == "Both" else "none"
    )


def create_disparity_scatter_chart(
    df_state: pd.DataFrame,
    selected_round: str = "2023-24",
    valuation_col: str = "mpce_unimputed"
) -> go.Figure:
    """
    Plots Rural MPCE vs Urban MPCE with parity line (1:1) and national benchmark.
    Fixes state label overlap by:
    1. Using interactive hover details for all states.
    2. Selectively labeling only prominent frontier extremes (top/bottom rural, highest/lowest ratio).
    3. Retaining national benchmark reference line with dynamic valuation basis.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    pivoted = filtered.pivot(index="state_name", columns="sector", values=valuation_col).dropna().reset_index()

    if pivoted.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No paired Rural-Urban observations available for selected filters",
            showarrow=False,
            font={"size": 13, "color": "#64748b"}
        )
        return format_chart_layout(fig, f"Urban-Rural Consumption Disparity ({selected_round})", 420)

    pivoted["ratio"] = (pivoted["Urban"] / pivoted["Rural"]).round(2)

    # Selective visible labels: anchor the four corners/extremes of the distribution
    labeled_states = set()
    if len(pivoted) > 6:
        labeled_states.update(pivoted.nlargest(2, "Rural")["state_name"].tolist())
        labeled_states.update(pivoted.nsmallest(2, "Rural")["state_name"].tolist())
        labeled_states.update(pivoted.nlargest(1, "ratio")["state_name"].tolist())
        labeled_states.update(pivoted.nsmallest(1, "ratio")["state_name"].tolist())
    else:
        labeled_states.update(pivoted["state_name"].tolist())

    pivoted["display_text"] = pivoted["state_name"].apply(lambda s: s if s in labeled_states else "")

    custom_data = np.stack((pivoted["state_name"], pivoted["ratio"]), axis=-1)

    fig = go.Figure()

    # Main scatter trace
    fig.add_trace(go.Scatter(
        x=pivoted["Rural"],
        y=pivoted["Urban"],
        mode="markers+text",
        text=pivoted["display_text"],
        textposition="top right",
        textfont={"size": 10, "color": "#1e293b", "family": "Inter, sans-serif"},
        customdata=custom_data,
        marker={
            "size": 10,
            "color": pivoted["ratio"],
            "colorscale": "Blues",
            "showscale": True,
            "colorbar": {
                "title": {"text": "Urban/Rural<br>Ratio", "font": {"size": 11}},
                "thickness": 14,
                "len": 0.7,
                "y": 0.5
            },
            "line": {"color": "#1e3a8a", "width": 1}
        },
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Rural MPCE: ₹%{x:,.0f}/month<br>"
            "Urban MPCE: ₹%{y:,.0f}/month<br>"
            "Urban/Rural Ratio: %{customdata[1]:.2f}×<extra></extra>"
        ),
        name="States / UTs"
    ))

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
    max_axis = max(max_val, 13000)

    # National Benchmark Line
    fig.add_trace(go.Scatter(
        x=[0, max_axis / nat_ratio],
        y=[0, max_axis],
        mode="lines",
        line={"color": "#475569", "width": 2, "dash": "dash"},
        name=benchmark_label
    ))

    # Parity Line (1.00x)
    fig.add_trace(go.Scatter(
        x=[0, max_axis],
        y=[0, max_axis],
        mode="lines",
        line={"color": "#cbd5e1", "width": 1.5, "dash": "dot"},
        name="Parity Line (1.00×)"
    ))

    fig.update_xaxes(
        title_text="Rural MPCE (₹/month)",
        tickformat=",,.0f",
        automargin=True
    )
    fig.update_yaxes(
        title_text="Urban MPCE (₹/month)",
        tickformat=",,.0f",
        automargin=True
    )

    return format_chart_layout(
        fig,
        f"Urban-Rural Consumption Disparity & Convergence ({selected_round})",
        height=540,
        margin={"l": 70, "r": 35, "t": 65, "b": 70},
        legend_pos="bottom"
    )


def create_category_comparison_chart(
    df_category: pd.DataFrame,
    selected_sector: str = "Rural",
    valuation_filter: str = "Unimputed"
) -> go.Figure:
    """
    Plots commodity shares comparing 2022-23 vs 2023-24.
    Reserves generous left margin for category labels and positions notes cleanly.
    """
    filtered = df_category[(df_category["sector"] == selected_sector) & (df_category["valuation"] == valuation_filter)]

    if filtered[filtered["survey_round"] == "2023-24"].empty:
        # Only 2022-23 available for this valuation (e.g. Imputed series)
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
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>2022-23 Share: %{x:.2f}% of MPCE<extra></extra>"
        )
        fig.update_xaxes(
            title_text="Share of Monthly Per Capita Expenditure (% of MPCE)",
            automargin=True
        )
        fig.update_yaxes(title_text="Commodity Group", automargin=True)

        return format_chart_layout(
            fig,
            f"Commodity Budget Allocation: 2022-23 ({selected_sector}, {valuation_filter})",
            height=640,
            margin={"l": 210, "r": 35, "t": 60, "b": 60},
            legend_pos="top"
        )

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
    fig.update_traces(
        hovertemplate="<b>%{y}</b> (%{data.name})<br>Share: %{x:.2f}% of MPCE<extra></extra>"
    )
    fig.update_xaxes(
        title_text="Share of Monthly Per Capita Expenditure (% of MPCE)",
        automargin=True
    )
    fig.update_yaxes(title_text="Commodity Group", automargin=True)

    return format_chart_layout(
        fig,
        f"Commodity Budget Allocation: 2022-23 vs 2023-24 ({selected_sector}, {valuation_filter})",
        height=640,
        margin={"l": 210, "r": 35, "t": 65, "b": 60},
        legend_pos="top"
    )


def create_cpi_trends_chart(df_cpi: pd.DataFrame, base_selection: str = "2024=100") -> go.Figure:
    """
    Plots CPI inflation trends including General Headline Inflation and CFPI Food Inflation.
    """
    filtered = df_cpi[df_cpi["base_year"] == base_selection]
    fig = go.Figure()

    if base_selection == "2024=100":
        combined_inf = filtered[(filtered["sector"] == "Combined") & (filtered["inflation_general_pct"].notnull())]
        rural_inf = filtered[(filtered["sector"] == "Rural") & (filtered["inflation_general_pct"].notnull())]
        urban_inf = filtered[(filtered["sector"] == "Urban") & (filtered["inflation_general_pct"].notnull())]

        fig.add_trace(go.Scatter(
            x=combined_inf["month_year"], y=combined_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Combined)",
            line={"color": "#0f172a", "width": 3}, marker={"size": 7},
            hovertemplate="<b>Headline (Combined)</b><br>Month: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=rural_inf["month_year"], y=rural_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Rural)",
            line={"color": "#059669", "width": 2}, marker={"size": 6},
            hovertemplate="<b>Rural Headline</b><br>Month: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=urban_inf["month_year"], y=urban_inf["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Urban)",
            line={"color": "#2563eb", "width": 2}, marker={"size": 6},
            hovertemplate="<b>Urban Headline</b><br>Month: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
        ))

        cfpi_data = filtered[(filtered["sector"] == "Combined") & (filtered["inflation_food_pct"].notnull())]
        if not cfpi_data.empty:
            fig.add_trace(go.Scatter(
                x=cfpi_data["month_year"], y=cfpi_data["inflation_food_pct"],
                mode="lines+markers", name="CFPI Food Inflation (Combined)",
                line={"color": "#d97706", "width": 2.5, "dash": "dash"}, marker={"size": 9, "symbol": "diamond"},
                hovertemplate="<b>CFPI Food Inflation</b><br>Month: %{x}<br>YoY: %{y:.2f}%<extra></extra>"
            ))
    else:
        comb_12 = filtered[filtered["sector"] == "Combined"]
        fig.add_trace(go.Scatter(
            x=comb_12["month_year"], y=comb_12["inflation_general_pct"],
            mode="lines+markers", name="CPI General (Base 2012)",
            line={"color": "#0f172a", "width": 3}, marker={"size": 8},
            hovertemplate="<b>CPI General (2012)</b><br>Period: %{x}<br>Inflation: %{y:.2f}%<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=comb_12["month_year"], y=comb_12["inflation_food_pct"],
            mode="lines+markers", name="CFPI Food Inflation (Base 2012)",
            line={"color": "#d97706", "width": 2.5, "dash": "dash"}, marker={"size": 8, "symbol": "diamond"},
            hovertemplate="<b>CFPI Food (2012)</b><br>Period: %{x}<br>Inflation: %{y:.2f}%<extra></extra>"
        ))

    fig.update_xaxes(title_text="Month / Reference Period", automargin=True)
    fig.update_yaxes(title_text="Year-on-Year Inflation Rate (%)", tickformat=".1f", automargin=True)

    return format_chart_layout(
        fig,
        f"MoSPI Consumer Price Index (CPI) Inflation & CFPI — Base {base_selection}",
        height=450,
        legend_pos="bottom"
    )
