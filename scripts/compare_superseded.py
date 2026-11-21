"""Compare the OpenAI API replication (results/) with the superseded v1.0 run (results/superseded_azure/).

Writes results/replication_vs_superseded.json. Descriptive only; no new hypothesis test.
"""
import csv
import json
from pathlib import Path

from prel.schema import CAT_FIELDS, FIELDS

ROOT = Path(__file__).resolve().parents[1]
NEW = json.loads((ROOT / "results/test_results.json").read_text())
OLD = json.loads((ROOT / "results/superseded_azure/test_results.json").read_text())
MODELS = ["gpt-4.1", "gpt-4o"]


def load_ext(path):
    return {r["patient_id"]: r for r in map(json.loads, path.read_text().splitlines())}


out = {"label": "descriptive comparison: OpenAI API replication vs superseded provisional-Azure v1.0 run (same snapshots, prompt, schema, rules, analysis)"}
keys = ["diff", "ci_low", "ci_high", "a", "b", "decision"]
out["primary"] = {"replication": {k: NEW["primary"][k] for k in keys}, "superseded": {k: OLD["primary"][k] for k in keys}}
out["secondary_gpt41_minus_gpt4o"] = {"replication": NEW["secondary"]["gpt-4.1_minus_gpt-4o_cat"], "superseded": OLD["secondary"]["gpt-4.1_minus_gpt-4o_cat"]}
out["macro_e2e"] = {m: {"replication": {"categorical10": NEW["tables"][m]["macro_e2e_categorical"], "all12": NEW["tables"][m]["macro_e2e_all"]},
                        "superseded": {"categorical10": OLD["tables"][m]["macro_e2e_categorical"], "all12": OLD["tables"][m]["macro_e2e_all"]}}
                    for m in ["rules"] + MODELS}
out["grounding"] = {m: {"replication": {k: NEW["grounding"][m][k] for k in ("claimed_values", "rejected", "rejection_rate_of_claims", "not_stated")},
                        "superseded": {k: OLD["grounding"][m][k] for k in ("claimed_values", "rejected", "rejection_rate_of_claims", "not_stated")}}
                    for m in MODELS}
out["per_field_e2e"] = {m: {f: {"replication": NEW["tables"][m]["per_field"][f]["agreement_e2e"],
                                "superseded": OLD["tables"][m]["per_field"][f]["agreement_e2e"]} for f in FIELDS} for m in MODELS}
# cell-level identity of grounded outputs (status + value) between runs
out["cell_identity"] = {}
for m in MODELS:
    new = load_ext(ROOT / f"results/extractions/test_{m}.jsonl")
    old = load_ext(ROOT / f"results/extractions/superseded_azure/test_{m}.jsonl")
    n = same = same_cat = n_cat = 0
    per = {}
    for p in new:
        for f in FIELDS:
            a, b = new[p][f], old[p][f]
            eq = a["status"] == b["status"] and str(a["value"]) == str(b["value"])
            n += 1
            same += eq
            per.setdefault(f, [0, 0])
            per[f][0] += eq
            per[f][1] += 1
            if f in CAT_FIELDS:
                n_cat += 1
                same_cat += eq
    out["cell_identity"][m] = {"cells": n, "identical": same, "rate": same / n, "categorical_rate": same_cat / n_cat,
                               "per_field_rate": {f: v[0] / v[1] for f, v in per.items()}}
# rules are deterministic: must be identical
rn = load_ext(ROOT / "results/extractions/test_rules.jsonl")
ro = load_ext(ROOT / "results/extractions/superseded_azure/test_rules.jsonl")
out["rules_identical"] = all(rn[p][f]["value"] == ro[p][f]["value"] and rn[p][f]["status"] == ro[p][f]["status"] for p in rn for f in FIELDS)
# adjudication sample item changes (same selection rule)
rd = lambda path: [(r["patient_id"], r["field"]) for r in csv.DictReader(open(path))]
a_new, a_old = rd(ROOT / "results/adjudication_sample.csv"), rd(ROOT / "results/superseded_azure/adjudication_sample.csv")
out["adjudication_sample"] = {"n_new": len(a_new), "n_old": len(a_old), "kept": sorted(set(a_new) & set(a_old)),
                              "added": [x for x in a_new if x not in a_old], "dropped": [x for x in a_old if x not in a_new],
                              "same_order": a_new == a_old}
d = out["primary"]
both_higher = d["replication"]["ci_low"] > 0 and d["superseded"]["ci_low"] > 0
out["conclusion"] = {"same_primary_decision": d["replication"]["decision"] == d["superseded"]["decision"],
                     "primary_diff_change": d["replication"]["diff"] - d["superseded"]["diff"],
                     "replication_point_inside_superseded_ci": d["superseded"]["ci_low"] <= d["replication"]["diff"] <= d["superseded"]["ci_high"],
                     "both_ci_above_zero": both_higher}
(ROOT / "results/replication_vs_superseded.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ("primary", "conclusion", "rules_identical")}, indent=1))
print({m: (round(v["rate"], 3), round(v["categorical_rate"], 3)) for m, v in out["cell_identity"].items()})
print("adjudication kept", len(out["adjudication_sample"]["kept"]), "added", out["adjudication_sample"]["added"], "dropped", out["adjudication_sample"]["dropped"])
