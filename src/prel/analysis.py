"""Consistency checks, cost summary, error-source tags and the adjudication sample."""
from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import numpy as np

from .schema import FIELDS, n_bucket

HER2_SCORE_STATUS = {"0": "negative", "1+": "negative", "2+": "equivocal", "3+": "positive"}


def _val(rec):
    return rec["value"] if rec["status"] == "answered" else None


def consistency(pids, pred_or_gold, is_gold=False) -> dict:
    get = (lambda p, f: pred_or_gold[p][f]) if is_gold else (lambda p, f: _val(pred_or_gold[p][f]))
    out = {}
    pairs = [(get(p, "ln_positive"), get(p, "ln_examined")) for p in pids]
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    out["positive_le_examined"] = {"n_both": len(pairs), "violations": sum(int(a) > int(b) for a, b in pairs)}
    pn = [(get(p, "pathologic_n"), get(p, "ln_positive")) for p in pids]
    pn = [(n, c) for n, c in pn if n is not None and c is not None and n != "NX"]
    out["pn_vs_positive_count"] = {"n_both": len(pn), "violations": sum(n != n_bucket(int(c)) for n, c in pn)}
    hs = [(get(p, "her2_ihc_score"), get(p, "her2_ihc_status")) for p in pids]
    hs = [(s, st) for s, st in hs if s is not None and st is not None]
    out["her2_score_vs_status"] = {"n_both": len(hs), "violations": sum(HER2_SCORE_STATUS[str(s)] != st for s, st in hs)}
    for v in out.values():
        v["rate"] = v["violations"] / v["n_both"] if v["n_both"] else None
    return out


def cost_summary(recs: list[dict]) -> dict:
    def stats(xs):
        a = np.asarray(xs, dtype=float)
        return {"mean": float(a.mean()), "median": float(np.median(a)), "p95": float(np.percentile(a, 95)), "total": float(a.sum())}
    return {"n_reports": len(recs), "input_tokens": stats([r["input_tokens"] for r in recs]),
            "output_tokens": stats([r["output_tokens"] for r in recs]), "seconds": stats([r["seconds"] for r in recs]),
            "cost_usd": stats([r["cost_usd"] for r in recs]),
            "finish_not_stop": sum(r["finish_reason"] != "stop" for r in recs),
            "deployment_models": sorted({r["deployment_model"] for r in recs})}


_OCR = re.compile(r"[^\x00-\x7f]|\bp[TN]\s?[OoIl]\b|\b[pP]T[Il][a-d]?\b|\d[Oo]\b|\b[Oo]\d")


def error_tags(text: str, field: str, gold, recs: dict) -> list[str]:
    """Automatic, unadjudicated tags for one (patient, field) disagreement. recs: extractor -> grounded record."""
    tags = []
    if not re.search(FIELDS[field]["cue"] if FIELDS[field]["kind"] == "cat" else r"(?i)lymph|node", text):
        tags.append("missing_in_report")
    elif all(r["status"] != "answered" for r in recs.values()):
        tags.append("not_extracted_by_any")
    both_sides = re.search(r"(?i)left\s+breast|breast\s*[,.]\s*left", text) and re.search(r"(?i)right\s+breast|breast\s*[,.]\s*right", text)
    multi_nodes = field in ("ln_examined", "ln_positive", "pathologic_n") and re.search(r"(?i)sentinel", text) and \
        re.search(r"(?i)axillary\s+(?:dissection|contents)|non-?sentinel", text)
    if both_sides or multi_nodes:
        tags.append("multiple_specimens_or_sides")
    quotes = " ".join(q for r in recs.values() for q in r.get("quotes", []))
    if _OCR.search(quotes):
        tags.append("ocr_noise_in_evidence")
    a, b = recs.get("rules"), recs.get("gpt-4.1")
    if a and b and a["status"] == "answered" and b["status"] == "answered":
        if str(a["value"]) != str(b["value"]):
            tags.append("extractors_conflict")
        elif str(a["value"]) != str(gold):
            tags.append("curated_vs_report_conflict")
    return tags


def _ctx(text, rec, width=220):
    if rec and rec.get("spans") and rec["spans"][0]:
        s, e = rec["spans"][0]
        return text[max(0, s - width):min(len(text), e + width)]
    return ""


def adjudication_sample(pids, gold, preds: dict, texts: dict, n=30, seed=20261120) -> list[dict]:
    rng = random.Random(seed)
    by_field = {}
    for f in FIELDS:
        cand = []
        for p in pids:
            g = gold[p][f]
            if g is None:
                continue
            dis = [m for m in ("rules", "gpt-4.1") if preds[m][p][f]["status"] == "answered" and str(preds[m][p][f]["value"]) != str(g)]
            if dis:
                cand.append(p)
        rng.shuffle(cand)
        by_field[f] = cand
    rows, i = [], 0
    while len(rows) < n and any(by_field.values()):
        f = list(FIELDS)[i % len(FIELDS)]
        i += 1
        if not by_field[f]:
            continue
        p = by_field[f].pop()
        recs = {m: preds[m][p][f] for m in preds}
        ctx_rec = recs["gpt-4.1"] if recs["gpt-4.1"]["status"] == "answered" else recs["rules"]
        row = {"item": len(rows) + 1, "patient_id": p, "field": f, "curated": gold[p][f]}
        for m, r in recs.items():
            row[f"{m}_value"] = r["value"] if r["status"] == "answered" else f"[{r['status']}]"
            row[f"{m}_quote"] = " | ".join(r.get("quotes", []))
        row["auto_tags"] = ",".join(error_tags(texts[p], f, gold[p][f], recs))
        row["report_context"] = _ctx(texts[p], ctx_rec)
        row["lu_true_value"] = ""
        row["lu_source_of_disagreement"] = ""
        row["lu_notes"] = ""
        rows.append(row)
    return rows


def write_adjudication(rows: list[dict], out_dir: Path, models: list[str]):
    with open(out_dir / "adjudication_sample.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    L = ["# Adjudication sample (UNREVIEWED)", "",
         "30 held-out test (patient, field) pairs where gpt-4.1 or the rules baseline answered a value that differs from the curated TCGA value.",
         "Sampled round-robin over fields, shuffled within field (seed 20261120). **Nothing here has been reviewed by a human yet.**", "",
         "For each item, read the report context (and, if needed, the full report) and fill in the CSV columns `lu_true_value` (what this report says, or `not_in_report`),",
         "`lu_source_of_disagreement` (one of: `extractor_error`, `curated_error_or_other_document`, `report_ambiguous_or_conflicting`, `multiple_specimens`, `ocr_noise`, `mapping_issue`) and `lu_notes`.", "",
         "Report excerpts: TCGA-Reports (Kefeli & Tatonetti 2024), CC BY 4.0. `auto_tags` are automatic heuristics, not adjudications.", ""]
    for r in rows:
        L.append(f"## {r['item']}. {r['patient_id']} — `{r['field']}`")
        L.append("")
        L.append(f"- **curated:** `{r['curated']}`  ·  auto tags: {r['auto_tags'] or '—'}")
        for m in ["rules"] + models:
            q = r[f"{m}_quote"].replace("\n", " ")
            L.append(f"- **{m}:** `{r[f'{m}_value']}`" + (f" — “{q}”" if q else ""))
        ctx = r["report_context"].replace("\n", " ")
        L.append(f"- **context:** …{ctx}…" if ctx else "- **context:** (no span)")
        L.append("- **Lu:** true value ____ · source ____ · notes ____")
        L.append("")
    (out_dir / "adjudication_sample.md").write_text("\n".join(L) + "\n")
