# pathology-report-extraction-lab

This is an independent clinical-NLP evaluation prototype built on public TCGA data. It was implemented by an AI coding agent under Lu Zhang's direction; see [`docs/ai-assisted-engineering.md`](docs/ai-assisted-engineering.md). It extracts a fixed 12-field schema from OCR'd TCGA breast-cancer (BRCA) pathology reports with two methods:

1. a **rules/regex baseline**
2. a **quote-grounded LLM extractor**: OpenAI API snapshots `gpt-4.1-2025-04-14` as the primary model and `gpt-4o-2024-11-20` as the secondary, both with strict JSON-schema output

Both extractors are scored against **curated TCGA clinical fields** under a protocol written down before the test set was used: a patient-level dev/test split, a one-shot held-out test, Cohen's kappa, and paired patient-bootstrap CIs.

> **Agreement, not accuracy.** The curated values come from TCGA clinical data forms, and those may draw on documents other than this OCR'd report (addenda, separate IHC/FISH reports, later surgery). A disagreement is therefore not necessarily an extractor error. A 30-item adjudication sample is provided for hand review. **It has not been reviewed yet**, so nothing here is "validated".

## Results (held-out test, 258 patients; OpenAI API replication, run once)

Provider: OpenAI API, pinned snapshots `gpt-4.1-2025-04-14` / `gpt-4o-2024-11-20`, frozen commit `e26bfcb` (`results/freeze.json`, protocol Addendum 2). These replace the superseded v1.0 run (same snapshots, prompt, schema, rules and analysis via a provisional Azure OpenAI endpoint), which is kept for comparison in `results/superseded_azure/`.

Full tables: [`results/results_tables.md`](results/results_tables.md); raw numbers: `results/test_results.json`; comparison with the superseded run: `results/replication_vs_superseded.json`.

Per-field **end-to-end agreement** with curated values (abstentions count as non-agreement) / **coverage** / **Cohen's κ** (over answered):

| field | n | rules | gpt-4.1 | gpt-4o |
|---|---|---|---|---|
| er_status | 247 | 0.364 / 0.409 / 0.734 | 0.571 / 0.575 / 0.982 | 0.559 / 0.563 / 0.981 |
| pr_status | 247 | 0.364 / 0.417 / 0.722 | 0.514 / 0.543 / 0.887 | 0.466 / 0.494 / 0.875 |
| her2_ihc_status | 219 | 0.215 / 0.251 / 0.670 | 0.361 / 0.425 / 0.721 | 0.429 / 0.498 / 0.731 |
| her2_ihc_score | 157 | 0.127 / 0.178 / 0.590 | 0.369 / 0.427 / 0.809 | 0.369 / 0.433 / 0.785 |
| her2_ish_status | 112 | 0.089 / 0.116 / 0.304 | 0.277 / 0.295 / 0.827 | 0.277 / 0.295 / 0.805 |
| histologic_type | 258 | 0.810 / 0.837 / 0.927 | 0.953 / 0.992 / 0.918 | 0.946 / 0.977 / 0.930 |
| pathologic_t | 258 | 0.581 / 0.616 / 0.897 | 0.674 / 0.713 / 0.902 | 0.674 / 0.713 / 0.902 |
| pathologic_n | 258 | 0.550 / 0.566 / 0.958 | 0.674 / 0.709 / 0.922 | 0.705 / 0.733 / 0.940 |
| laterality | 258 | 0.791 / 0.814 / 0.943 | 0.899 / 0.915 / 0.966 | 0.884 / 0.891 / 0.983 |
| margin_status | 247 | 0.543 / 0.611 / 0.300 | 0.672 / 0.781 / 0.287 | 0.619 / 0.761 / 0.254 |
| ln_examined | 224 | 0.246 / 0.513 / n/a | 0.696 / 0.821 / n/a | 0.661 / 0.790 / n/a |
| ln_positive | 219 | 0.402 / 0.511 / n/a | 0.758 / 0.840 / n/a | 0.731 / 0.804 / n/a |
| **macro, 10 categorical fields** | | **0.444** | **0.597** | **0.593** |
| macro, all 12 fields | | 0.424 | 0.618 | 0.610 |

**Primary comparison (prespecified):** macro end-to-end agreement over the **10 categorical fields**, gpt-4.1 − rules = **+0.153 (95% CI +0.134 to +0.173)**, paired patient bootstrap B = 2000 → *gpt-4.1 higher agreement*.
Secondary: gpt-4o − rules +0.149 (95% CI +0.128 to +0.172); gpt-4.1 − gpt-4o +0.004 (95% CI -0.007 to +0.014); gpt-4.1 − rules over all 12 fields +0.195 (95% CI +0.176 to +0.214).

**Replication vs superseded run.** Primary estimate +0.153 [+0.134, +0.173] vs superseded +0.156 [+0.136, +0.176]; same decision: True. Rules outputs identical: True. Grounded field outputs (status + value) identical between runs in 96.6% of gpt-4.1 cells and 95.7% of gpt-4o cells (temperature 0 is not bit-deterministic across providers/infrastructure).

**Abstention and grounding.** Of 3,096 field cells (258 × 12):

- rules: 1445 values claimed, 0 rejected by grounding (0.0% of claims: none), 1651 not_stated.
- gpt-4.1: 2075 values claimed, 106 rejected by grounding (5.1% of claims: quote_not_in_report 40, quote_lacks_field_cue 56, number_not_in_quote 10), 1021 not_stated.
- gpt-4o: 2128 values claimed, 178 rejected by grounding (8.4% of claims: quote_not_in_report 105, quote_lacks_field_cue 53, number_not_in_quote 20), 968 not_stated.
- Post hoc (`results/posthoc_rejections.json`): 92 of gpt-4.1's 106 rejected claims (gpt-4o: 140 of 178) had a claimed value equal to the curated value. The strict all-quotes-verbatim rule costs agreement; it is kept as prespecified. Grounding checks that a quote **exists** and mentions the field, not that it supports the value.

**Cost / latency (test, per report; API usage × list price, billing not checked).**

- gpt-4.1: mean 2454 input (of which 157 cached) + 327 output tokens, USD 0.0073/report (USD 1.88 for 258); latency mean 1.80 s / median 1.69 s / p95 2.78 s (2 workers).
- gpt-4o: mean 2454 input (of which 183 cached) + 333 output tokens, USD 0.0092/report (USD 2.38 for 258); latency mean 1.53 s / median 1.50 s / p95 2.15 s (2 workers).
- Spend on the OpenAI API for this replication: **USD 4.26** (cap 6). Superseded run (dev iteration + test + smoke): USD 5.67. Rules: 0.92 s for all 1,034 reports on CPU (`results/rules_timing.json`).

**Cross-field consistency checks** (violations / patients with both fields answered; checks, not relation extraction):

| check | rules | gpt-4.1 | gpt-4o | curated |
|---|---|---|---|---|
| positive_le_examined | 3/118 | 0/190 | 0/183 | 0/219 |
| pn_vs_positive_count | 7/76 | 5/138 | 3/138 | 15/217 |
| her2_score_vs_status | 6/22 | 1/74 | 2/95 | 12/154 |

The curated values themselves are inconsistent with the score→status and count→pN rules in some patients (possible reasons: status recorded after a reflex test, micrometastases/ITC, IHC-only nodes; not investigated).

### How to read this

- On several fields (histology, pT, pN, laterality, margin, HER2 IHC status) agreement *among answered cases* is similar for rules and the LLMs; there the LLM advantage is mainly **coverage**. See `results/results_tables.md` for the answered-agreement columns.
- Receptor fields have low end-to-end agreement for every extractor because the status is often not in this OCR'd report at all (separate IHC report / addendum); see the `missing_in_report` tag counts in `test_results.json → error_tags`.
- `margin_status` κ is low for all extractors: the curated field is mostly `negative`, and `close` vs `negative` is definitional.
- **Adjudication sample** (30 test disagreements, identical selection rule): [`results/adjudication_sample.md`](results/adjudication_sample.md) / `.csv` — **unreviewed**. Relative to the superseded sample, 18 items are kept, 12 added, 12 dropped (`replication_vs_superseded.json → adjudication_sample`). The agent pre-read of the superseded sample (`results/superseded_azure/adjudication_agent_preread.md`) is not an adjudication.

### What was verified on the test run

- Extraction ran against frozen commit `e26bfcb`; the runner refuses to run if `src/` or `protocol.json` changed since. Prompt, schema, rules, grounding and metrics are byte-identical to the v1.0 freeze `1fb21c1`.
- Finish reason `stop` for all calls (non-stop: gpt-4.1 0, gpt-4o 0); served model versions logged per response: gpt-4.1-2025-04-14, gpt-4o-2024-11-20.
- An earlier replication attempt was blocked by `insufficient_quota` with zero responses (`docs/protocol.md`, Addendum 2 run log).

## Limitations

- **Agreement ≠ accuracy**, and the adjudication sample is not yet reviewed. No claim of validated extraction performance.
- **Reference is imperfect and partly out-of-report:** curated TCGA fields can come from other documents; receptor/HER2 fields are often absent from the OCR'd report.
- **Template sharing:** the split is by patient, not tissue source site (39 sites); rules tuned on dev have seen the same templates as test. This favours the rules baseline; an LLM-vs-rules gap on unseen sites could be larger.
- **Run-to-run variability:** one temperature-0 run per model per provider. Across the superseded and replication runs (same snapshots), 96.6% (gpt-4.1) and 95.7% (gpt-4o) of grounded field outputs were identical, and the primary estimate moved by −0.003. Individual items can flip: the HER2 'POSITIVE (2+)' → equivocal prompt issue appears in 1 of the 2 superseded cases in the replication. Dev LLM iteration used only 80 patients and two prompt versions, on the superseded endpoint.
- **Grounding checks are lexical**: they prove the quote exists and mentions the field, not that it entails the value (see the HER2 2+ errors).
- **Error-source tags are heuristics**, not adjudications. Node counts summed across specimens are inherently hard to evidence with short quotes.
- **Cost** is list price × logged API usage; actual billing was not checked. Latency includes SDK retry back-off.
- Public, de-identified TCGA research data only; no PHI/EHR. Not a clinical tool.

## Not done

- Hand adjudication (prepared, awaiting Lu).
- Relation extraction proper (only cross-field consistency checks), knowledge graph, fine-tuning, a trained ML classifier baseline, site-grouped split, repeated LLM runs, prompt repair loop for rejected quotes.


## Design in one screen

- **Data:** 1,034 TCGA-BRCA patients, one OCR'd pathology report each, from TCGA-Reports (Kefeli & Tatonetti 2024, CC BY 4.0). The curated reference is the UCSC Xena `BRCA_clinicalMatrix` (TCGA BCR clinical data). URLs and a SHA-256 hash for each of the 4 source files are in `data/manifest.json`. The data are public and de-identified. They are not PHI and not EHR data.
- **Split:** patient-level and deterministic, by SHA-256 of the patient ID: 776 dev and 258 test patients (`data/membership.json`, re-derived in tests).
  - The rules were tuned on dev.
  - The LLM prompt was tuned on an 80-patient dev sample only (prompt v2 → v3).
  - The test set was extracted and scored once, after the freeze commit (`results/freeze.json`).
- **LLM workload:** the cohort is 1,034 reports, but only the rules ran on all of them. In the current (replication) run, gpt-4.1 and gpt-4o each processed the 258 test reports. Prompt iteration used gpt-4.1 on 80 dev reports in the superseded run, so gpt-4.1 has seen 338 reports in total (80 dev + 258 test).
- **Schema:** ER, PR, HER2 IHC status, HER2 IHC score, HER2 ISH status, histologic type, pT, pN, laterality, margin status, nodes examined, nodes positive. Every field allows an explicit `not_stated`. The curated-value mapping is in `docs/protocol.md` and `src/prel/schema.py`.
- **Grounding (both extractors):** every value must cite at least one quote. The code locates each quote in the report and computes the character offsets itself. The match must be exact, or exact after collapsing whitespace, with no fuzzy matching. The quote must also contain a field keyword (cue regex) and, for a single-quote count, the number. This checks that the quote **exists** in the report and mentions the field. It does **not** check that the quote supports the specific value. A failure becomes a *rejected* abstention, which is reported separately from `not_stated`.
- **Primary metric:** per field, end-to-end agreement = agreeing answers / patients with a curated value. Abstentions count against the extractor, so abstaining cannot inflate the score. Agreement among answered patients, coverage and kappa are reported next to it.
- **Primary comparison:** macro end-to-end agreement over the 10 categorical fields, gpt-4.1 minus rules, with a paired patient bootstrap (B = 2000) for the 95% CI.
- **Cross-field consistency checks** (not relation extraction): positive nodes ≤ examined nodes, pN vs the positive-node-count bucket, and HER2 IHC score vs status.

## Reproduce

```bash
uv sync
uv run python scripts/build_data.py        # copy/download + verify inputs, build cohort + split
uv run pytest -q                           # unit tests
uv run python scripts/run_eval.py dev      # dev tables (LLM part reads the cache)
uv run python scripts/run_eval.py test     # one-shot test run (needs OPENAI_API_KEY; see results/llm_spend.json for measured cost)
uv run python scripts/make_report.py       # results/results_tables.md
uv run python scripts/spend.py             # results/llm_spend.json
uv run python scripts/posthoc.py           # results/posthoc_rejections.json (post hoc)
uv run python scripts/compare_superseded.py  # results/replication_vs_superseded.json
uv run python scripts/render_readme_results.py  # regenerate this README's results section
```

**LLM access.** The current results call the official OpenAI API (`https://api.openai.com/v1`, fixed in code) with `OPENAI_API_KEY` from the environment, using pinned snapshots `gpt-4.1-2025-04-14` and `gpt-4o-2024-11-20`, temperature 0, seed 0. Every response is cached in `results/cache/llm_cache.jsonl` (gitignored: it contains report text). An earlier run used the same snapshots through a provisional Azure OpenAI endpoint; it is superseded and kept only for comparison in `results/superseded_azure/` (see `docs/protocol.md`, Addendum 2). See `.env.example`.

## Layout

```
src/prel/schema.py      fields, curated-value mapping, grounding cues
src/prel/grounding.py   quote location + support checks
src/prel/rules.py       regex baseline
src/prel/llm.py         prompt, strict JSON schema, OpenAI client (pinned snapshots), cache, cost
src/prel/metrics.py     agreement, kappa, paired bootstrap
src/prel/analysis.py    consistency checks, cost summary, error tags, adjudication sample
scripts/                build_data, dev_rules, dev_llm, dev_errors, run_eval, make_report, spend, posthoc,
                        compare_superseded, render_readme_results
results/                dev_results.json, freeze.json, test_results.json, results_tables.md,
                        adjudication_sample.{md,csv}, llm_spend.json, replication_vs_superseded.json,
                        superseded_azure/ (superseded v1.0 run, comparison only)
docs/                   protocol.md (prespecified), ai-assisted-engineering.md
```

## License and attribution

Code: MIT (`LICENSE`). Data attribution: [`THIRD_PARTY.md`](THIRD_PARTY.md). The results are based on data generated by the TCGA Research Network. This is research and education only, not a clinical tool.
