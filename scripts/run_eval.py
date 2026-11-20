"""Prespecified evaluation.

  python scripts/run_eval.py dev     # dev tables (rules on all dev; LLM on the cached 80-patient dev sample)
  python scripts/run_eval.py freeze  # record the commit used for the test run (tree must be clean)
  python scripts/run_eval.py test    # one-shot held-out test run (requires freeze.json at HEAD)
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from prel import analysis, evaluate as E, llm
from prel.metrics import e2e_matrix, field_bootstrap, paired_bootstrap
from prel.schema import CAT_FIELDS, FIELDS

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
MODELS = ["gpt-4.1", "gpt-4o"]
P = json.loads((ROOT / "protocol.json").read_text())
B, SEED = 2000, 20261120


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def jdump(obj, path):
    path.write_text(json.dumps(obj, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")


def save_extractions(name, pids, pred):
    d = RES / "extractions"
    d.mkdir(exist_ok=True)
    with open(d / f"{name}.jsonl", "w") as fh:
        for p in pids:
            fh.write(json.dumps({"patient_id": p, **pred[p]}, ensure_ascii=False) + "\n")


def dev():
    rep, gold, mem, texts = E.load_all()
    out = {"phase": "dev", "rules_all_dev": E.tables(mem["dev"], gold, E.run_rules(mem["dev"], texts))}
    s = mem["llm_dev_sample"]
    cache = llm.load_cache()
    if all(llm.cache_key("gpt-4.1", p, texts[p]) in cache for p in s):
        pred, recs = E.run_llm("gpt-4.1", s, texts)
        out["llm_dev_sample"] = {"gpt-4.1": E.tables(s, gold, pred), "rules": E.tables(s, gold, E.run_rules(s, texts)),
                                 "cost": analysis.cost_summary(recs), "prompt_version": llm.PROMPT_VERSION}
    jdump(out, RES / "dev_results.json")
    print(E.fmt(out["rules_all_dev"]))


def freeze():
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files modified; commit before freezing")
    jdump({"frozen_commit": git("rev-parse", "HEAD"), "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "prompt_version": llm.PROMPT_VERSION, "protocol_version": P["protocol_version"],
           "note": "test-set extraction and evaluation run once against this commit"}, RES / "freeze.json")
    print(json.loads((RES / "freeze.json").read_text()))


def test():
    fz = json.loads((RES / "freeze.json").read_text())
    code_diff = git("diff", "--stat", fz["frozen_commit"], "HEAD", "--", "src", "protocol.json")
    if code_diff:
        sys.exit(f"src/ or protocol.json changed since freeze:\n{code_diff}")
    rep, gold, mem, texts = E.load_all()
    pids = mem["test"]
    preds, recs = {"rules": E.run_rules(pids, texts)}, {}
    for m in MODELS:
        preds[m], recs[m] = E.run_llm(m, pids, texts, budget_usd=10.0)
    for m, pr in preds.items():
        save_extractions(f"test_{m}", pids, pr)
    out = {"phase": "test", "frozen_commit": fz["frozen_commit"], "n_test": len(pids), "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "tables": {m: E.tables(pids, gold, pr) for m, pr in preds.items()}}
    mats = {m: e2e_matrix(pids, gold, pr, CAT_FIELDS) for m, pr in preds.items()}
    mats_all = {m: e2e_matrix(pids, gold, pr, list(FIELDS)) for m, pr in preds.items()}
    prim = paired_bootstrap(mats["gpt-4.1"], mats["rules"], n_boot=B, seed=SEED)
    lo, hi = prim["ci_low"], prim["ci_high"]
    prim["decision"] = "gpt-4.1 higher agreement" if lo > 0 else ("gpt-4.1 lower agreement" if hi < 0 else "inconclusive")
    out["primary"] = {"estimand": P["primary_comparison"]["estimand"], **prim}
    out["secondary"] = {
        "gpt-4o_minus_rules_cat": paired_bootstrap(mats["gpt-4o"], mats["rules"], n_boot=B, seed=SEED),
        "gpt-4.1_minus_gpt-4o_cat": paired_bootstrap(mats["gpt-4.1"], mats["gpt-4o"], n_boot=B, seed=SEED),
        "gpt-4.1_minus_rules_all12": paired_bootstrap(mats_all["gpt-4.1"], mats_all["rules"], n_boot=B, seed=SEED),
        "gpt-4o_minus_rules_all12": paired_bootstrap(mats_all["gpt-4o"], mats_all["rules"], n_boot=B, seed=SEED),
        "per_field_gpt-4.1_minus_rules": {f: field_bootstrap(mats_all["gpt-4.1"], mats_all["rules"], j, n_boot=B, seed=SEED) for j, f in enumerate(FIELDS)},
        "per_field_gpt-4o_minus_rules": {f: field_bootstrap(mats_all["gpt-4o"], mats_all["rules"], j, n_boot=B, seed=SEED) for j, f in enumerate(FIELDS)},
    }
    out["consistency"] = {m: analysis.consistency(pids, pr) for m, pr in preds.items()}
    out["consistency"]["curated"] = analysis.consistency(pids, gold, is_gold=True)
    out["cost"] = {m: analysis.cost_summary(r) for m, r in recs.items()}
    # grounding / rejection summary across all fields
    out["grounding"] = {}
    for m, pr in preds.items():
        cells = [pr[p][f] for p in pids for f in FIELDS]
        claimed = [c for c in cells if c["status"] != "not_stated"]
        rej = [c for c in cells if c["status"] == "rejected"]
        reasons = {}
        for c in rej:
            reasons[c["reason"]] = reasons.get(c["reason"], 0) + 1
        out["grounding"][m] = {"cells": len(cells), "claimed_values": len(claimed), "rejected": len(rej),
                               "rejection_rate_of_claims": len(rej) / len(claimed) if claimed else None,
                               "not_stated": sum(c["status"] == "not_stated" for c in cells), "reasons": reasons}
    # error-source tags over all disagreements / abstentions vs curated
    tags = {m: {} for m in preds}
    for m, pr in preds.items():
        for p in pids:
            for f in FIELDS:
                g = gold[p][f]
                if g is None:
                    continue
                r = pr[p][f]
                if r["status"] == "answered" and str(r["value"]) == str(g):
                    continue
                kind = "wrong_value" if r["status"] == "answered" else "abstained"
                for t in analysis.error_tags(texts[p], f, g, {k: preds[k][p][f] for k in preds}) or ["untagged"]:
                    tags[m].setdefault(kind, {}).setdefault(t, 0)
                    tags[m][kind][t] += 1
    out["error_tags"] = tags
    rows = analysis.adjudication_sample(pids, gold, preds, texts, n=30, seed=SEED)
    analysis.write_adjudication(rows, RES, MODELS)
    out["adjudication_sample"] = {"n": len(rows), "files": ["results/adjudication_sample.md", "results/adjudication_sample.csv"],
                                  "by_field": {f: sum(r["field"] == f for r in rows) for f in FIELDS}, "status": "UNREVIEWED"}
    jdump(out, RES / "test_results.json")
    for m in preds:
        print(m); print(E.fmt(out["tables"][m]))
    print("PRIMARY", json.dumps(out["primary"], indent=1))


if __name__ == "__main__":
    {"dev": dev, "freeze": freeze, "test": test}[sys.argv[1]]()
