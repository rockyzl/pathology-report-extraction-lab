"""Render results/test_results.json into markdown tables (results/results_tables.md)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "results" / "test_results.json").read_text())
M = ["rules", "gpt-4.1", "gpt-4o"]


def f3(x):
    return "—" if x is None else f"{x:.3f}"


def ci(d):
    return f"{d['diff']:+.3f} [{d['ci_low']:+.3f}, {d['ci_high']:+.3f}]"


PROV = ", ".join(sorted({p for m in ("gpt-4.1", "gpt-4o") for p in R["cost"][m].get("providers", ["azure_openai_superseded"])}))
L = [f"# Held-out test results (n = {R['n_test']} patients, frozen commit `{R['frozen_commit'][:7]}`, LLM provider: {PROV})", "",
     "Agreement with curated TCGA clinical fields, **not accuracy**. e2e = agreeing answers / patients with a curated value",
     "(not_stated and grounding rejections count as non-agreement). ans = agreement among answered. κ = Cohen's kappa over answered.", ""]
L.append("## Per-field agreement")
L.append("")
hdr = "| field | n curated | " + " | ".join(f"{m} cov | {m} e2e | {m} ans | {m} κ" for m in M) + " |"
L.append(hdr)
L.append("|" + "---|" * (2 + 4 * len(M)))
fields = list(R["tables"]["rules"]["per_field"])
for f in fields:
    row = [f, str(R["tables"]["rules"]["per_field"][f]["n_curated"])]
    for m in M:
        t = R["tables"][m]["per_field"][f]
        k = t.get("kappa_answered") if "kappa_answered" in t else None
        row += [f3(t["coverage"]), f3(t["agreement_e2e"]), f3(t["agreement_answered"]), f3(k) if "kappa_answered" in t else "n/a"]
    L.append("| " + " | ".join(row) + " |")
L.append("| **macro, 10 categorical** | | " + " | ".join(f" | {f3(R['tables'][m]['macro_e2e_categorical'])} | | " for m in M) + " |")
L.append("| **macro, all 12** | | " + " | ".join(f" | {f3(R['tables'][m]['macro_e2e_all'])} | | " for m in M) + " |")
L.append("")
L.append("## Primary comparison (prespecified)")
L.append("")
p = R["primary"]
L.append(f"- {p['estimand']}: **{ci(p)}** (paired patient bootstrap, B = {p['n_boot']}, seed {p['seed']}); gpt-4.1 {p['a']:.3f} vs rules {p['b']:.3f}. Decision: **{p['decision']}**.")
s = R["secondary"]
L.append(f"- gpt-4o − rules (10 categorical): {ci(s['gpt-4o_minus_rules_cat'])}")
L.append(f"- gpt-4.1 − gpt-4o (10 categorical): {ci(s['gpt-4.1_minus_gpt-4o_cat'])}")
L.append(f"- gpt-4.1 − rules (all 12): {ci(s['gpt-4.1_minus_rules_all12'])}; gpt-4o − rules (all 12): {ci(s['gpt-4o_minus_rules_all12'])}")
L.append("")
L.append("Per-field e2e difference vs rules (descriptive, no multiplicity correction):")
L.append("")
L.append("| field | gpt-4.1 − rules [95% CI] | gpt-4o − rules [95% CI] |")
L.append("|---|---|---|")
for f in fields:
    L.append(f"| {f} | {ci(s['per_field_gpt-4.1_minus_rules'][f])} | {ci(s['per_field_gpt-4o_minus_rules'][f])} |")
L.append("")
L.append("## Abstention and grounding")
L.append("")
L.append("| extractor | field cells | claimed values | grounding rejections | rejection rate of claims | not_stated | rejection reasons |")
L.append("|---|---|---|---|---|---|---|")
for m in M:
    g = R["grounding"][m]
    L.append(f"| {m} | {g['cells']} | {g['claimed_values']} | {g['rejected']} | {f3(g['rejection_rate_of_claims'])} | {g['not_stated']} | {json.dumps(g['reasons'])} |")
L.append("")
L.append("## Cross-field consistency checks (violations / patients with both fields answered)")
L.append("")
L.append("| check | " + " | ".join(M + ["curated"]) + " |")
L.append("|---|" + "---|" * (len(M) + 1))
for c in ["positive_le_examined", "pn_vs_positive_count", "her2_score_vs_status"]:
    L.append(f"| {c} | " + " | ".join(f"{R['consistency'][m][c]['violations']}/{R['consistency'][m][c]['n_both']}" for m in M + ["curated"]) + " |")
L.append("")
L.append("## Cost and latency per report (test set)")
L.append("")
L.append("| model | reports | input tokens mean (p95) | cached input tokens mean | output tokens mean (p95) | latency s mean / median / p95 | USD mean | USD total |")
L.append("|---|---|---|---|---|---|---|---|")
for m in ["gpt-4.1", "gpt-4o"]:
    c = R["cost"][m]
    L.append(f"| {m} ({', '.join(c['deployment_models'])}) | {c['n_reports']} | {c['input_tokens']['mean']:.0f} ({c['input_tokens']['p95']:.0f}) | "
             f"{c.get('cached_input_tokens', {}).get('mean', 0):.0f} | {c['output_tokens']['mean']:.0f} ({c['output_tokens']['p95']:.0f}) | {c['seconds']['mean']:.2f} / {c['seconds']['median']:.2f} / {c['seconds']['p95']:.2f} | "
             f"{c['cost_usd']['mean']:.4f} | {c['cost_usd']['total']:.2f} |")
L.append("")
L.append("Latency is wall-clock per call with 2 concurrent workers, including any SDK retry back-off. Cost = API usage x list price (cached-input rate where reported); billing not checked.")
L.append("")
L.append("## Automatic error-source tags (unadjudicated heuristics; one disagreement can carry several tags)")
L.append("")
for m in M:
    L.append(f"- **{m}**: " + "; ".join(f"{kind}: " + ", ".join(f"{t} {n}" for t, n in sorted(d.items(), key=lambda x: -x[1])) for kind, d in R["error_tags"][m].items()))
L.append("")
(ROOT / "results" / "results_tables.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
