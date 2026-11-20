"""Prespecified extraction schema and mapping of curated TCGA clinical values onto it."""
from __future__ import annotations

import math
import re

NOT_STATED = "not_stated"

# field -> (kind, allowed values for categorical, curated source column(s), cue regex a supporting quote must match)
FIELDS: dict[str, dict] = {
    "er_status": {"kind": "cat", "values": ["positive", "negative"],
                  "curated": "breast_carcinoma_estrogen_receptor_status",
                  "cue": r"(?i)estrogen|oestrogen|\bE\.?R\b|\bER[-+:]"},
    "pr_status": {"kind": "cat", "values": ["positive", "negative"],
                  "curated": "breast_carcinoma_progesterone_receptor_status",
                  "cue": r"(?i)progesterone|\bP\.?R\b|\bPgR\b|\bPR[-+:]"},
    "her2_ihc_status": {"kind": "cat", "values": ["positive", "equivocal", "negative"],
                        "curated": "lab_proc_her2_neu_immunohistochemistry_receptor_status",
                        "cue": r"(?i)her-?\s?2|\bneu\b|erbb-?2|herceptest|c-?erb"},
    "her2_ihc_score": {"kind": "cat", "values": ["0", "1+", "2+", "3+"],
                       "curated": "her2_immunohistochemistry_level_result",
                       "cue": r"(?i)(?:\b[0-3]\s*\+|\+\s*[0-3]\b|\bscore\b|\b0\b|\bzero\b|negative|positive)"},
    "her2_ish_status": {"kind": "cat", "values": ["amplified", "equivocal", "not_amplified"],
                        "curated": "lab_procedure_her2_neu_in_situ_hybrid_outcome_type",
                        "cue": r"(?i)\bFISH\b|\b[CS]?ISH\b|amplif|ratio|in[- ]situ|hybridi[sz]ation|chromosome\s*17|cep\s*17"},
    "histologic_type": {"kind": "cat", "values": ["ductal", "lobular", "mixed_ductal_lobular", "mucinous", "other"],
                        "curated": "histological_type",
                        "cue": r"(?i)carcinoma|ductal|lobular|mucinous|colloid|metaplastic|medullary|papillary|tubular|cribriform|apocrine"},
    "pathologic_t": {"kind": "cat", "values": ["T1", "T2", "T3", "T4", "TX"],
                     "curated": "pathologic_T",
                     "cue": r"(?i)\b(?:y?p|y)?\s*T\s*[0-4xXIl]|\bT(?:is)\b|\bT\s*stage\s*[:=]?\s*[0-4xX]"},
    "pathologic_n": {"kind": "cat", "values": ["N0", "N1", "N2", "N3", "NX"],
                     "curated": "pathologic_N",
                     "cue": r"(?i)(?:\b|(?<=[0-9a-d]))(?:y?p|y)?\s*N\s*[0-3oOxX]|\bN\s*stage\s*[:=]?\s*[0-3oOxX]"},
    "laterality": {"kind": "cat", "values": ["left", "right"],
                   "curated": "anatomic_neoplasm_subdivision",
                   "cue": r"(?i)\bleft\b|\bright\b|\blt\.?\b|\brt\.?\b"},
    "margin_status": {"kind": "cat", "values": ["negative", "close", "positive"],
                      "curated": "margin_status",
                      "cue": r"(?i)margin|resection edge|excision edge|inked"},
    "ln_examined": {"kind": "count", "curated": "lymph_node_examined_count",
                    "cue": r"(?i)\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|none|no)\b"},
    "ln_positive": {"kind": "count", "curated": "number_of_lymphnodes_positive_by_he",
                    "cue": r"(?i)\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|none|no|negative)\b"},
}
CAT_FIELDS = [f for f, s in FIELDS.items() if s["kind"] == "cat"]
COUNT_FIELDS = [f for f, s in FIELDS.items() if s["kind"] == "count"]


def _missing(v) -> bool:
    return v is None or (isinstance(v, float) and math.isnan(v)) or str(v).strip() in ("", "[Not Available]", "[Not Evaluated]", "[Unknown]", "[Discrepancy]", "nan")


def _status3(v, mapping):
    if _missing(v):
        return None
    return mapping.get(str(v).strip().lower())


def map_histology(primary, other) -> str | None:
    if _missing(primary):
        return None
    p = str(primary).strip().lower()
    o = "" if _missing(other) else str(other).lower()
    if p == "infiltrating ductal carcinoma":
        return "ductal"
    if p == "infiltrating lobular carcinoma":
        return "lobular"
    if p == "mucinous carcinoma":
        return "mucinous"
    if p in ("mixed histology (please specify)", "other, specify"):
        if "ductal" in o and "lobular" in o:
            return "mixed_ductal_lobular"
        return "other"
    return "other"  # metaplastic, medullary, infiltrating carcinoma NOS


def map_t(v) -> str | None:
    if _missing(v):
        return None
    m = re.match(r"^T([1-4]|X)", str(v).strip(), re.I)
    return None if not m else ("T" + m.group(1).upper())


def map_n(v) -> str | None:
    if _missing(v):
        return None
    m = re.match(r"^N([0-3]|X)", str(v).strip(), re.I)
    return None if not m else ("N" + m.group(1).upper())


def map_laterality(v) -> str | None:
    if _missing(v):
        return None
    s = str(v).lower()
    has_l, has_r = "left" in s, "right" in s
    if has_l and not has_r:
        return "left"
    if has_r and not has_l:
        return "right"
    return None  # bilateral / unknown -> excluded


def map_count(v) -> int | None:
    if _missing(v):
        return None
    try:
        f = float(v)
    except ValueError:
        return None
    return int(f) if f >= 0 and f == int(f) else None


def map_curated(row: dict) -> dict:
    """Map one patient's curated clinical-matrix row onto the extraction schema. None = curated value unavailable."""
    pn = {"positive": "positive", "negative": "negative"}  # Indeterminate -> excluded
    return {
        "er_status": _status3(row.get("breast_carcinoma_estrogen_receptor_status"), pn),
        "pr_status": _status3(row.get("breast_carcinoma_progesterone_receptor_status"), pn),
        "her2_ihc_status": _status3(row.get("lab_proc_her2_neu_immunohistochemistry_receptor_status"),
                                    {"positive": "positive", "negative": "negative", "equivocal": "equivocal"}),
        "her2_ihc_score": _status3(row.get("her2_immunohistochemistry_level_result"),
                                   {"0": "0", "1+": "1+", "2+": "2+", "3+": "3+"}),
        "her2_ish_status": _status3(row.get("lab_procedure_her2_neu_in_situ_hybrid_outcome_type"),
                                    {"positive": "amplified", "negative": "not_amplified", "equivocal": "equivocal"}),
        "histologic_type": map_histology(row.get("histological_type"), row.get("histological_type_other")),
        "pathologic_t": map_t(row.get("pathologic_T")),
        "pathologic_n": map_n(row.get("pathologic_N")),
        "laterality": map_laterality(row.get("anatomic_neoplasm_subdivision")),
        "margin_status": _status3(row.get("margin_status"), {"negative": "negative", "positive": "positive", "close": "close"}),
        "ln_examined": map_count(row.get("lymph_node_examined_count")),
        "ln_positive": map_count(row.get("number_of_lymphnodes_positive_by_he")),
    }


def n_bucket(count: int) -> str:
    """AJCC 7th-edition pN bucket implied by the number of positive axillary nodes (consistency check only)."""
    if count == 0:
        return "N0"
    if count <= 3:
        return "N1"
    if count <= 9:
        return "N2"
    return "N3"
