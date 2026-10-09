"""
Automated unit tests for the Data Quality Engine and Composite Quality Scoring.
"""

import pytest
import pandas as pd
from src.quality_engine import DataQualityEngine
from src.pipeline import (
    build_state_mpce_dataset,
    build_category_shares_dataset,
    build_fractile_distribution_dataset,
    build_cpi_series_dataset,
    build_macro_pfce_dataset
)


def test_quality_engine_clean_data_audit():
    engine = DataQualityEngine()
    df_state = build_state_mpce_dataset()
    df_category = build_category_shares_dataset()
    df_fractile = build_fractile_distribution_dataset()
    df_cpi = build_cpi_series_dataset()
    df_pfce = build_macro_pfce_dataset()

    report = engine.run_audit(
        df_state=df_state,
        df_category=df_category,
        df_fractile=df_fractile,
        df_cpi=df_cpi,
        df_pfce=df_pfce
    )

    assert report["total_evaluated"] >= 25
    assert report["failed"] == 0
    assert report["composite_score"] == 100.0
    for dim, meta in report["dimension_breakdown"].items():
        assert meta["score_pct"] == 100.0


def test_quality_engine_detects_synthetic_violations():
    engine = DataQualityEngine()
    df_state = build_state_mpce_dataset()
    df_category = build_category_shares_dataset()
    df_fractile = build_fractile_distribution_dataset()
    df_cpi = build_cpi_series_dataset()
    df_pfce = build_macro_pfce_dataset()

    # Inject negative MPCE (Validity violation)
    corrupted_state = df_state.copy()
    corrupted_state.loc[0, "mpce_unimputed"] = -500.0

    # Inject invalid share (> 100)
    corrupted_cat = df_category.copy()
    corrupted_cat.loc[0, "share_pct"] = 150.0

    report = engine.run_audit(
        df_state=corrupted_state,
        df_category=corrupted_cat,
        df_fractile=df_fractile,
        df_cpi=df_cpi,
        df_pfce=df_pfce
    )

    assert report["failed"] >= 2
    assert report["composite_score"] < 100.0
    failed_checks = [c["check_id"] for c in report["checks"] if c["status"] == "FAIL"]
    assert "V01" in failed_checks or "V02" in failed_checks
