"""Classical baseline: hand-written regular expressions with explicit evidence spans.

Each rule returns (value, [quote]) where the quote is the exact matched report substring, or (None, []) for
not_stated. The output goes through the same grounding check as the LLM output.
"""
from __future__ import annotations

import re

from .grounding import ground_extraction
from .schema import FIELDS

POS = r"(?:positive|pos\b|\+(?!\d))"
NEG = r"(?:negative|neg\b|-(?!\d))"


def _first(pattern: str, text: str, flags=re.I):
    return re.search(pattern, text, flags)


def _quote(text: str, m: re.Match) -> str:
    return text[m.start():m.end()]


def receptor(text: str, name_re: str):
    """ER/PR: '<name> [receptor(s)] [qualifiers] [:=-.] positive|negative' within a short window."""
    pat = rf"(?:{name_re})(?:\s*receptors?)?(?:\s*\([^)]{{0,25}}\))?(?:\s*(?:status|assay|results?|by\s+ihc|\(?ihc\)?|immunohistochemistry))?\s*[:=\-.]?\s*(?:is\s+|was\s+|are\s+)?(?:strongly\s+|weakly\s+|low\s+)?({POS}|{NEG})"
    for m in re.finditer(pat, text, re.I):
        ctx = text[max(0, m.start() - 40):m.start()].lower()
        if "defined as" in ctx or "considered" in ctx:  # skip assay boilerplate
            continue
        v = m.group(1).lower()
        return ("positive" if v.startswith(("pos", "+")) else "negative"), [_quote(text, m)]
    m = re.search(rf"(\bno\s+)?(?:{name_re})\s*receptors\s+(?:were\s+)?found\s+in\s+[^.]{{0,40}}?(?:neoplastic|tumou?r|cancer)", text, re.I)
    if m:
        return ("negative" if m.group(1) else "positive"), [_quote(text, m)]
    return None, []


def her2_ihc(text: str):
    pat = r"HER[-\s]?2(?:\s*/?\s*neu)?[^.;]{0,60}?(?:IHC|immunohisto\w*|hercep\s*test|immunoperoxidase)[^.;]{0,25}?[:\-]?\s*(weakly\s+positive|positive|negative|equivocal|borderline)"
    m = _first(pat, text)
    if not m:  # 'HER2/NEU: NEGATIVE' / 'HER2: Negative by IHC' (but not '... by FISH')
        for m2 in re.finditer(r"HER[-\s]?2(?:\s*/?\s*neu)?\s*(?:\([^)]{0,20}\))?\s*[:.\-]\s*(weakly\s+positive|positive|negative|equivocal|borderline)(?!\s*(?:by|for)\s+(?:FISH|ISH|CISH|SISH))", text, re.I):
            m = m2
            break
    if not m:  # 'HER2 protein stained ... . Negative reaction in invasive cancerous cells'
        m = _first(r"HER2\s+protein\s+stained[^.]{0,80}\.\s*(positive|negative)\s+reaction", text)
    if not m:
        return None, []
    v = m.group(1).lower()
    v = "equivocal" if ("weakly" in v or "borderline" in v or v == "equivocal") else v
    return v, [_quote(text, m)]


def her2_score(text: str):
    m = _first(r"HER[-\s]?2(?:\s*/?\s*neu)?[^.;]{0,80}?(?:\(\s*(?:score\s*)?([0-3])\s*\+?\s*\)|\bscore\s*(?:of\s*)?([0-3])\b\+?|\b([1-3])\s*\+)", text)
    if not m:
        return None, []
    if re.match(r"\s*(?:or|to|-)\s*[0-3]", text[m.end():m.end() + 8]) or re.search(r"(?i)\bor\b", _quote(text, m)):
        return None, []  # ranges such as 'zero or 1+' are ambiguous -> abstain
    s = next(g for g in m.groups() if g is not None)
    return (s if s == "0" else f"{s}+"), [_quote(text, m)]


def her2_ish(text: str):
    pat = (r"(?:\bFISH\b|\b[CS]?ISH\b|in[\s-]situ\s+hybridi[sz]ation)[^.;]{0,60}?"
           r"(not\s+amplified|non-?amplified|no\s+(?:evidence\s+of\s+)?(?:gene\s+)?amplification|(?<!\w)amplified|equivocal|[:=]\s*(?:negative|positive))")
    for m in re.finditer(pat, text, re.I):
        ctx = text[m.start():m.end()].lower()
        if "not performed" in ctx or "pending" in ctx:
            continue
        v = m.group(1).lower().lstrip(":= ")
        if v.startswith(("not", "non", "no ")) or v == "negative":
            return "not_amplified", [_quote(text, m)]
        if v == "equivocal":
            return "equivocal", [_quote(text, m)]
        return "amplified", [_quote(text, m)]
    return None, []


def histology(text: str):
    pat = (r"(?:infiltrating|invasive)\s+(?:mammary\s+)?(?:carcinoma\s*,?\s*)?(?:with\s+)?"
           r"(mixed\s+ductal\s+and\s+lobular|ductal\s+and\s+lobular|lobular\s+and\s+ductal|ductal\s*/\s*lobular|lobular\s*/\s*ductal|"
           r"ductal|lobular|mucinous|colloid|metaplastic|medullary|papillary|tubular|cribriform|apocrine)")
    m = _first(pat, text)
    if not m:
        m = _first(r"carcinoma\s*,\s*(?:invasive|infiltrating)\s+(ductal|lobular|mucinous)", text)
    if not m:
        return None, []
    w = m.group(1).lower()
    if "ductal" in w and "lobular" in w:
        v = "mixed_ductal_lobular"
    elif w in ("ductal", "lobular", "mucinous"):
        v = w
    elif w == "colloid":
        v = "mucinous"
    else:
        v = "other"
    return v, [_quote(text, m)]


def pathologic_t(text: str):
    m = _first(r"\by?pT\s?([1-4]|[xX]|I(?=[abc\s,.]))", text, 0) or _first(r"\b(?:y?p)T\s?([1-4xX])", text)
    if not m:
        return None, []
    g = m.group(1).upper()
    return ("T1" if g == "I" else f"T{g}"), [_quote(text, m)]


def pathologic_n(text: str):
    m = _first(r"\by?pN\s?([0-3]|[oOxX])", text, 0)
    if not m:  # 'pT2 N1a MX' style: N category immediately after a pT category
        m = _first(r"\by?pT\s?[1-4][a-d]?(?:\s*\(\w+\))?\s*,?\s*(?:p?N)\s?([0-3oOxX])", text, 0)
    if not m:
        return None, []
    g = m.group(1).upper()
    return ("N0" if g == "O" else f"N{g}"), [_quote(text, m)]


def laterality(text: str):
    """Side named with 'breast' (either order, comma or period separated); majority vote, abstain on a tie."""
    ms = list(re.finditer(r"\b(left|right)\s+breast\b|\bbreast\s*[,.]?\s*(left|right)\b", text, re.I))
    if not ms:
        ms = list(re.finditer(r"\b(left|right)\s+axill\w*|\baxilla\s*,\s*(left|right)\b", text, re.I))
    if not ms:
        return None, []
    sides = [(m.group(1) or m.group(2)).lower() for m in ms]
    nl, nr = sides.count("left"), sides.count("right")
    if nl == nr:
        return None, []
    side = "left" if nl > nr else "right"
    m = next(m for m, s_ in zip(ms, sides) if s_ == side)
    return side, [_quote(text, m)]


def margin(text: str):
    pat = (r"margins?(?:\s+of\s+(?:resection|excision))?(?:\s*\([^)]{0,20}\))?\s*(?:are|is|:|-|=)?\s*(?:widely\s+)?"
           r"(not\s+involved|uninvolved|free|negative|clear|close|positive|involved)")
    m = _first(pat, text)
    if not m:
        m = _first(r"(negative|positive|free)\s+(?:surgical\s+|resection\s+)?margins?", text)
        if not m:
            return None, []
    w = m.group(1).lower()
    if w in ("not involved", "uninvolved", "free", "negative", "clear"):
        v = "negative"
    elif w == "close":
        v = "close"
    else:
        v = "positive"
    return v, [_quote(text, m)]


_NODE_PAIR = re.compile(r"\(?\b(\d{1,2})\s*(?:/|of|out\s+of)\s*(\d{1,2})\b\)?(?=[^.;]{0,40}?(?:lymph\s*nodes?|nodes?\b|LN))"
                        r"|(?:lymph\s*nodes?|nodes?)[^.;]{0,60}?\(\s*(\d{1,2})\s*/\s*(\d{1,2})\s*\)", re.I)


def node_counts(text: str):
    """Returns ((pos, quotes), (exam, quotes)). Synoptic labels first, else x/y pairs (max-pair or sum heuristic)."""
    me = _first(r"(?:number\s+of\s+)?(?:lymph\s+)?nodes?\s+examined\s*[:=]?\s*(\d{1,2})\b", text) or \
        _first(r"total\s+(?:number\s+of\s+)?(?:lymph\s+)?nodes?\s*(?:examined|recovered|identified)?\s*[:=]\s*(\d{1,2})\b", text)
    mp = _first(r"(?:number\s+of\s+)?(?:lymph\s+)?nodes?\s+(?:positive|involved|with\s+(?:macro)?metasta\w*)(?:\s+for\s+\w+)?\s*[:=]\s*(\d{1,2})\b", text)
    if me and mp:
        return (int(mp.group(1)), [_quote(text, mp)]), (int(me.group(1)), [_quote(text, me)])
    pairs = []
    for m in _NODE_PAIR.finditer(text):
        a, b = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        a, b = int(a), int(b)
        if 0 < b <= 60 and a <= b:
            pairs.append((a, b, _quote(text, m)))
    if not pairs:
        return (None, []), (None, [])
    uniq = {}
    for a, b, q in pairs:
        uniq.setdefault((a, b), q)
    keys = list(uniq)
    big = max(keys, key=lambda k: k[1])
    rest = [k for k in keys if k != big]
    if not rest or (sum(k[0] for k in rest) == big[0] and sum(k[1] for k in rest) == big[1]):
        chosen = [big]
    else:
        chosen = keys
    quotes = [uniq[k] for k in chosen][:3]
    if len(chosen) > 3:
        return (None, []), (None, [])
    return (sum(k[0] for k in chosen), quotes), (sum(k[1] for k in chosen), quotes)


def extract_claims(text: str) -> dict:
    (pos, pq), (exam, eq) = node_counts(text)
    out = {
        "er_status": receptor(text, r"estrogen|oestrogen|\bER\b"),
        "pr_status": receptor(text, r"progesterone|\bPR\b|\bPgR\b"),
        "her2_ihc_status": her2_ihc(text),
        "her2_ihc_score": her2_score(text),
        "her2_ish_status": her2_ish(text),
        "histologic_type": histology(text),
        "pathologic_t": pathologic_t(text),
        "pathologic_n": pathologic_n(text),
        "laterality": laterality(text),
        "margin_status": margin(text),
        "ln_examined": (exam, eq),
        "ln_positive": (pos, pq),
    }
    assert set(out) == set(FIELDS)
    return {f: {"value": v, "quotes": q} for f, (v, q) in out.items()}


def extract(text: str) -> dict:
    return ground_extraction(extract_claims(text), text)
