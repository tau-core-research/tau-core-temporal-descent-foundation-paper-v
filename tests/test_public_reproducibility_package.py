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
        "data/derived/future_orientation_ledger.json",
        "arxiv_submission_source.zip",
    ]:
        assert (ROOT / rel).exists(), rel

def test_claim_boundaries_and_markers():
    tex = (ROOT / "paperV_submission_source/main.tex").read_text()
    assert "Temporal Descent from an Atemporal Morphological Body" in tex
    assert "Order-only no-go" in tex
    assert "Global synchronization criterion" in tex
    assert "Pathwise VEP clock" in tex
    assert "Localized complex-phase clock carrier" in tex
    assert "Future-orientation sign no-go" in tex
    assert "Conditional common clock--flow packet and two-sign no-go" in tex
    assert "Diagonal-orientation descent" in tex
    assert "Contact cotangent completeness, CTC-P1" in tex
    assert "Temporal MVP selection law" in tex
    assert "present seed scalar cannot be renamed" in tex
    assert "CTC ownership in the temporal MVP" in tex
    assert "observed Tau signal" not in tex

def test_ledger():
    data = json.loads((ROOT / "data/derived/temporal_descent_ledger.json").read_text())
    assert data["proved"]["order_only_duration_selection"] is False
    assert data["proved"]["positive_path_form_defines_observer_clock"] is True
    assert "global_and_singular_relativistic_limit" in data["open"]

def test_future_orientation_ledger():
    data = json.loads((ROOT / "data/derived/future_orientation_ledger.json").read_text())
    assert data["proved"]["phase_current_nonzero_timelike"] is True
    assert data["proved"]["normalized_unit_clock_covector_without_gain"] is True
    assert data["proved"]["current_parent_selects_one_frequency_sign"] is False
    assert data["proved"]["conditional_common_clock_flow_packet_exists"] is True
    assert data["proved"]["current_seed_scalar_supplies_causal_sign_line"] is False
    assert data["proved"]["diagonal_global_Z2_is_clock_terminal_null"] is True
    assert data["proved"]["ctc_p1_closes_local_handoff_conditionally"] is True
    assert data["proved"]["current_reduct_entails_ctc_p1"] is False
    assert data["temporal_mvp_selection"] == "adopts_CTC_P1_as_the_single_enriched_parent_selection_law"
    assert data["neutral_tau_over_gr_prediction"] == 0

def test_arxiv_archive_is_source_only():
    with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip") as archive:
        names = archive.namelist()
    assert "main.tex" in names
    assert "figures/fig_temporal_descent_spine.pdf" in names
    assert "main.pdf" not in names
