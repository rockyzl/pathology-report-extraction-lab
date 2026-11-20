import json
from pathlib import Path

import numpy as np
import pytest

from prel import cohort, rules
from prel.grounding import ground_field, locate
from prel.metrics import cohen_kappa, e2e_matrix, macro_e2e, paired_bootstrap
from prel.schema import FIELDS, map_curated, map_histology, map_laterality, map_n, map_t, n_bucket

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (ROOT / "tests" / "fixtures" / "synthetic_report.txt").read_text()


# ---------- span grounding ----------
def test_locate_exact_and_whitespace_collapsed():
    text = "FINAL DIAGNOSIS:  Invasive ductal\ncarcinoma, grade 2."
    assert locate("Invasive ductal carcinoma", text) == (18, 43)
    s, e = locate("Invasive ductal carcinoma", text)
    assert text[s:e] == "Invasive ductal\ncarcinoma"
    assert locate("invasive ductal carcinoma", text) is None  # no case folding
    assert locate("Invasive duct carcinoma", text) is None  # no fuzzy match
    assert locate("", text) is None


def test_ground_field_rejects_fabricated_and_unsupported_quotes():
    text = "ESTROGEN RECEPTOR: POSITIVE. Margins free. 3 of 12 lymph nodes positive."
    ok = ground_field("er_status", "positive", ["ESTROGEN RECEPTOR: POSITIVE"], text)
    assert ok["status"] == "answered" and ok["spans"] == [[0, 27]]
    fab = ground_field("er_status", "positive", ["ER strongly positive"], text)
    assert fab["status"] == "rejected" and fab["reason"] == "quote_not_in_report" and fab["value"] is None
    nocue = ground_field("er_status", "positive", ["Margins free"], text)
    assert nocue["reason"] == "quote_lacks_field_cue"
    noquote = ground_field("er_status", "positive", [], text)
    assert noquote["reason"] == "no_quote"
    wrongnum = ground_field("ln_examined", 13, ["3 of 12 lymph nodes positive"], text)
    assert wrongnum["reason"] == "number_not_in_quote"
    assert ground_field("ln_examined", 12, ["3 of 12 lymph nodes positive"], text)["status"] == "answered"
    ns = ground_field("er_status", None, [], text)
    assert ns["status"] == "not_stated"


# ---------- normalization / mapping ----------
def test_tnm_mapping():
    assert map_t("T1c") == "T1" and map_t("T4b") == "T4" and map_t("TX") == "TX" and map_t(None) is None
    assert map_n("N0 (i-)") == "N0" and map_n("N0 (i+)") == "N0" and map_n("N1mi") == "N1"
    assert map_n("N3a") == "N3" and map_n("NX") == "NX" and map_n("[Not Available]") is None


def test_histology_and_laterality_mapping():
    assert map_histology("Infiltrating Ductal Carcinoma", None) == "ductal"
    assert map_histology("Mixed Histology (please specify)", "Infiltrating ductal and lobular carcinoma") == "mixed_ductal_lobular"
    assert map_histology("Other, specify", "Lobular/Ductal") == "mixed_ductal_lobular"
    assert map_histology("Mixed Histology (please specify)", "tubular and cribriform") == "other"
    assert map_histology("Metaplastic Carcinoma", None) == "other"
    assert map_laterality("Left Upper Outer Quadrant|Left") == "left"
    assert map_laterality("Right") == "right"
    assert map_laterality("Left|Right") is None


def test_map_curated_statuses():
    row = {"breast_carcinoma_estrogen_receptor_status": "Indeterminate",
           "breast_carcinoma_progesterone_receptor_status": "Negative",
           "lab_proc_her2_neu_immunohistochemistry_receptor_status": "Equivocal",
           "her2_immunohistochemistry_level_result": "2+",
           "lab_procedure_her2_neu_in_situ_hybrid_outcome_type": "Positive",
           "lymph_node_examined_count": "12", "number_of_lymphnodes_positive_by_he": "0",
           "margin_status": "Close"}
    m = map_curated(row)
    assert m["er_status"] is None  # Indeterminate excluded from evaluation
    assert m["pr_status"] == "negative" and m["her2_ihc_status"] == "equivocal" and m["her2_ihc_score"] == "2+"
    assert m["her2_ish_status"] == "amplified" and m["ln_examined"] == 12 and m["ln_positive"] == 0
    assert m["margin_status"] == "close" and m["histologic_type"] is None
    assert n_bucket(0) == "N0" and n_bucket(3) == "N1" and n_bucket(4) == "N2" and n_bucket(10) == "N3"


# ---------- split leakage ----------
def test_split_is_patient_level_deterministic_and_disjoint():
    pids = [f"TCGA-XX-{i:04d}" for i in range(400)]
    a = cohort.assign_split(pids + pids[:50])  # duplicates must not create a second assignment
    b = cohort.assign_split(list(reversed(pids)))
    assert a == b and len(a) == 400
    assert sum(v == "test" for v in a.values()) == 100


def test_saved_membership_matches_rule():
    mpath = ROOT / "data" / "membership.json"
    if not mpath.exists():
        pytest.skip("membership not built")
    m = json.loads(mpath.read_text())
    dev, test = set(m["dev"]), set(m["test"])
    assert not dev & test
    assert set(m["llm_dev_sample"]) <= dev
    re_split = cohort.assign_split(sorted(dev | test))
    assert {p for p, s in re_split.items() if s == "test"} == test
    assert m["llm_dev_sample"] == cohort.llm_dev_sample(sorted(dev))


# ---------- metrics ----------
def test_cohen_kappa_toy():
    assert cohen_kappa(list("aabb"), list("aabb")) == pytest.approx(1.0)
    # po = 0.5, pe = 0.5 -> 0
    assert cohen_kappa(list("aabb"), list("abab")) == pytest.approx(0.0)
    # classic 2x2: a=20,b=5,c=10,d=15 -> po=.7, pe=.5 -> .4
    x = ["y"] * 25 + ["n"] * 25
    y = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    assert cohen_kappa(x, y) == pytest.approx(0.4)
    assert cohen_kappa([], []) is None
    assert cohen_kappa(["a", "a"], ["a", "a"]) is None  # chance agreement 1 -> undefined


def test_e2e_matrix_counts_abstention_as_disagreement():
    gold = {"p1": {f: None for f in FIELDS}, "p2": {f: None for f in FIELDS}}
    gold["p1"]["er_status"] = "positive"
    gold["p2"]["er_status"] = "negative"
    rec = lambda v, s: {"value": v, "status": s}
    pred = {p: {f: rec(None, "not_stated") for f in FIELDS} for p in gold}
    pred["p1"]["er_status"] = rec("positive", "answered")
    pred["p2"]["er_status"] = rec(None, "rejected")
    m = e2e_matrix(["p1", "p2"], gold, pred, ["er_status", "pr_status"])
    assert m[0, 0] == 1 and m[1, 0] == 0 and np.isnan(m[:, 1]).all()
    assert macro_e2e(m) == pytest.approx(0.5)


def test_paired_bootstrap_toy():
    rng = np.random.default_rng(0)
    a = (rng.random((300, 3)) < 0.8).astype(float)
    b = (rng.random((300, 3)) < 0.5).astype(float)
    r = paired_bootstrap(a, b, n_boot=500, seed=1)
    assert r["ci_low"] < r["diff"] < r["ci_high"] and r["ci_low"] > 0.15
    same = paired_bootstrap(a, a, n_boot=200, seed=1)
    assert same["diff"] == 0 and same["ci_low"] == 0 and same["ci_high"] == 0
    assert paired_bootstrap(a, b, n_boot=200, seed=7) == paired_bootstrap(a, b, n_boot=200, seed=7)


# ---------- rules baseline on fixture text ----------
def test_rules_on_synthetic_fixture():
    out = rules.extract(FIXTURE)
    v = {f: r["value"] for f, r in out.items()}
    assert v["er_status"] == "positive" and v["pr_status"] == "negative"
    assert v["her2_ihc_status"] == "equivocal" and v["her2_ihc_score"] == "2+"
    assert v["her2_ish_status"] == "not_amplified"
    assert v["histologic_type"] == "ductal"
    assert v["pathologic_t"] == "T2" and v["pathologic_n"] == "N1"
    assert v["laterality"] == "left" and v["margin_status"] == "negative"
    assert v["ln_positive"] == 2 and v["ln_examined"] == 14
    for f, r in out.items():  # every answered value is grounded at its offsets
        if r["status"] == "answered":
            for q, (s, e) in zip(r["quotes"], r["spans"]):
                assert " ".join(FIXTURE[s:e].split()) == " ".join(q.split())


def test_rules_abstain_on_empty_and_ambiguous():
    out = rules.extract("Specimen received. No diagnostic text. HER2/NEU: zero or 1+.")
    assert all(r["status"] != "answered" for f, r in out.items() if f != "her2_ihc_status")
    assert out["her2_ihc_score"]["status"] == "not_stated"
