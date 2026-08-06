import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_files_exist():
    for rel in [
        "paperV_submission_source/main.tex",
        "paperV_submission_source/main.pdf",
        "figures/fig_temporal_descent_spine.pdf",
        "figures/fig_clock_diamond.pdf",
        "data/derived/temporal_descent_ledger.json",
        "arxiv_submission_source.zip",
    ]:
        assert (ROOT / rel).exists(), rel

def test_claim_boundaries_and_markers():
    tex = (ROOT / "paperV_submission_source/main.tex").read_text()
    assert "Temporal Descent from an Atemporal Morphological Body" in tex
    assert "Order-only no-go" in tex
    assert "Exact-clock criterion" in tex
    assert "Physical source selection remains open" in tex or "physical source selection remains open" in tex
    assert "observed Tau signal" not in tex

def test_ledger():
    data = json.loads((ROOT / "data/derived/temporal_descent_ledger.json").read_text())
    assert data["proved"]["order_only_duration_selection"] is False
    assert data["proved"]["positive_exact_edge_form_defines_clock"] is True
    assert "standard_relativistic_limit" in data["open"]

def test_arxiv_archive_is_source_only():
    with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip") as archive:
        names = archive.namelist()
    assert "main.tex" in names
    assert "figures/fig_temporal_descent_spine.pdf" in names
    assert "main.pdf" not in names
