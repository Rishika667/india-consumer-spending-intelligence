"""
Automated unit tests for primary source reconciliation and regression gates.
Tests ensure:
1. Reconciler matches clean source tables against preserved raw documents.
2. Dataset observation corruption fails reconciliation and exits non-zero.
3. Missing raw primary documents produce UNRESOLVED status.
4. Schema consistency with app.py audit log rendering.
"""

import os
import json
import pytest
import pandas as pd
from scripts.reconcile_sources import run_reconciliation


def test_reconciliation_clean_run():
    """Verify that the clean baseline achieves 100% match rate across all benchmarks."""
    result = run_reconciliation()
    assert result["total_records_checked"] >= 40
    assert result["records_matched"] == result["total_records_checked"]
    assert result["records_mismatched"] == 0
    assert result["unresolved_records"] == 0
    assert result["match_rate_pct"] == 100.0
    assert len(result["reconciliation_checks"]) == result["total_records_checked"]

    # Verify check record schema expected by app.py
    first_check = result["reconciliation_checks"][0]
    required_keys = {"check_id", "metric", "dataset", "observed_value", "primary_source_doc", "table_ref", "status", "source_evidence"}
    assert required_keys.issubset(first_check.keys())


def test_reconciliation_detects_data_corruption(tmp_path):
    """Verify that tampering with a source CSV produces MISMATCH."""
    from scripts.reconcile_sources import SourceReconciliationEngine, SOURCES_DIR, RAW_DIR

    # Create temporary copies of sources
    temp_sources = tmp_path / "sources"
    temp_sources.mkdir()
    
    # Copy all source CSVs
    for f in os.listdir(SOURCES_DIR):
        if f.endswith(".csv"):
            src_file = os.path.join(SOURCES_DIR, f)
            dest_file = temp_sources / f
            dest_file.write_text(open(src_file, encoding="utf-8").read(), encoding="utf-8")

    # Corrupt one value in source_state_mpce_2023_24.csv (All-India Rural unimputed from 4122 to 9999)
    state_csv = temp_sources / "source_state_mpce_2023_24.csv"
    df_state = pd.read_csv(state_csv)
    mask = (df_state["state_name"] == "All-India") & (df_state["sector"] == "Rural")
    df_state.loc[mask, "mpce_unimputed"] = 9999.0
    df_state.to_csv(state_csv, index=False)

    reconciler = SourceReconciliationEngine(sources_dir=str(temp_sources), raw_dir=RAW_DIR, docs_dir=None)
    result = reconciler.run_reconciliation()

    assert result["records_mismatched"] > 0
    assert result["match_rate_pct"] < 100.0

    mismatches = [c for c in result["reconciliation_checks"] if c["status"] == "MISMATCH"]
    assert any("4122" in m["metric"] or "Rural MPCE" in m["metric"] for m in mismatches)


def test_reconciliation_handles_missing_raw_doc(tmp_path):
    """Verify that a missing primary raw document produces UNRESOLVED rather than silent pass."""
    from scripts.reconcile_sources import SourceReconciliationEngine, SOURCES_DIR

    # Create temporary empty raw dir
    temp_raw = tmp_path / "raw"
    temp_raw.mkdir()

    reconciler = SourceReconciliationEngine(sources_dir=SOURCES_DIR, raw_dir=str(temp_raw), docs_dir=None)
    result = reconciler.run_reconciliation()

    assert result["unresolved_records"] > 0
    unresolved = [c for c in result["reconciliation_checks"] if c["status"] == "UNRESOLVED"]
    assert len(unresolved) == result["total_records_checked"]

