"""Summarise LLM spend from the response caches (list price x logged usage; billing not checked).

- current run: results/cache/llm_cache.jsonl (OpenAI API)
- superseded run: results/cache/superseded_azure/llm_cache.jsonl (provisional Azure OpenAI endpoint), plus its
  two uncached connectivity smoke-test calls
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def summarise(path):
    recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []
    by = defaultdict(lambda: {"calls": 0, "input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "usd": 0.0})
    for r in recs:
        k = f"{r['model']} prompt {r['prompt_version']}"
        by[k]["calls"] += 1
        by[k]["input_tokens"] += r["input_tokens"]
        by[k]["cached_input_tokens"] += r.get("cached_input_tokens", 0)
        by[k]["output_tokens"] += r["output_tokens"]
        by[k]["usd"] = round(by[k]["usd"] + r["cost_usd"], 6)
    return dict(by), round(sum(v["usd"] for v in by.values()), 4)


cur, cur_total = summarise(ROOT / "results/cache/llm_cache.jsonl")
old, old_total = summarise(ROOT / "results/cache/superseded_azure/llm_cache.jsonl")
smoke = 0.007966 + 0.009768
out = {"current_openai_api": {"by_model_prompt": cur, "total_usd_list_price": cur_total,
                              "pricing": "OpenAI API standard list prices incl. cached-input rate (protocol.json)"},
       "superseded_azure": {"by_model_prompt": old, "uncached_smoke_test_usd": round(smoke, 6),
                            "total_usd_list_price": round(old_total + smoke, 4)},
       "note": "token usage from API usage fields x list prices; actual billing not checked"}
(ROOT / "results/llm_spend.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
