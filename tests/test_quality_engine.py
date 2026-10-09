"""
Automated unit tests for the Data Quality Engine and Composite Quality Scoring.
Verifies the exact 28-rule audit suite, corruption detection, and availability tracking.
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

    assert report["total_evaluated"] == 28
    assert report["expected_total_checks"] == 28
    assert report["failed"] == 0
    assert report["composite_score"] == 100.0
    for dim, meta in report["dimension_breakdown"].items():
        assert meta["score_pct"] == 100.0
    
    # Verify presence of data availability metrics
    assert "data_availability_summary" in report
    avail = report["data_availability_summary"]
    assert "hces_2022_23_state_coverage" in avail
    assert "hces_2023_24_unimputed_coverage" in avail


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


def test_quality_engine_p02_line_endings_robustness():
    """Verify that check P02 succeeds regardless of LF or CRLF git checkout line endings."""
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
    p02_checks = [c for c in report["checks"] if c["check_id"] == "P02"]
    assert len(p02_checks) == 1
    assert p02_checks[0]["status"] == "PASS"
    assert "6/6 source files verified" in p02_checks[0]["actual_value"]


def test_reconciliation_summary_integration_success():
    """Verify that quality engine integrates real source reconciliation summary from disk."""
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
    rec_sum = report.get("source_reconciliation_summary", {})
    assert rec_sum["status"] == "PASSED"
    assert rec_sum["records_checked"] >= 42
    assert rec_sum["records_matched"] == rec_sum["records_checked"]
    assert rec_sum["records_mismatched"] == 0
    assert rec_sum["unresolved_records"] == 0
    assert rec_sum["match_rate_pct"] == 100.0


def test_reconciliation_summary_integration_missing_and_malformed(tmp_path, monkeypatch):
    """Verify that quality engine handles missing and malformed reconciliation reports without silent false passes."""
    import src.quality_engine as qe
    engine = DataQualityEngine()
    df_state = build_state_mpce_dataset()
    df_category = build_category_shares_dataset()
    df_fractile = build_fractile_distribution_dataset()
    df_cpi = build_cpi_series_dataset()
    df_pfce = build_macro_pfce_dataset()

    # Case 1: Missing file
    fake_docs_missing = tmp_path / "docs_missing"
    fake_docs_missing.mkdir()
    monkeypatch.setattr(qe, "DOCS_DIR", str(fake_docs_missing))

    report_missing = engine.run_audit(
        df_state=df_state,
        df_category=df_category,
        df_fractile=df_fractile,
        df_cpi=df_cpi,
        df_pfce=df_pfce
    )
    rec_missing = report_missing.get("source_reconciliation_summary", {})
    assert rec_missing["status"] == "NOT_RUN"
    assert rec_missing["records_checked"] == 0
    assert "not found" in rec_missing["message"].lower()

    # Case 2: Malformed file
    fake_docs_malformed = tmp_path / "docs_malformed"
    fake_docs_malformed.mkdir()
    (fake_docs_malformed / "SOURCE_RECONCILIATION.json").write_text("{invalid json", encoding="utf-8")
    monkeypatch.setattr(qe, "DOCS_DIR", str(fake_docs_malformed))

    report_malformed = engine.run_audit(
        df_state=df_state,
        df_category=df_category,
        df_fractile=df_fractile,
        df_cpi=df_cpi,
        df_pfce=df_pfce
    )
    rec_malformed = report_malformed.get("source_reconciliation_summary", {})
    assert rec_malformed["status"] == "MALFORMED"
    assert rec_malformed["records_checked"] == 0
    assert "failed to parse" in rec_malformed["message"].lower()


