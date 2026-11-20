"""POST HOC (not prespecified): what did grounding rejections cost? Compares each rejected claim with the curated value."""
import json
from pathlib import Path

from prel import evaluate as E

ROOT = Path(__file__).resolve().parents[1]
rep, gold, mem, texts = E.load_all()
out = {"label": "post hoc, not prespecified; test set, after the one-shot run"}
for m in ["gpt-4.1", "gpt-4o"]:
    c = {"rejected": 0, "claimed_equals_curated": 0, "claimed_differs": 0, "no_curated": 0}
    for line in (ROOT / f"results/extractions/test_{m}.jsonl").read_text().splitlines():
        r = json.loads(line)
        p = r.pop("patient_id")
        for f, x in r.items():
            if x["status"] != "rejected":
                continue
            c["rejected"] += 1
            g = gold[p][f]
            k = "no_curated" if g is None else ("claimed_equals_curated" if str(x.get("claimed")) == str(g) else "claimed_differs")
            c[k] += 1
    out[m] = c
(ROOT / "results/posthoc_rejections.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
