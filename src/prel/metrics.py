"""Agreement metrics (vs curated fields), Cohen's kappa and the paired patient bootstrap."""
from __future__ import annotations

import numpy as np

from .schema import CAT_FIELDS, FIELDS


def cohen_kappa(a: list, b: list) -> float | None:
    """Unweighted Cohen's kappa over paired labels. None if undefined (no pairs or chance agreement == 1)."""
    if len(a) != len(b):
        raise ValueError("length mismatch")
    n = len(a)
    if n == 0:
        return None
    cats = sorted(set(a) | set(b), key=str)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    if pe >= 1.0:
        return None
    return (po - pe) / (1 - pe)


def same(pred, gold, kind: str) -> bool:
    if pred is None:
        return False
    if kind == "count":
        return int(pred) == int(gold)
    return str(pred) == str(gold)


def field_table(pids: list[str], gold: dict, pred: dict, field: str) -> dict:
    """gold/pred: pid -> field -> value (None = unavailable / abstained); pred also carries status."""
    kind = FIELDS[field]["kind"]
    elig = [p for p in pids if gold[p][field] is not None]
    n = len(elig)
    answered = [p for p in elig if pred[p][field]["status"] == "answered"]
    rejected = sum(pred[p][field]["status"] == "rejected" for p in elig)
    agree = [p for p in answered if same(pred[p][field]["value"], gold[p][field], kind)]
    out = {"n_curated": n, "n_answered": len(answered), "n_rejected": rejected,
           "n_not_stated": n - len(answered) - rejected,
           "coverage": len(answered) / n if n else None,
           "agreement_e2e": len(agree) / n if n else None,
           "agreement_answered": len(agree) / len(answered) if answered else None}
    if kind == "cat":
        out["kappa_answered"] = cohen_kappa([str(gold[p][field]) for p in answered], [str(pred[p][field]["value"]) for p in answered])
    else:
        diffs = [abs(int(pred[p][field]["value"]) - int(gold[p][field])) for p in answered]
        out["within1_answered"] = float(np.mean([d <= 1 for d in diffs])) if diffs else None
    return out


def e2e_matrix(pids: list[str], gold: dict, pred: dict, fields: list[str]) -> np.ndarray:
    """patients x fields matrix: 1 agree, 0 disagree/abstain, nan = curated unavailable."""
    m = np.full((len(pids), len(fields)), np.nan)
    for i, p in enumerate(pids):
        for j, f in enumerate(fields):
            if gold[p][f] is not None:
                v = pred[p][f]["value"] if pred[p][f]["status"] == "answered" else None
                m[i, j] = 1.0 if same(v, gold[p][f], FIELDS[f]["kind"]) else 0.0
    return m


def macro_e2e(m: np.ndarray) -> float:
    """Unweighted mean over fields of per-field end-to-end agreement (each over its own eligible patients)."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # all-nan column = field with no curated values
        per = np.nanmean(m, axis=0)
    return float(np.nanmean(per))


def paired_bootstrap(ma: np.ndarray, mb: np.ndarray, n_boot: int = 2000, seed: int = 20261120, alpha: float = 0.05) -> dict:
    """Paired patient bootstrap of macro_e2e(a) - macro_e2e(b): resample patient rows jointly."""
    assert ma.shape == mb.shape
    rng = np.random.default_rng(seed)
    n = ma.shape[0]
    point = macro_e2e(ma) - macro_e2e(mb)
    diffs = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        diffs[b] = macro_e2e(ma[idx]) - macro_e2e(mb[idx])
    lo, hi = np.nanpercentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"diff": point, "ci_low": float(lo), "ci_high": float(hi), "n_boot": n_boot, "seed": seed,
            "a": macro_e2e(ma), "b": macro_e2e(mb), "p_boot_le_0": float(np.mean(diffs <= 0))}


def field_bootstrap(ma: np.ndarray, mb: np.ndarray, j: int, n_boot: int = 2000, seed: int = 20261120) -> dict:
    """Paired bootstrap CI of per-field e2e agreement difference (column j), over patients with curated value."""
    keep = ~np.isnan(ma[:, j])
    a, b = ma[keep, j], mb[keep, j]
    rng = np.random.default_rng(seed + j)
    n = len(a)
    if n == 0:
        return {"diff": None, "ci_low": None, "ci_high": None}
    d = np.empty(n_boot)
    for k in range(n_boot):
        idx = rng.integers(0, n, n)
        d[k] = a[idx].mean() - b[idx].mean()
    lo, hi = np.percentile(d, [2.5, 97.5])
    return {"diff": float(a.mean() - b.mean()), "ci_low": float(lo), "ci_high": float(hi)}


__all__ = ["cohen_kappa", "field_table", "e2e_matrix", "macro_e2e", "paired_bootstrap", "field_bootstrap", "CAT_FIELDS"]
