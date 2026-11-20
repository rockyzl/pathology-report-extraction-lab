"""Programmatic quote grounding: every extracted value must cite text that actually occurs in the report.

Match rule (prespecified): exact substring match, or exact match after collapsing every whitespace run to a single
space in both quote and report. No case folding, no fuzzy matching, no OCR correction.
"""
from __future__ import annotations

import re

from .schema import FIELDS

NUM_WORDS = {0: ["zero", "no", "none", "negative", "free", "without"], 1: ["one", "single"], 2: ["two"], 3: ["three"],
             4: ["four"], 5: ["five"], 6: ["six"], 7: ["seven"], 8: ["eight"], 9: ["nine"], 10: ["ten"],
             11: ["eleven"], 12: ["twelve"], 13: ["thirteen"], 14: ["fourteen"], 15: ["fifteen"]}
_WS = re.compile(r"\s+")


def _collapse(s: str) -> tuple[str, list[int]]:
    """Collapse whitespace runs to one space; return collapsed string and index map collapsed->original."""
    out, idx = [], []
    prev_ws = False
    for i, ch in enumerate(s):
        if ch.isspace():
            if not prev_ws:
                out.append(" ")
                idx.append(i)
            prev_ws = True
        else:
            out.append(ch)
            idx.append(i)
            prev_ws = False
    return "".join(out), idx


def locate(quote: str, text: str) -> tuple[int, int] | None:
    """Return (start, end) character offsets of quote in text, or None if not grounded."""
    q = quote.strip()
    if not q:
        return None
    i = text.find(q)
    if i >= 0:
        return i, i + len(q)
    ct, idx = _collapse(text)
    cq = _WS.sub(" ", q)
    j = ct.find(cq)
    if j < 0:
        return None
    return idx[j], idx[j + len(cq) - 1] + 1


def number_supported(value: int, quotes: list[str]) -> bool:
    if len(quotes) > 1:  # summation across specimens is allowed; each quote is still grounded
        return any(re.search(r"\d", q) or any(w in q.lower() for ws in NUM_WORDS.values() for w in ws) for q in quotes)
    q = quotes[0]
    if re.search(rf"(?<!\d){value}(?!\d)", q):
        return True
    return any(re.search(rf"(?i)\b{w}\b", q) for w in NUM_WORDS.get(value, []))


def ground_field(field: str, value, quotes: list[str], text: str) -> dict:
    quotes = [q for q in (quotes or []) if q and q.strip()]
    if value is None:
        return {"value": None, "status": "not_stated", "reason": "", "quotes": [], "spans": []}
    if not quotes:
        return {"value": None, "status": "rejected", "reason": "no_quote", "claimed": value, "quotes": [], "spans": []}
    spans = [locate(q, text) for q in quotes]
    if any(s is None for s in spans):
        return {"value": None, "status": "rejected", "reason": "quote_not_in_report", "claimed": value,
                "quotes": quotes, "spans": [list(s) if s else None for s in spans]}
    spec = FIELDS[field]
    if not any(re.search(spec["cue"], q) for q in quotes):
        return {"value": None, "status": "rejected", "reason": "quote_lacks_field_cue", "claimed": value,
                "quotes": quotes, "spans": [list(s) for s in spans]}
    if spec["kind"] == "count" and not number_supported(int(value), quotes):
        return {"value": None, "status": "rejected", "reason": "number_not_in_quote", "claimed": value,
                "quotes": quotes, "spans": [list(s) for s in spans]}
    return {"value": value, "status": "answered", "reason": "", "quotes": quotes, "spans": [list(s) for s in spans]}


def ground_extraction(claims: dict, text: str) -> dict:
    """claims: field -> {"value": v or None, "quotes": [...]} -> field -> grounded record."""
    return {f: ground_field(f, claims.get(f, {}).get("value"), claims.get(f, {}).get("quotes", []), text) for f in FIELDS}
