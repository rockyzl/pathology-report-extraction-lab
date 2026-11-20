"""Dev-only LLM iteration on the prespecified 80-patient dev sample (never touches test)."""
import json
import sys

from prel import evaluate as E

model = sys.argv[1] if len(sys.argv) > 1 else "gpt-4.1"
rep, gold, mem, texts = E.load_all()
pids = mem["llm_dev_sample"]
pred, recs = E.run_llm(model, pids, texts, budget_usd=10.0)
rules = E.run_rules(pids, texts)
print("LLM", model); print(E.fmt(E.tables(pids, gold, pred)))
print("rules (same 80)"); print(E.fmt(E.tables(pids, gold, rules)))
print(json.dumps({"cost": round(sum(r["cost_usd"] for r in recs), 3), "in": sum(r["input_tokens"] for r in recs),
                  "out": sum(r["output_tokens"] for r in recs), "sec_mean": round(sum(r["seconds"] for r in recs) / len(recs), 2)}))
