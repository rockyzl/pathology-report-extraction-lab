"""Summarise total LLM spend from the response cache (plus two uncached smoke-test calls)."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
recs = [json.loads(l) for l in (ROOT / "results/cache/llm_cache.jsonl").read_text().splitlines() if l.strip()]
by = defaultdict(lambda: {"calls": 0, "input_tokens": 0, "output_tokens": 0, "usd": 0.0})
for r in recs:
    k = f"{r['model']} prompt {r['prompt_version']}"
    by[k]["calls"] += 1
    by[k]["input_tokens"] += r["input_tokens"]
    by[k]["output_tokens"] += r["output_tokens"]
    by[k]["usd"] = round(by[k]["usd"] + r["cost_usd"], 6)
smoke = {"calls": 2, "usd": 0.007966 + 0.009768, "note": "initial connectivity smoke test (one dev report per deployment), not cached"}
total = round(sum(v["usd"] for v in by.values()) + smoke["usd"], 4)
out = {"by_model_prompt": by, "uncached_smoke_test": smoke, "total_usd_list_price": total,
       "note": "computed from token usage x list prices in protocol.json; actual Azure billing not checked"}
(ROOT / "results/llm_spend.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
