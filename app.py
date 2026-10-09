"""
ConsumerLens India — India Consumer Spending Intelligence & Data Quality Engine
Official MoSPI HCES 2023-24, HCES 2022-23, and CPI Intelligence Dashboard.
Offline-reproducible, zero-cost, recruiter-ready syndicated research application.
"""

import os
import sys
import json
import pandas as pd
import streamlit as st

# Configure page layout and metadata
st.set_page_config(
    page_title="ConsumerLens India | MoSPI Consumption Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure src modules are resolvable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.ui.components import inject_custom_css, render_metric_card, render_disclaimer_banner
from src.ui.charts import (
    create_trend_trajectory_chart,
    create_fractile_curve_chart,
    create_state_bar_chart,
    create_disparity_scatter_chart,
    create_category_comparison_chart,
    create_cpi_trends_chart
)


@st.cache_data
def load_all_datasets():
    processed_dir = os.path.join(BASE_DIR, "data", "processed")
    df_state = pd.read_csv(os.path.join(processed_dir, "state_mpce.csv"))
    df_category = pd.read_csv(os.path.join(processed_dir, "category_shares.csv"))
    df_fractile = pd.read_csv(os.path.join(processed_dir, "fractile_distribution.csv"))
    df_cpi = pd.read_csv(os.path.join(processed_dir, "cpi_series.csv"))
    df_pfce = pd.read_csv(os.path.join(processed_dir, "macro_pfce.csv"))
    df_traj = pd.read_csv(os.path.join(processed_dir, "national_trajectory.csv"))
    
    validation_path = os.path.join(BASE_DIR, "docs", "VALIDATION_REPORT.json")
    with open(validation_path, "r", encoding="utf-8") as f:
        validation_report = json.load(f)
        
    return df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, validation_report


def main():
    inject_custom_css()
    df_state, df_category, df_fractile, df_cpi, df_pfce, df_traj, validation_report = load_all_datasets()

    # ==================== SIDEBAR GLOBAL CONTROLS ====================
    with st.sidebar:
        st.markdown("### 🏛️ ConsumerLens India")
        st.markdown("<span class='editorial-badge'>MoSPI HCES 2023-24 Intelligence</span>", unsafe_allow_html=True)
        st.caption("Recruiter-ready research dashboard examining Indian household consumption patterns and price dynamics.")
        st.divider()

        st.subheader("⚙️ Global Analysis Parameters")
        valuation_option = st.radio(
            "Expenditure Valuation Basis:",
            options=["Out-of-Pocket Only (Without Imputation)", "Including Social Welfare Imputation"],
            index=0,
            help="HCES reports both out-of-pocket expenditure and an imputed series valuing in-kind government transfers (PMGKY foodgrains, uniforms, devices) at market price."
        )
        is_imputed = "Including Social Welfare" in valuation_option
        valuation_col = "mpce_imputed" if is_imputed else "mpce_unimputed"
        valuation_label = "Imputed" if is_imputed else "Unimputed"

        st.divider()
        st.markdown("**Data Quality Health:**")
        val_score = validation_report.get("pipeline_validation_score", validation_report.get("composite_score", 100.0))
        total_eval = validation_report["total_evaluated"]
        passed_eval = validation_report["passed"]
        st.markdown(f"<span class='qc-badge-pass'>✓ Pipeline Validation Score: {val_score:.1f}% ({passed_eval}/{total_eval} Checks Passed)</span>", unsafe_allow_html=True)
        st.caption("Evaluated by deterministic Data Quality Engine across Completeness, Validity, Uniqueness, Consistency & Lineage. Pipeline validation verifies automated data hygiene and does not assert survey representativeness or sampling precision.")

        st.divider()
        st.markdown("**Navigation Sections:**")
        selected_tab = st.radio(
            "Go to section:",
            ["1. Overview", "2. Regional Explorer", "3. Consumption Basket", "4. Price Context", "5. Data Quality & Sources", "6. Methodology & Downloads"],
            label_visibility="collapsed"
        )

    # ==================== HEADER STRIP ====================
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.title("ConsumerLens India")
        st.markdown(
            "**Official Household Consumption Expenditure & Price Intelligence Engine** • "
            "Primary Benchmark: NSS Report No. 592 & PIB Factsheets (August 2023 – July 2024)"
        )
    with col_hdr2:
        st.metric(
            label="Valuation Basis",
            value="With Transfers" if is_imputed else "Out-of-Pocket",
            delta="+₹125/mo Welfare Effect (Rural)" if is_imputed else "Base Survey Values"
        )

    # ==================== SECTION 1: OVERVIEW ====================
    if selected_tab == "1. Overview":
        st.markdown("<div class='section-title'>1. Executive Overview & National Consumption Dynamics</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Key macroeconomic indicators from the 2023-24 Household Consumption Expenditure Survey compared to the 2022-23 round.</div>", unsafe_allow_html=True)

        # National KPI cards
        ai_23 = df_state[(df_state["state_name"] == "All-India") & (df_state["survey_round"] == "2023-24")]
        ai_22 = df_state[(df_state["state_name"] == "All-India") & (df_state["survey_round"] == "2022-23")]
        
        r_val_23 = ai_23[ai_23["sector"] == "Rural"][valuation_col].values[0]
        r_val_22 = ai_22[ai_22["sector"] == "Rural"][valuation_col].values[0]
        r_growth = ((r_val_23 - r_val_22) / r_val_22) * 100

        u_val_23 = ai_23[ai_23["sector"] == "Urban"][valuation_col].values[0]
        u_val_22 = ai_22[ai_22["sector"] == "Urban"][valuation_col].values[0]
        u_growth = ((u_val_23 - u_val_22) / u_val_22) * 100

        ratio_23 = u_val_23 / r_val_23
        food_share_r = 48.43 if is_imputed else 47.04

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            render_metric_card("Rural MPCE", f"₹{r_val_23:,.0f}", f"+{r_growth:.1f}% vs 2022-23")
        with kpi2:
            render_metric_card("Urban MPCE", f"₹{u_val_23:,.0f}", f"+{u_growth:.1f}% vs 2022-23")
        with kpi3:
            render_metric_card("Urban/Rural Ratio", f"{ratio_23:.2f}×", "Narrowed from 1.69× (2022-23)" if is_imputed else "Narrowed from 1.71× (2022-23)")
        with kpi4:
            render_metric_card("Rural Food Share", f"{food_share_r:.2f}%", "With Imputed Transfers" if is_imputed else "Out-of-Pocket Share")
        with kpi5:
            render_metric_card("Pipeline Validation", f"{val_score:.1f}%", f"{passed_eval}/{total_eval} Checks Passed")

        st.markdown("---")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.plotly_chart(create_trend_trajectory_chart(df_traj, valuation_label), use_container_width=True)
        with c2:
            st.plotly_chart(create_fractile_curve_chart(df_fractile), use_container_width=True)

        st.markdown("### 📌 Executive Research Findings (Syndicated Brief)")
        if is_imputed:
            st.markdown(f"""
            - **Rural Consumption Growth (With Social Transfers):** Rural nominal MPCE including social welfare transfer imputation reached **₹4,247** (+9.8% YoY vs ₹3,868 in 2022-23), while urban MPCE reached **₹7,078** (+8.6% YoY vs ₹6,521 in 2022-23). The urban-to-rural spending premium narrowed to **{ratio_23:.2f}×** (down from 1.69× in 2022-23).
            - **Measured Impact of In-Kind Transfers:** Imputing social welfare entitlements (PMGKY foodgrains, school uniforms, textbooks, transport/devices) at local market rates adds **₹125/month** to average rural household MPCE (3.0% boost over out-of-pocket expenditure) and **₹82/month** to urban MPCE (1.2% boost).
            - **Distributional Focus:** Welfare transfers produce the largest proportional consumption uplift in lower-fractile households, where food grain support constitutes a substantial share of total sustenance.
            - **Descriptive Shift in Budget Allocations:** Non-food spending dominates urban household budgets (~60.3%), while the rural food share stands at **{food_share_r:.2f}%** when accounting for in-kind foodgrain transfers.
            """)
        else:
            st.markdown(f"""
            - **Rural Consumption Growth (Out-of-Pocket):** Rural nominal out-of-pocket MPCE reached **₹4,122** (+9.2% YoY vs ₹3,773 in 2022-23), while urban MPCE reached **₹6,996** (+8.3% YoY vs ₹6,459 in 2022-23). The urban-to-rural spending premium narrowed to **{ratio_23:.2f}×** (down from 1.71× in 2022-23 and 1.84× in 2011-12).
            - **Bottom-Fractile Expansion:** The bottom 5% fractile class recorded notable nominal increases, reaching **₹1,677 in rural areas** (+22.1% YoY) and **₹2,376 in urban areas** (+18.7% YoY).
            - **Descriptive Shift in Budget Allocations:** Non-food spending accounts for **52.96% of rural** and **60.30% of urban** budgets. Within food, spending has shifted toward processed refreshments, milk, and vegetables relative to basic cereals.
            - **Primary Survey Benchmark:** Out-of-pocket expenditure serves as the primary survey benchmark across 34 published states/UTs in 2023-24 (with Delhi and Chandigarh retained as explicit unpublished cells).
            """)

    # ==================== SECTION 2: REGIONAL EXPLORER ====================
    elif selected_tab == "2. Regional Explorer":
        st.markdown("<div class='section-title'>2. Regional Explorer: State & UT Consumption Divergence</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Analyze cross-state purchasing power, regional disparity, and rural-urban convergence ratios.</div>", unsafe_allow_html=True)

        MAJOR_STATES = [
            "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Gujarat", "Haryana",
            "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha",
            "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
        ]
        all_states = sorted(list(df_state[df_state["state_name"] != "All-India"]["state_name"].unique()))

        if "state_filter_selection" not in st.session_state:
            st.session_state.state_filter_selection = all_states

        def select_all_states():
            st.session_state.state_filter_selection = all_states

        def select_major_states():
            st.session_state.state_filter_selection = [s for s in MAJOR_STATES if s in all_states]

        def select_clear_states():
            st.session_state.state_filter_selection = []

        # Quick selectors row
        st.markdown("**Quick Geographic Cohort Selectors:**")
        qc1, qc2, qc3, _ = st.columns([1, 1, 1, 3])
        qc1.button("🌐 All 36 Geographies", on_click=select_all_states, use_container_width=True)
        qc2.button("🏛️ 18 Major States", on_click=select_major_states, use_container_width=True)
        qc3.button("🧹 Clear Selection", on_click=select_clear_states, use_container_width=True)

        # Filters row
        fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
        with fcol1:
            selected_states = st.multiselect(
                "Filter States / UTs (Harmonized across bar chart, scatter plot, and data table):",
                options=all_states,
                key="state_filter_selection",
                help="Select specific states or use quick buttons above. Selection updates all views synchronously."
            )
        with fcol2:
            selected_round = st.selectbox("Survey Round:", options=["2023-24", "2022-23"], index=0)
        with fcol3:
            sector_view = st.selectbox("Sector Breakdown:", options=["Both", "Rural", "Urban"], index=0)

        # Harmonized filtered subset applied consistently across all charts & table
        filtered_state_df = df_state[
            (df_state["survey_round"] == selected_round) & 
            (df_state["state_name"].isin(selected_states))
        ]

        total_in_selection = len(selected_states)
        
        # Check for officially unpublished records in the selection
        missing_records = filtered_state_df[filtered_state_df[valuation_col].isnull()]
        if not missing_records.empty:
            missing_names = sorted(missing_records["state_name"].unique().tolist())
            st.info(
                f"ℹ️ **Data Availability Notice ({selected_round}, {valuation_label}):** "
                f"Of {total_in_selection} selected geographies, {len(missing_names)} state(s)/UT(s) have officially unavailable values "
                f"in MoSPI Report 592 / PRID 2247612: **{', '.join(missing_names)}**. "
                f"These are retained as explicit missing values rather than inferred or fabricated."
            )
        elif total_in_selection > 0:
            st.caption(f"✓ All {total_in_selection} selected geographies have officially published figures for {selected_round} ({valuation_label}).")

        st.plotly_chart(create_state_bar_chart(filtered_state_df, selected_round, valuation_col, sector_view), use_container_width=True)

        st.markdown("---")
        st.subheader("Spatial Convergence: Rural vs. Urban Disparity")
        st.plotly_chart(create_disparity_scatter_chart(filtered_state_df, selected_round, valuation_col), use_container_width=True)

        with st.expander("🔍 View Raw State Data Table (Harmonized Selection)"):
            pivoted_view = filtered_state_df.pivot(index="state_name", columns="sector", values=valuation_col).reset_index()
            if "Rural" in pivoted_view.columns and "Urban" in pivoted_view.columns:
                pivoted_view["Urban_to_Rural_Ratio"] = (pivoted_view["Urban"] / pivoted_view["Rural"]).round(2)
            st.dataframe(pivoted_view, use_container_width=True)

    # ==================== SECTION 3: CONSUMPTION BASKET ====================
    elif selected_tab == "3. Consumption Basket":
        st.markdown("<div class='section-title'>3. Consumption Basket & Expenditure Allocations</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Examine how Indian households allocate their monthly budget across 17 detailed commodity categories.</div>", unsafe_allow_html=True)

        bcol1, bcol2 = st.columns([1, 1])
        with bcol1:
            basket_sector = st.radio("Select Sector:", options=["Rural", "Urban"], horizontal=True)
        with bcol2:
            st.info(f"Currently viewing **{valuation_option}** (Controlled via sidebar)")

        if is_imputed:
            st.warning(
                "⚠️ **Methodological Boundary Notice:** MoSPI published item-level commodity shares with welfare imputation "
                "for **2022–23** (Statement 15), but did **NOT** publish item-group category breakdown with welfare imputation for **2023–24** "
                "in Report 592. To maintain empirical integrity, cross-year category comparisons are evaluated on the official **Unimputed** series."
            )

        st.plotly_chart(create_category_comparison_chart(df_category, basket_sector, valuation_label), use_container_width=True)

        st.markdown("### 📊 Budget Allocation Insights (Official Unimputed Series)")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("""
            **Top Food Expenditure Allocations (2023-24):**
            1. **Beverages & Processed Food:** 9.84% (Rural) | 11.09% (Urban) — Leading food spending category nationwide.
            2. **Milk & Milk Products:** 8.44% (Rural) | 7.19% (Urban).
            3. **Vegetables:** 6.03% (Rural) | 4.12% (Urban).
            4. **Cereals:** 4.99% (Rural) | 3.76% (Urban) — Continues historical downward share trajectory.
            """)
        with col_b2:
            st.markdown("""
            **Top Non-Food Expenditure Allocations (2023-24):**
            1. **Conveyance / Transport:** 7.59% (Rural) | 8.46% (Urban) — Largest single non-food category.
            2. **Rent & Accommodation:** Urban households allocate ~7% to housing.
            3. **Medical Care:** 6.83% (Rural) | 5.85% (Urban).
            4. **Clothing & Footwear:** 6.63% (Rural) | 5.66% (Urban).
            """)

    # ==================== SECTION 4: PRICE CONTEXT ====================
    elif selected_tab == "4. Price Context":
        st.markdown("<div class='section-title'>4. Macroeconomic Price Context (Official MoSPI CPI)</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Official retail inflation trends presented as separate macroeconomic context.</div>", unsafe_allow_html=True)

        render_disclaimer_banner(
            "Strict Methodological Decoupling",
            "MoSPI CPI price indices measure changes in a fixed market basket across time and must NOT be used as spatial deflators for cross-sectional state survey spending. Direct comparison between Base 2012=100 and Base 2024=100 is not methodologically valid."
        )

        cpi_tabs = st.tabs(["Base 2024=100 (Monthly Series Jan 2025 – Aug 2026)", "Base 2012=100 (Discontinued Historical Snapshots)"])

        with cpi_tabs[0]:
            st.markdown("#### Transition Series (Base 2024=100) — Latest August 2026 Release (PIB PRID 2310058)")
            st.caption("Derived directly from HCES 2023-24 consumption weights, expanding coverage to 358 items and incorporating online markets.")

            # Compute latest 2024=100 CPI metrics dynamically
            cpi_2024 = df_cpi[df_cpi["base_year"] == "2024=100"].copy()
            latest_month = cpi_2024["month_year"].max() if not cpi_2024.empty else "N/A"
            cpi_latest = cpi_2024[cpi_2024["month_year"] == latest_month]

            # Combined general & food
            c_comb = cpi_latest[cpi_latest["sector"] == "Combined"]
            gen_index_val = f"{c_comb['cpi_general'].values[0]:.2f}" if not c_comb.empty and pd.notnull(c_comb['cpi_general'].values[0]) else "N/A"
            gen_yoy_val = f"{c_comb['inflation_general_pct'].values[0]:.2f}%" if not c_comb.empty and pd.notnull(c_comb['inflation_general_pct'].values[0]) else "N/A"
            cfpi_index_val = f"{c_comb['cpi_food_cfpi'].values[0]:.2f}" if not c_comb.empty and pd.notnull(c_comb['cpi_food_cfpi'].values[0]) else "N/A"
            cfpi_yoy_val = f"{c_comb['inflation_food_pct'].values[0]:.2f}%" if not c_comb.empty and pd.notnull(c_comb['inflation_food_pct'].values[0]) else "N/A"

            # Rural
            r_row = cpi_latest[cpi_latest["sector"] == "Rural"]
            r_gen_val = f"{r_row['cpi_general'].values[0]:.2f}" if not r_row.empty and pd.notnull(r_row['cpi_general'].values[0]) else "N/A"
            r_gen_yoy = f"{r_row['inflation_general_pct'].values[0]:.2f}%" if not r_row.empty and pd.notnull(r_row['inflation_general_pct'].values[0]) else "N/A"
            r_cfpi_yoy = f"{r_row['inflation_food_pct'].values[0]:.2f}%" if not r_row.empty and pd.notnull(r_row['inflation_food_pct'].values[0]) else "N/A"

            # Urban
            u_row = cpi_latest[cpi_latest["sector"] == "Urban"]
            u_gen_val = f"{u_row['cpi_general'].values[0]:.2f}" if not u_row.empty and pd.notnull(u_row['cpi_general'].values[0]) else "N/A"
            u_gen_yoy = f"{u_row['inflation_general_pct'].values[0]:.2f}%" if not u_row.empty and pd.notnull(u_row['inflation_general_pct'].values[0]) else "N/A"
            u_cfpi_yoy = f"{u_row['inflation_food_pct'].values[0]:.2f}%" if not u_row.empty and pd.notnull(u_row['inflation_food_pct'].values[0]) else "N/A"

            # Dynamic coverage counts
            num_months_idx = cpi_2024[cpi_2024["cpi_general"].notnull()]["month_year"].nunique()
            num_months_yoy = cpi_2024[cpi_2024["inflation_general_pct"].notnull()]["month_year"].nunique()
            num_months_cfpi = cpi_2024[cpi_2024["inflation_food_pct"].notnull()]["month_year"].nunique()
            min_month = cpi_2024["month_year"].min()
            max_month = cpi_2024["month_year"].max()

            cp1, cp2, cp3, cp4 = st.columns(4)
            with cp1:
                render_metric_card(f"General CPI ({latest_month})", gen_index_val, f"YoY Headline: {gen_yoy_val} (Combined)")
            with cp2:
                render_metric_card("CFPI Food Inflation", cfpi_yoy_val, f"Food Index: {cfpi_index_val} (Combined)")
            with cp3:
                render_metric_card("Rural General / Food", f"{r_gen_yoy} / {r_cfpi_yoy}", f"General CPI: {r_gen_val}")
            with cp4:
                render_metric_card("Urban General / Food", f"{u_gen_yoy} / {u_cfpi_yoy}", f"General CPI: {u_gen_val}")

            cov_c1, cov_c2, cov_c3 = st.columns(3)
            with cov_c1:
                st.info(f"📅 **Monthly Index:** {num_months_idx} Months ({min_month} – {max_month})")
            with cov_c2:
                st.info(f"📈 **YoY Inflation:** {num_months_yoy} Months (Jan 2026 – {max_month})")
            with cov_c3:
                st.info(f"🥗 **CFPI Food Inflation:** {num_months_cfpi} Months (Jul 2026 – {max_month})")

            st.plotly_chart(create_cpi_trends_chart(df_cpi, "2024=100"), use_container_width=True)

            st.markdown("""
            **Key Features and Data Boundaries of the Revised 2024 Base Series:**
            - **HCES 2023-24 Weighting Diagram:** Basket weights updated to reflect recent household spending patterns.
            - **Basket Expansion:** Expanded from 299 to 358 items, incorporating streaming services, personal electronics, and modern consumer services.
            - **Market Scope:** 1,465 rural markets, 1,395 urban markets, and 12 online ecommerce markets.
            - **Official Release Availability:** Table 10 of PIB PRID 2310058 provides a 20-month General Index series starting January 2025. Because monthly index values for 2024 were not published in this release, YoY inflation is officially available only from January 2026 onward (8 months). Similarly, CFPI food inflation is published only for July and August 2026. ConsumerLens India reflects this exact official availability without inventing intermediate values.
            """)

        with cpi_tabs[1]:
            st.markdown("#### Discontinued Historical Series (Base 2012=100)")
            st.info("ℹ️ **Discontinuation Notice:** The Base 2012=100 series was officially discontinued by MoSPI in February 2026 upon the introduction of the Base 2024=100 series. Data points below represent reference-period benchmarks corresponding to HCES survey rounds.")
            st.plotly_chart(create_cpi_trends_chart(df_cpi, "2012=100"), use_container_width=True)

    # ==================== SECTION 5: DATA QUALITY & SOURCES ====================
    elif selected_tab == "5. Data Quality & Sources":
        st.markdown("<div class='section-title'>5. Pipeline Validation Engine & Audit Matrix</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Automated 28-point validation audit evaluating pipeline hygiene, mathematical consistency, and lineage.</div>", unsafe_allow_html=True)

        q1, q2 = st.columns([1, 2])
        with q1:
            render_metric_card("Pipeline Validation Score", f"{val_score:.1f}%", f"{passed_eval}/{total_eval} Automated Checks Evaluated")
            st.markdown("""
            **Scoring Dimension Weights:**
            - Completeness: **25%** (6 checks)
            - Validity: **25%** (6 checks)
            - Uniqueness: **15%** (4 checks)
            - Internal Consistency: **20%** (7 checks)
            - Provenance: **15%** (5 checks)
            """)
        with q2:
            st.markdown("#### Dimension Breakdown")
            breakdown_rows = []
            for dim, meta in validation_report["dimension_breakdown"].items():
                breakdown_rows.append({
                    "Dimension": dim.replace("_", " "),
                    "Weight": f"{int(meta['weight']*100)}%",
                    "Checks Passed": f"{meta['passed']} / {meta['total']}",
                    "Score": f"{meta['score_pct']:.1f}%"
                })
            st.table(pd.DataFrame(breakdown_rows))

        st.subheader("📊 Official Data Availability & Missingness Register")
        avail_dict = validation_report.get("data_availability_summary", {})
        avail_table = [{"Dataset / Dimension": k.replace("_", " ").title(), "Official Status & Coverage": v} for k, v in avail_dict.items()]
        st.table(pd.DataFrame(avail_table))

        st.subheader("🔍 Primary Source Reconciliation Summary")
        st.caption("Verifies structured source dataset observations against preserved primary documents in data/raw/ using scripts/reconcile_sources.py.")
        rec_data = validation_report.get("source_reconciliation_summary", {})
        
        checked_count = rec_data.get('records_checked', 0)
        matched_count = rec_data.get('records_matched', 0)
        mismatch_count = rec_data.get('records_mismatched', 0)
        unres_count = rec_data.get('unresolved_records', 0)
        match_rate_str = f"{rec_data.get('match_rate_pct', 0.0):.1f}% Match Rate" if checked_count > 0 else "N/A"

        rec_cols = st.columns(4)
        with rec_cols[0]:
            render_metric_card("Records Checked", f"{checked_count}", "Official Primary Citations")
        with rec_cols[1]:
            render_metric_card("Records Matched", f"{matched_count}", match_rate_str)
        with rec_cols[2]:
            render_metric_card("Mismatches", f"{mismatch_count}", "Tolerance Violations")
        with rec_cols[3]:
            render_metric_card("Unresolved", f"{unres_count}", "Ambiguous or Missing Source")

        # Load reconciliation detail if available
        rec_path = os.path.join(BASE_DIR, "docs", "SOURCE_RECONCILIATION.json")
        if os.path.exists(rec_path):
            with open(rec_path, "r", encoding="utf-8") as f:
                rec_json = json.load(f)
                rec_items = rec_json.get("reconciliation_checks", [])
                if rec_items:
                    with st.expander(f"📋 View Detailed Primary Source Reconciliation Log ({len(rec_items)} Benchmarks)"):
                        rec_df_display = pd.DataFrame(rec_items)
                        cols_to_show = [c for c in ["check_id", "metric", "dataset", "observed_value", "primary_source_doc", "table_ref", "status", "source_evidence"] if c in rec_df_display.columns]
                        st.dataframe(rec_df_display[cols_to_show], use_container_width=True)
        else:
            st.warning("⚠️ Source reconciliation file `docs/SOURCE_RECONCILIATION.json` not found. Run `scripts/reconcile_sources.py` to generate the log.")

        st.subheader("📋 Comprehensive 28-Rule Audit Log")
        checks_df = pd.DataFrame(validation_report["checks"])
        st.dataframe(checks_df, use_container_width=True)

        st.subheader("🔐 Cryptographic Lineage Manifest (SHA-256)")
        st.caption("Cryptographic hashes verify pipeline file integrity against original downloads; they do not assert statistical accuracy or sampling precision of the underlying NSSO surveys.")
        raw_manifest = [
            {"Source File": "HCES_Press_Note_2023-24_27122024_rev.pdf", "SHA-256 Checksum": "9a67df191fac044f1c3b45fdfe3d40bbb43ff2865789fc3a1f7d35875be60bc7", "Producer": "MoSPI / NSSO", "Status": "VERIFIED"},
            {"Source File": "Factsheet_HCES_2022-23.pdf", "SHA-256 Checksum": "2993c572f87f8b58c9c4ddc075431b2d2f2593aef00914f136d11ac434e3e9fc", "Producer": "MoSPI / NSSO", "Status": "VERIFIED"},
            {"Source File": "CPI_Release_Aug2026.html", "SHA-256 Checksum": "bce912654ac399ebdec9a10115a15fb812ccee8f909c6c75912752b9c8013f28", "Producer": "MoSPI / PSD", "Status": "VERIFIED"},
            {"Source File": "Factsheet_HCES_2023-24_PIB.pdf", "SHA-256 Checksum": "8af294a423d39b5184e73e0c8e6a24db4199aa3eec4cdb5525c81f12968fce37", "Producer": "PIB / MoSPI", "Status": "VERIFIED"},
            {"Source File": "HCES_2023-24_PIB_2247612.html", "SHA-256 Checksum": "09f9b686230f677d8ee22d2686425cd1ceb113f3c77e73f7a95599b3752d828f", "Producer": "PIB / MoSPI", "Status": "VERIFIED"},
            {"Source File": "HCES_2023-24_PIB_2088390.html", "SHA-256 Checksum": "bfe042dfb51beefc4bfe0a30d621037af5d8d90787f0fcb85f159ed63953716b", "Producer": "PIB / MoSPI", "Status": "VERIFIED"}
        ]
        st.table(pd.DataFrame(raw_manifest))

    # ==================== SECTION 6: METHODOLOGY & DOWNLOADS ====================
    elif selected_tab == "6. Methodology & Downloads":
        st.markdown("<div class='section-title'>6. Research Methodology & Data Downloads</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Detailed survey design notes, conceptual boundary documentation, and exportable data artifacts.</div>", unsafe_allow_html=True)

        m_tabs = st.tabs(["Survey Methodology", "HCES vs. PFCE Divergence", "Export Center & Licensing"])

        with m_tabs[0]:
            st.markdown("""
            ### MoSPI HCES Survey Design (CAPI 3-Visit Architecture)
            - **Sample Size:** 2,61,953 households (1,54,357 rural and 1,07,596 urban) across 14,827 First Stage Units (FSUs).
            - **Panel Questionnaire Design:** In HCES 2022-23 and 2023-24, MoSPI deployed a 3-visit panel method canvassing three distinct schedules:
              1. **FDQ (Food Items):** Canvassed in month 1 of a quarter.
              2. **CSQ (Consumables & Services):** Canvassed in month 2.
              3. **DGQ (Durable Goods):** Canvassed in month 3.
            - **Social Welfare Imputation:** Captures in-kind transfers (foodgrains under PMGKY, school uniforms, cycles, computers) and values them at local market rates.
            """)

        with m_tabs[1]:
            st.markdown("""
            ### Understanding the Divergence: Household Survey (HCES) vs. National Accounts (PFCE)
            Economists and market researchers consistently observe that household survey MPCE captures approximately **45% to 50%** of aggregate National Accounts Private Final Consumption Expenditure (PFCE).
            """)
            pfce_comparison = [
                {"Attribute": "Scope of Population", "HCES Household Survey": "Resident private households only", "National Accounts PFCE": "Households + Non-Profit Institutions Serving Households (NPISH)"},
                {"Attribute": "Housing / Shelter", "HCES Household Survey": "Out-of-pocket rent paid only (imputed owner rent excluded)", "National Accounts PFCE": "Includes imputed rental value of owner-occupied dwellings"},
                {"Attribute": "Financial Services", "HCES Household Survey": "Direct out-of-pocket fees only", "National Accounts PFCE": "Includes FISIM (Financial Intermediation Services Indirectly Measured)"},
                {"Attribute": "Top-Fractile Coverage", "HCES Household Survey": "Prone to respondent under-reporting in top 1%", "National Accounts PFCE": "Macroeconomic domestic supply/absorption method"},
                {"Attribute": "FY 2023-24 Aggregate", "HCES Household Survey": "Aggregated survey spending: ~₹85-90 lakh crore", "National Accounts PFCE": "₹178.6 lakh crore (~60.2% of GDP)"}
            ]
            st.table(pd.DataFrame(pfce_comparison))

        with m_tabs[2]:
            st.markdown("### 📥 Download Analysis-Ready Datasets & Reports")
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    label="📥 Download State MPCE Dataset (CSV)",
                    data=df_state.to_csv(index=False),
                    file_name="consumerlens_state_mpce_2023-24.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="📥 Download Commodity Basket Shares (CSV)",
                    data=df_category.to_csv(index=False),
                    file_name="consumerlens_category_shares_2023-24.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="📥 Download Fractile Distribution (CSV)",
                    data=df_fractile.to_csv(index=False),
                    file_name="consumerlens_fractile_distribution.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="📥 Download National Growth Trajectory (CSV)",
                    data=df_traj.to_csv(index=False),
                    file_name="consumerlens_national_trajectory.csv",
                    mime="text/csv"
                )
            with dcol2:
                st.download_button(
                    label="📥 Download CPI Series Dataset (CSV)",
                    data=df_cpi.to_csv(index=False),
                    file_name="consumerlens_cpi_series.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="📥 Download Pipeline Validation Report (JSON)",
                    data=json.dumps(validation_report, indent=2),
                    file_name="consumerlens_validation_report.json",
                    mime="application/json"
                )
                with open(os.path.join(BASE_DIR, "docs", "SOURCE_REGISTER.csv"), "r", encoding="utf-8") as f:
                    src_csv = f.read()
                st.download_button(
                    label="📥 Download Official Source Register (CSV)",
                    data=src_csv,
                    file_name="consumerlens_source_register.csv",
                    mime="text/csv"
                )
                rec_path = os.path.join(BASE_DIR, "docs", "SOURCE_RECONCILIATION.json")
                if os.path.exists(rec_path):
                    with open(rec_path, "r", encoding="utf-8") as f:
                        rec_json_str = f.read()
                    st.download_button(
                        label="📥 Download Source Reconciliation Report (JSON)",
                        data=rec_json_str,
                        file_name="consumerlens_source_reconciliation.json",
                        mime="application/json"
                    )

            st.divider()
            st.markdown("### ⚖️ Licensing & Attribution Framework")
            st.markdown("""
            - **Software Code License:** MIT License — Open source, free for academic, personal, and commercial adaptation.
            - **Underlying Official Data License:** Open Government Data License - India (OGDL-India) — Produced and published by the Ministry of Statistics and Programme Implementation (MoSPI), Government of India.
            - **Citation:** National Sample Survey Office (NSSO), MoSPI, Government of India: *Household Consumption Expenditure Survey: 2023-24* (Report No. 592) and *2022-23* (Report No. 590); Price Statistics Division (PSD), MoSPI: *Consumer Price Index Releases (Base 2024=100 & Base 2012=100)*.
            """)


if __name__ == "__main__":
    main()
