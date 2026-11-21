"""Regenerate the README results section (between '## Results' and '## Limitations') from results files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "results/test_results.json").read_text())
C = json.loads((ROOT / "results/replication_vs_superseded.json").read_text())
SP = json.loads((ROOT / "results/llm_spend.json").read_text())
PH = json.loads((ROOT / "results/posthoc_rejections.json").read_text())
M = ["rules", "gpt-4.1", "gpt-4o"]
# original (pre-rewrite) commit ID -> final ID, from docs/commit-map.md
CMAP = {c[0]: c[2] for c in ([x.strip(" `") for x in ln.strip().strip("|").split("|")]
                             for ln in (ROOT / "docs/commit-map.md").read_text().splitlines()) if len(c) >= 3 and len(c[0]) == 7}


def cid(sha):
    """Cite a recorded commit ID with its final ID after the history rewrite."""
    s = sha[:7]
    return f"`{s}` (now `{CMAP[s]}`)" if s in CMAP and CMAP[s] != s else f"`{s}`"


def f3(x):
    return "—" if x is None else f"{x:.3f}"


def ci(d):
    return f"{d['diff']:+.3f} (95% CI {d['ci_low']:+.3f} to {d['ci_high']:+.3f})"


L = ["## Results (held-out test, 258 patients; OpenAI API replication, run once)", "",
     f"Provider: OpenAI API, pinned snapshots `gpt-4.1-2025-04-14` / `gpt-4o-2024-11-20`, frozen commit `{R['frozen_commit'][:7]}` (original ID, now `{CMAP[R['frozen_commit'][:7]]}`; recorded in `results/freeze.json`, protocol Addendum 2; ID mapping in [`docs/commit-map.md`](docs/commit-map.md)). "
     "These replace the superseded v1.0 run (same snapshots, prompt, schema, rules and analysis via a provisional Azure OpenAI endpoint), which is kept for comparison in `results/superseded_azure/`.", "",
     "Full tables: [`results/results_tables.md`](results/results_tables.md); raw numbers: `results/test_results.json`; comparison with the superseded run: `results/replication_vs_superseded.json`.", "",
     "Per-field **end-to-end agreement** with curated values (abstentions count as non-agreement) / **coverage** / **Cohen's κ** (over answered):", "",
     "| field | n | rules | gpt-4.1 | gpt-4o |", "|---|---|---|---|---|"]
for f, t in R["tables"]["rules"]["per_field"].items():
    cells = []
    for m in M:
        x = R["tables"][m]["per_field"][f]
        k = f3(x["kappa_answered"]) if "kappa_answered" in x else "n/a"
        cells.append(f"{f3(x['agreement_e2e'])} / {f3(x['coverage'])} / {k}")
    L.append(f"| {f} | {t['n_curated']} | " + " | ".join(cells) + " |")
L.append("| **macro, 10 categorical fields** | | " + " | ".join(f"**{f3(R['tables'][m]['macro_e2e_categorical'])}**" for m in M) + " |")
L.append("| macro, all 12 fields | | " + " | ".join(f3(R["tables"][m]["macro_e2e_all"]) for m in M) + " |")
p, s = R["primary"], R["secondary"]
L += ["", f"**Primary comparison (prespecified):** macro end-to-end agreement over the **10 categorical fields**, gpt-4.1 − rules = **{ci(p)}**, paired patient bootstrap B = 2000 → *{p['decision']}*.",
      f"Secondary: gpt-4o − rules {ci(s['gpt-4o_minus_rules_cat'])}; gpt-4.1 − gpt-4o {ci(s['gpt-4.1_minus_gpt-4o_cat'])}; gpt-4.1 − rules over all 12 fields {ci(s['gpt-4.1_minus_rules_all12'])}.", ""]
cp = C["primary"]
ident = C["cell_identity"]
L += ["**Replication vs superseded run.** "
      f"Primary estimate {cp['replication']['diff']:+.3f} [{cp['replication']['ci_low']:+.3f}, {cp['replication']['ci_high']:+.3f}] vs superseded {cp['superseded']['diff']:+.3f} [{cp['superseded']['ci_low']:+.3f}, {cp['superseded']['ci_high']:+.3f}]; "
      f"same decision: {C['conclusion']['same_primary_decision']}. Rules outputs identical: {C['rules_identical']}. "
      f"Grounded field outputs (status + value) identical between runs in {ident['gpt-4.1']['rate']*100:.1f}% of gpt-4.1 cells and {ident['gpt-4o']['rate']*100:.1f}% of gpt-4o cells (temperature 0 is not bit-deterministic across providers/infrastructure).", ""]
g = R["grounding"]
L += ["**Abstention and grounding.** Of 3,096 field cells (258 × 12):", ""]
for m in M:
    x = g[m]
    L.append(f"- {m}: {x['claimed_values']} values claimed, {x['rejected']} rejected by grounding ({x['rejection_rate_of_claims']*100:.1f}% of claims: "
             f"{', '.join(f'{k} {v}' for k, v in x['reasons'].items()) or 'none'}), {x['not_stated']} not_stated.")
L += [f"- Post hoc (`results/posthoc_rejections.json`): {PH['gpt-4.1']['claimed_equals_curated']} of gpt-4.1's {PH['gpt-4.1']['rejected']} rejected claims "
      f"(gpt-4o: {PH['gpt-4o']['claimed_equals_curated']} of {PH['gpt-4o']['rejected']}) had a claimed value equal to the curated value. The strict all-quotes-verbatim rule costs agreement; it is kept as prespecified. Grounding checks that a quote **exists** and mentions the field, not that it supports the value.", "",
      "**Cost / latency (test, per report; API usage × list price, billing not checked).**", ""]
for m in ["gpt-4.1", "gpt-4o"]:
    c = R["cost"][m]
    L.append(f"- {m}: mean {c['input_tokens']['mean']:.0f} input (of which {c['cached_input_tokens']['mean']:.0f} cached) + {c['output_tokens']['mean']:.0f} output tokens, "
             f"USD {c['cost_usd']['mean']:.4f}/report (USD {c['cost_usd']['total']:.2f} for 258); latency mean {c['seconds']['mean']:.2f} s / median {c['seconds']['median']:.2f} s / p95 {c['seconds']['p95']:.2f} s (2 workers).")
L += [f"- Spend on the OpenAI API for this replication: **USD {SP['current_openai_api']['total_usd_list_price']:.2f}** (cap 6). Superseded run (dev iteration + test + smoke): USD {SP['superseded_azure']['total_usd_list_price']:.2f}. "
      "Rules: 0.92 s for all 1,034 reports on CPU (`results/rules_timing.json`).", ""]
K = R["consistency"]
L += ["**Cross-field consistency checks** (violations / patients with both fields answered; checks, not relation extraction):", "",
      "| check | rules | gpt-4.1 | gpt-4o | curated |", "|---|---|---|---|---|"]
for c in ["positive_le_examined", "pn_vs_positive_count", "her2_score_vs_status"]:
    L.append(f"| {c} | " + " | ".join(f"{K[m][c]['violations']}/{K[m][c]['n_both']}" for m in M + ["curated"]) + " |")
L += ["", "The curated values themselves are inconsistent with the score→status and count→pN rules in some patients (possible reasons: status recorded after a reflex test, micrometastases/ITC, IHC-only nodes; not investigated).", ""]
A = C["adjudication_sample"]
L += ["### How to read this", "",
      "- On several fields (histology, pT, pN, laterality, margin, HER2 IHC status) agreement *among answered cases* is similar for rules and the LLMs; there the LLM advantage is mainly **coverage**. See `results/results_tables.md` for the answered-agreement columns.",
      "- Receptor fields have low end-to-end agreement for every extractor because the status is often not in this OCR'd report at all (separate IHC report / addendum); see the `missing_in_report` tag counts in `test_results.json → error_tags`.",
      "- `margin_status` κ is low for all extractors: the curated field is mostly `negative`, and `close` vs `negative` is definitional.",
      f"- **Adjudication sample** (30 test disagreements, identical selection rule): [`results/adjudication_sample.md`](results/adjudication_sample.md) / `.csv` — **unreviewed**. "
      f"Relative to the superseded sample, {len(A['kept'])} items are kept, {len(A['added'])} added, {len(A['dropped'])} dropped (`replication_vs_superseded.json → adjudication_sample`). "
      "The agent pre-read of the superseded sample (`results/superseded_azure/adjudication_agent_preread.md`) is not an adjudication.", "",
      "### What was verified on the test run", "",
      f"- Extraction ran against frozen commit {cid(R['frozen_commit'])}; the runner refuses to run if `src/` or `protocol.json` changed since. Prompt, schema, rules, grounding and metrics are byte-identical to the v1.0 freeze {cid('1fb21c1')}.",
      "- Commit IDs in result files and docs are original IDs from before the pre-publication history rewrite; [`docs/commit-map.md`](docs/commit-map.md) maps them to this history, and `scripts/run_eval.py` resolves the recorded freeze through it.",
      f"- Finish reason `stop` for all calls (non-stop: gpt-4.1 {R['cost']['gpt-4.1']['finish_not_stop']}, gpt-4o {R['cost']['gpt-4o']['finish_not_stop']}); served model versions logged per response: "
      f"{', '.join(R['cost']['gpt-4.1']['deployment_models'] + R['cost']['gpt-4o']['deployment_models'])}.",
      "- An earlier replication attempt was blocked by `insufficient_quota` with zero responses (`docs/protocol.md`, Addendum 2 run log).", ""]
text = "\n".join(L)
readme = (ROOT / "README.md").read_text()
a = readme.index("## Results")
b = readme.index("## Limitations")
(ROOT / "README.md").write_text(readme[:a] + text + "\n" + readme[b:])
print(text)
