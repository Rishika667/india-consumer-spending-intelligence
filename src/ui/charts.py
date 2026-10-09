"""
ConsumerLens India — High-Quality Plotly Chart Generators
Engineered for syndicated research reports: restrained palette, clean formatting, and legible typography.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


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


def create_trend_trajectory_chart(valuation_mode: str = "Unimputed") -> go.Figure:
    """
    Shows national consumption trajectory across survey rounds (2011-12, 2022-23, 2023-24).
    Compares current prices vs constant (2011-12) prices.
    """
    years = ["2011-12", "2022-23", "2023-24"]
    
    if valuation_mode == "Unimputed":
        rural_curr = [1430, 3773, 4122]
        rural_const = [1430, 2008, 2079]
        urban_curr = [2630, 6459, 6996]
        urban_const = [2630, 3510, 3632]
    else:
        rural_curr = [1430, 3860, 4247]
        rural_const = [1430, 2054, 2142]
        urban_curr = [2630, 6521, 7078]
        urban_const = [2630, 3544, 3674]

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

    return format_chart_layout(fig, f"All-India MPCE Growth: Current vs Constant (2011-12) Prices ({valuation_mode})", 440)


def create_fractile_curve_chart(df_fractile: pd.DataFrame) -> go.Figure:
    """
    Renders the fractile distribution across 12 decile classes for 2022-23 and 2023-24.
    """
    df_23 = df_fractile[df_fractile["survey_round"] == "2023-24"]
    
    fig = px.line(
        df_23,
        x="fractile_class",
        y="avg_mpce",
        color="sector",
        markers=True,
        color_discrete_map={"Rural": "#10b981", "Urban": "#2563eb"},
        labels={"fractile_class": "Fractile Class (Percentiles)", "avg_mpce": "Average MPCE (₹/month)", "sector": "Sector"}
    )
    fig.update_traces(line={"width": 3}, marker={"size": 7})
    fig.add_annotation(
        x="0-5%", y=2376, text="Bottom 5%: Rural ₹1,677 (+22%), Urban ₹2,376 (+19%)",
        showarrow=True, arrowhead=2, ax=40, ay=-40, font={"size": 11, "color": "#0f172a"},
        bgcolor="#f1f5f9", bordercolor="#cbd5e1"
    )
    return format_chart_layout(fig, "Consumption Expenditure Distribution across Fractile Classes (2023-24)", 420)


def create_state_bar_chart(df_state: pd.DataFrame, selected_round: str = "2023-24", valuation_col: str = "mpce_unimputed", sector_view: str = "Both") -> go.Figure:
    """
    Creates a ranked horizontal bar chart of states and union territories.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    
    if sector_view in ["Rural", "Urban"]:
        filtered = filtered[filtered["sector"] == sector_view]
        filtered = filtered.sort_values(by=valuation_col, ascending=True)
        fig = px.bar(
            filtered,
            y="state_name",
            x=valuation_col,
            orientation="h",
            color_discrete_sequence=["#10b981" if sector_view == "Rural" else "#2563eb"],
            labels={"state_name": "State / UT", valuation_col: f"MPCE (₹/month)"}
        )
    else:
        # Side-by-side grouped horizontal bars
        # Sort states by Urban MPCE
        order = filtered[filtered["sector"] == "Urban"].sort_values(by=valuation_col)["state_name"].tolist()
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
    return format_chart_layout(fig, f"State & UT Consumption Ranking — {selected_round} ({val_label})", 720)


def create_disparity_scatter_chart(df_state: pd.DataFrame, selected_round: str = "2023-24", valuation_col: str = "mpce_unimputed") -> go.Figure:
    """
    Plots Rural MPCE vs Urban MPCE with parity line (1:1) and national benchmark.
    """
    filtered = df_state[(df_state["survey_round"] == selected_round) & (df_state["state_name"] != "All-India")]
    pivoted = filtered.pivot(index="state_name", columns="sector", values=valuation_col).dropna().reset_index()
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
    
    # 1.70x national reference line
    max_val = max(pivoted["Rural"].max(), pivoted["Urban"].max()) * 1.05
    fig.add_trace(go.Scatter(
        x=[0, max_val / 1.70], y=[0, max_val], mode="lines",
        line={"color": "#94a3b8", "dash": "dot"}, name="National 1.70x Ratio Line"
    ))
    return format_chart_layout(fig, f"Urban-Rural Consumption Disparity & Convergence ({selected_round})", 540)


def create_category_comparison_chart(df_category: pd.DataFrame, selected_sector: str = "Rural", valuation_filter: str = "Unimputed") -> go.Figure:
    """
    Plots commodity shares comparing 2022-23 vs 2023-24.
    """
    filtered = df_category[(df_category["sector"] == selected_sector) & (df_category["valuation"] == valuation_filter)]
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
    Plots CPI inflation trends for General vs Food components.
    """
    filtered = df_cpi[df_cpi["base_year"] == base_selection]
    
    fig = px.line(
        filtered,
        x="month_year",
        y="inflation_general_pct",
        color="sector",
        markers=True,
        labels={"month_year": "Month", "inflation_general_pct": "YoY Inflation Rate (%)", "sector": "Sector"},
        color_discrete_map={"Combined": "#0f172a", "Rural": "#10b981", "Urban": "#2563eb"}
    )
    fig.update_traces(line={"width": 3}, marker={"size": 8})
    return format_chart_layout(fig, f"MoSPI Consumer Price Index (CPI) Inflation — Base {base_selection}", 420)
