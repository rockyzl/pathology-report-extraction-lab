"""LLM extractor: OpenAI API (pinned model snapshots), strict JSON schema, jsonl cache, programmatic grounding.

Provider: the official OpenAI API at https://api.openai.com/v1, authenticated with OPENAI_API_KEY from the
environment (the project owner's OpenAI account). The base URL is passed explicitly so an ambient
OPENAI_BASE_URL cannot redirect calls. Earlier runs used a provisional Azure OpenAI endpoint and are superseded
(docs/protocol.md, Addendum 2).
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from pathlib import Path

from .grounding import ground_extraction
from .schema import FIELDS, NOT_STATED

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "results" / "cache" / "llm_cache.jsonl"
PROVIDER = "openai"
BASE_URL = "https://api.openai.com/v1"
PROMPT_VERSION = "v3"
# logical name -> pinned snapshot (same model versions as the superseded runs)
SNAPSHOTS = {"gpt-4.1": "gpt-4.1-2025-04-14", "gpt-4o": "gpt-4o-2024-11-20"}

# USD per 1M tokens, OpenAI API list prices (standard tier) as recorded in protocol.json; billing not checked
PRICES = {"gpt-4.1": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
          "gpt-4o": {"input": 2.50, "cached_input": 1.25, "output": 10.00}}
EST_USD_PER_CALL = 0.0095  # conservative pre-run estimate used by the budget guard

SYSTEM_PROMPT = """You extract structured fields from one OCR'd breast-cancer surgical pathology report.

Rules:
1. Use ONLY what the report text explicitly states. Do not infer, compute or guess. In particular do not derive the
   pT category from tumor size, do not derive the pN category from node counts, and do not derive HER2 status from a
   score unless the report itself states the status.
2. For every field either give a value with 1-3 supporting quotes, or give "not_stated" (counts: null) with an empty
   quote list.
3. Each quote must be copied VERBATIM from the report: same characters, same OCR errors, same punctuation and spacing.
   Do not correct typos or accents. Each quote must be ONE contiguous stretch of the report: never use "...", never
   join text from different places, never add or drop words. Line breaks in the source appear as ". " - keep them.
   Keep quotes short (<= 120 characters). A quote is rejected automatically if it does not occur in the report, so
   when unsure, quote a shorter piece.
4. Fields:
   - er_status / pr_status: estrogen / progesterone receptor result of the invasive breast carcinoma.
   - her2_ihc_status: HER2 immunohistochemistry interpretation (positive / equivocal / negative). Older reports call
     2+ "weakly positive" or "borderline": record that as equivocal. A HER2 result reported only "by FISH" is ISH,
     not IHC.
   - her2_ihc_score: HER2 IHC score 0, 1+, 2+ or 3+.
   - her2_ish_status: HER2 in-situ hybridisation (FISH/CISH/SISH) result: amplified / equivocal / not_amplified.
   - histologic_type: invasive carcinoma type. ductal (incl. "no special type"), lobular, mixed_ductal_lobular (both
     ductal and lobular features in the invasive tumor), mucinous (colloid), other (e.g. metaplastic, medullary,
     papillary, tubular, carcinoma NOS).
   - pathologic_t / pathologic_n: the primary-tumor (pT) and regional-node (pN) category only when the report states a
     TNM category (e.g. "pT2", "T1c", "pN1a"). Report the main category: T1-T4 or TX; N0-N3 or NX
     (e.g. pT1c -> T1, pN1mi -> N1, pN0(i+) -> N0). OCR may print a zero as the letter O ("pNO" = pN0).
     Ignore clinical staging in the clinical history (e.g. "T1N0M0 ... on physical exam").
   - laterality: side of the breast with the primary tumor (left / right).
   - margin_status: invasive carcinoma at the final surgical margins: positive (tumor at ink), close (report explicitly
     calls a margin close), negative (free/uninvolved).
   - ln_examined / ln_positive: total number of regional lymph nodes examined / positive for metastatic carcinoma,
     summed across all specimens of this report (e.g. sentinel nodes plus axillary dissection). Quote each part.
5. If the report covers several specimens or conflicting statements, use the final diagnosis / synoptic summary for
   the main invasive tumor."""


def response_schema() -> dict:
    props = {}
    for f, s in FIELDS.items():
        if s["kind"] == "cat":
            value = {"type": "string", "enum": s["values"] + [NOT_STATED]}
        else:
            value = {"type": ["integer", "null"]}
        props[f] = {"type": "object", "additionalProperties": False, "required": ["value", "quotes"],
                    "properties": {"value": value, "quotes": {"type": "array", "items": {"type": "string"}}}}
    return {"type": "object", "additionalProperties": False, "required": list(FIELDS), "properties": props}


def _client():
    from openai import OpenAI

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=key, base_url=BASE_URL, timeout=120, max_retries=8)


def cache_key(model: str, patient_id: str, text: str) -> str:
    h = hashlib.sha256(f"{PROVIDER}|{SNAPSHOTS[model]}|{PROMPT_VERSION}|{SYSTEM_PROMPT}|{patient_id}|{text}".encode()).hexdigest()
    return h[:24]


def load_cache() -> dict:
    out = {}
    if CACHE.exists():
        for line in CACHE.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["key"]] = r
    return out


def call_model(client, model: str, patient_id: str, text: str) -> dict:
    t0 = time.monotonic()
    raw_resp = client.chat.completions.with_raw_response.create(
        model=SNAPSHOTS[model], temperature=0, max_tokens=3000, seed=0,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": f"REPORT:\n<<<\n{text}\n>>>"}],
        response_format={"type": "json_schema", "json_schema": {"name": "pathology_extraction", "strict": True,
                                                                "schema": response_schema()}})
    secs = time.monotonic() - t0
    r = raw_resp.parse()
    ch = r.choices[0]
    u = r.usage
    details = getattr(u, "prompt_tokens_details", None)
    cached = int(getattr(details, "cached_tokens", 0) or 0) if details else 0
    rec = {"key": cache_key(model, patient_id, text), "provider": PROVIDER, "model": model,
           "requested_snapshot": SNAPSHOTS[model], "deployment_model": r.model,
           "prompt_version": PROMPT_VERSION, "patient_id": patient_id, "finish_reason": ch.finish_reason,
           "input_tokens": u.prompt_tokens, "cached_input_tokens": cached, "output_tokens": u.completion_tokens,
           "seconds": round(secs, 3), "raw": ch.message.content, "refusal": ch.message.refusal,
           "system_fingerprint": r.system_fingerprint, "response_id": r.id,
           "openai_organization": raw_resp.headers.get("openai-organization"),
           "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    rec["cost_usd"] = cost_usd(model, rec["input_tokens"], cached, rec["output_tokens"])
    return rec


def cost_usd(model: str, input_tokens: int, cached_input_tokens: int, output_tokens: int) -> float:
    p = PRICES[model]
    uncached = input_tokens - cached_input_tokens
    return round((uncached * p["input"] + cached_input_tokens * p["cached_input"] + output_tokens * p["output"]) / 1e6, 6)


def parse(raw: str | None) -> dict | None:
    try:
        return json.loads(raw) if raw else None
    except json.JSONDecodeError:
        return None


def to_extraction(rec: dict, text: str) -> dict:
    """Turn one cached LLM record into the common extraction format, with programmatic grounding."""
    obj = parse(rec.get("raw")) if rec.get("finish_reason") == "stop" else None
    if obj is None:
        return {f: {"value": None, "status": "rejected", "reason": "invalid_response", "quotes": [], "spans": []} for f in FIELDS}
    claims = {}
    for f in FIELDS:
        v = obj[f]["value"]
        if v == NOT_STATED:
            v = None
        claims[f] = {"value": v, "quotes": obj[f]["quotes"]}
    return ground_extraction(claims, text)


_spend_lock = threading.Lock()
_spend = {"usd": 0.0, "cap": None}


def run(model: str, items: list[tuple[str, str]], workers: int = 2, budget_usd: float = 6.0) -> list[dict]:
    """items: (patient_id, text). Returns cached-or-fresh records; appends fresh ones to the jsonl cache.

    Budget: refuses to start if cached spend + a conservative estimate exceeds budget_usd, and stops issuing
    new calls once actual spend reaches budget_usd.
    """
    from concurrent.futures import ThreadPoolExecutor

    cache = load_cache()
    spent = sum(r.get("cost_usd", 0) for r in cache.values())
    todo = [(p, t) for p, t in items if cache_key(model, p, t) not in cache]
    est = len(todo) * EST_USD_PER_CALL
    if spent + est > budget_usd:
        raise RuntimeError(f"budget guard: spent {spent:.2f} + est {est:.2f} > {budget_usd}")
    _spend.update(usd=spent, cap=budget_usd)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    client = _client() if todo else None
    with ThreadPoolExecutor(workers) as ex, open(CACHE, "a") as fh:
        for rec in ex.map(lambda pt: _safe_call(client, model, *pt), todo):
            if rec is None:
                continue
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            cache[rec["key"]] = rec
    missing = [p for p, t in items if cache_key(model, p, t) not in cache]
    if missing:
        raise RuntimeError(f"{len(missing)} calls failed or skipped (not cached); rerun to retry: {missing[:5]}")
    return [cache[cache_key(model, p, t)] for p, t in items]


def _safe_call(client, model, pid, text):
    with _spend_lock:
        if _spend["cap"] is not None and _spend["usd"] >= _spend["cap"]:
            print(f"[llm] budget cap {_spend['cap']} reached; skipping {model} {pid}")
            return None
    try:
        rec = call_model(client, model, pid, text)
    except Exception as e:  # transient API errors are not cached; a rerun retries them
        print(f"[llm] {model} {pid} failed: {type(e).__name__}: {str(e)[:200]}")
        return None
    with _spend_lock:
        _spend["usd"] += rec["cost_usd"]
    return rec
