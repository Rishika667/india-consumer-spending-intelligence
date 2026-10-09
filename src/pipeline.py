"""
ConsumerLens India — Research Data Ingestion & Transformation Pipeline
Processes official MoSPI HCES and CPI datasets into normalized analytical datasets.
Zero-cost, offline-reproducible, and audit-ready.
Ingests from documented structured source files in data/sources/.
"""

import os
import sys
import json
import hashlib
from typing import Dict, List, Tuple, Any
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
SOURCES_DIR = os.path.join(BASE_DIR, "data", "sources")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def ensure_directories():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)


def build_state_mpce_dataset() -> pd.DataFrame:
    """
    Builds the state-level MPCE dataset by ingesting documented source tables:
    - 2022-23: data/sources/source_state_mpce_2022_23.csv (Statement 8 & 18 of Factsheet Report 590)
    - 2023-24: data/sources/source_state_mpce_2023_24.csv (PIB PRID 2247612 & Report 592 Press Note)
    Maintains explicit NaN / missing status where an official figure is unpublished.
    """
    f_22 = os.path.join(SOURCES_DIR, "source_state_mpce_2022_23.csv")
    f_23 = os.path.join(SOURCES_DIR, "source_state_mpce_2023_24.csv")

    df_22 = pd.read_csv(f_22)
    df_23 = pd.read_csv(f_23)

    combined = pd.concat([df_22, df_23], ignore_index=True)
    # Ensure correct data types
    combined["mpce_unimputed"] = pd.to_numeric(combined["mpce_unimputed"], errors="coerce")
    combined["mpce_imputed"] = pd.to_numeric(combined["mpce_imputed"], errors="coerce")
    combined["welfare_delta"] = pd.to_numeric(combined["welfare_delta"], errors="coerce")

    return combined


def build_category_shares_dataset() -> pd.DataFrame:
    """
    Builds the commodity group shares dataset by ingesting data/sources/source_category_shares.csv:
    - 2022-23: Statement 5 (unimputed) & Statement 15 (imputed)
    - 2023-24: Press Note Figures 4, 5, 6, 7 (unimputed)
    Note: MoSPI did NOT publish commodity category shares with imputation for 2023-24.
    """
    f_cat = os.path.join(SOURCES_DIR, "source_category_shares.csv")
    df_cat = pd.read_csv(f_cat)
    df_cat["share_pct"] = pd.to_numeric(df_cat["share_pct"], errors="coerce")
    return df_cat


def build_fractile_distribution_dataset() -> pd.DataFrame:
    """
    Builds the fractile classes dataset by ingesting data/sources/source_fractile_distribution.csv:
    - 2022-23: Statement 4 of Report 590 Factsheet
    - 2023-24: Figure 1 & Report 592 Press Note
    """
    f_frac = os.path.join(SOURCES_DIR, "source_fractile_distribution.csv")
    df_frac = pd.read_csv(f_frac)
    df_frac["avg_mpce"] = pd.to_numeric(df_frac["avg_mpce"], errors="coerce")
    return df_frac


def build_cpi_series_dataset() -> pd.DataFrame:
    """
    Builds the CPI dataset combining:
    1. Revised CPI (Base 2024=100) monthly series (Jan 2025 – Aug 2026, Table 10 of August 2026 release)
    2. Discontinued Historical CPI (Base 2012=100) benchmark snapshots for HCES survey periods
    """
    f_24 = os.path.join(SOURCES_DIR, "source_cpi_monthly_2024_base.csv")
    f_12 = os.path.join(SOURCES_DIR, "source_cpi_historical_2012_base_snapshot.csv")

    df_24 = pd.read_csv(f_24)
    df_12 = pd.read_csv(f_12)

    combined = pd.concat([df_24, df_12], ignore_index=True)
    combined["cpi_general"] = pd.to_numeric(combined["cpi_general"], errors="coerce")
    combined["cpi_food_cfpi"] = pd.to_numeric(combined["cpi_food_cfpi"], errors="coerce")
    combined["inflation_general_pct"] = pd.to_numeric(combined["inflation_general_pct"], errors="coerce")
    combined["inflation_food_pct"] = pd.to_numeric(combined["inflation_food_pct"], errors="coerce")

    return combined


def build_macro_pfce_dataset() -> pd.DataFrame:
    """
    Builds the National Accounts Private Final Consumption Expenditure (PFCE) benchmark dataset.
    Ingested from data/sources/source_macro_pfce.csv.
    Used exclusively for methodological comparison (HCES vs PFCE divergence).
    """
    f_pfce = os.path.join(SOURCES_DIR, "source_macro_pfce.csv")
    df_pfce = pd.read_csv(f_pfce)
    df_pfce["pfce_current_inr_cr"] = pd.to_numeric(df_pfce["pfce_current_inr_cr"], errors="coerce")
    df_pfce["pfce_constant_inr_cr"] = pd.to_numeric(df_pfce["pfce_constant_inr_cr"], errors="coerce")
    df_pfce["share_of_gdp_pct"] = pd.to_numeric(df_pfce["share_of_gdp_pct"], errors="coerce")
    return df_pfce


def run_pipeline() -> Dict[str, Any]:
    """
    Executes the ingestion, transformation, and validation sequence.
    """
    print("[1/5] Initializing directories...")
    ensure_directories()

    print("[2/5] Building normalized analytical datasets from structured sources...")
    df_state = build_state_mpce_dataset()
    df_category = build_category_shares_dataset()
    df_fractile = build_fractile_distribution_dataset()
    df_cpi = build_cpi_series_dataset()
    df_pfce = build_macro_pfce_dataset()

    print("[3/5] Saving analytical outputs to data/processed/...")
    df_state.to_csv(os.path.join(PROCESSED_DIR, "state_mpce.csv"), index=False)
    df_category.to_csv(os.path.join(PROCESSED_DIR, "category_shares.csv"), index=False)
    df_fractile.to_csv(os.path.join(PROCESSED_DIR, "fractile_distribution.csv"), index=False)
    df_cpi.to_csv(os.path.join(PROCESSED_DIR, "cpi_series.csv"), index=False)
    df_pfce.to_csv(os.path.join(PROCESSED_DIR, "macro_pfce.csv"), index=False)

    print("[4/5] Executing Data Quality Engine...")
    from src.quality_engine import DataQualityEngine
    engine = DataQualityEngine()
    audit_report = engine.run_audit(
        df_state=df_state,
        df_category=df_category,
        df_fractile=df_fractile,
        df_cpi=df_cpi,
        df_pfce=df_pfce
    )

    report_path = os.path.join(DOCS_DIR, "VALIDATION_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=2)

    print(f"[5/5] Pipeline complete. Composite Quality Score: {audit_report['composite_score']:.2f}% ({audit_report['passed']}/{audit_report['total_evaluated']} checks passed)")
    return audit_report


if __name__ == "__main__":
    run_pipeline()
