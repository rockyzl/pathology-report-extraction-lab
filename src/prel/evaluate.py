"""Glue: run extractors over a patient set and compute the prespecified tables."""
from __future__ import annotations

from . import cohort, llm, rules
from .metrics import e2e_matrix, field_table, macro_e2e
from .schema import CAT_FIELDS, COUNT_FIELDS, FIELDS


def gold_dict(curated) -> dict:
    g = {}
    for r in curated.to_dict("records"):
        d = {}
        for f in FIELDS:
            v = r[f]
            if v is None or v != v:
                d[f] = None
            elif FIELDS[f]["kind"] == "count":
                d[f] = int(float(v))
            else:
                d[f] = str(v)
        g[r["patient_id"]] = d
    return g


def run_rules(pids, texts) -> dict:
    return {p: rules.extract(texts[p]) for p in pids}


def run_llm(model, pids, texts, **kw) -> tuple[dict, list[dict]]:
    recs = llm.run(model, [(p, texts[p]) for p in pids], **kw)
    return {r["patient_id"]: llm.to_extraction(r, texts[r["patient_id"]]) for r in recs}, recs


def tables(pids, gold, pred) -> dict:
    per = {f: field_table(pids, gold, pred, f) for f in FIELDS}
    m_cat = e2e_matrix(pids, gold, pred, CAT_FIELDS)
    m_all = e2e_matrix(pids, gold, pred, list(FIELDS))
    return {"per_field": per, "macro_e2e_categorical": macro_e2e(m_cat), "macro_e2e_all": macro_e2e(m_all),
            "count_fields": COUNT_FIELDS}


def load_all():
    rep = cohort.load_reports()
    cur = cohort.load_curated()
    mem = cohort.load_membership()
    texts = dict(zip(rep.patient_id, rep.text))
    return rep, gold_dict(cur), mem, texts


def fmt(t: dict) -> str:
    lines = [f"{'field':16s} {'n':>4s} {'cov':>6s} {'e2e':>6s} {'ans':>6s} {'kappa':>6s} {'rej':>4s}"]
    for f, r in t["per_field"].items():
        k = r.get("kappa_answered")
        lines.append(f"{f:16s} {r['n_curated']:4d} {r['coverage'] or 0:6.3f} {r['agreement_e2e'] or 0:6.3f} "
                     f"{(r['agreement_answered'] or 0):6.3f} {(k if k is not None else float('nan')):6.3f} {r['n_rejected']:4d}")
    lines.append(f"macro e2e (categorical) {t['macro_e2e_categorical']:.3f}; all {t['macro_e2e_all']:.3f}")
    return "\n".join(lines)
