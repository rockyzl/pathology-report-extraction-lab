"""Acquire + verify raw inputs, build the cohort and the patient-level split. Writes data/manifest.json and data/membership.json."""
import json
from datetime import datetime, timezone

from prel import cohort, data
from prel.schema import FIELDS

manifest = {"created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "sources": data.acquire()}
b = cohort.build()
rep, cur, mem = b["reports"], b["curated"], b["membership"]
manifest["cohort"] = {
    "brca_reports_in_tcga_reports": int(len(rep)),
    "dev": len(mem["dev"]), "test": len(mem["test"]), "llm_dev_sample": len(mem["llm_dev_sample"]),
    "report_chars": {k: round(float(v), 1) for k, v in rep.text.str.len().describe().items()},
    "curated_available": {f: {s: int(cur.loc[cur.split == s, f].notna().sum()) for s in ("dev", "test")} for f in FIELDS},
    "curated_distribution": {f: {str(k): int(v) for k, v in cur[f].value_counts(dropna=False).items()} for f in FIELDS if FIELDS[f]["kind"] == "cat"},
    "tissue_source_sites": int(rep.tss.nunique()),
}
(data.ROOT / "data" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
(data.ROOT / "data" / "membership.json").write_text(json.dumps(mem, indent=1) + "\n")
print(json.dumps(manifest["cohort"], indent=1))
