# pathology-report-extraction-lab

This is a personal clinical-NLP evaluation prototype built on public TCGA data. It extracts a fixed 12-field schema from OCR'd TCGA breast-cancer (BRCA) pathology reports with two methods:

1. a **rules/regex baseline**
2. a **quote-grounded LLM extractor**: Azure OpenAI gpt-4.1 as the primary model and gpt-4o as the secondary, both with strict JSON-schema output

Both extractors are scored against **curated TCGA clinical fields** under a protocol written down before the test set was used: a patient-level dev/test split, a one-shot held-out test, Cohen's kappa, and paired patient-bootstrap CIs.

> **Agreement, not accuracy.** The curated values come from TCGA clinical data forms, and those may draw on documents other than this OCR'd report (addenda, separate IHC/FISH reports, later surgery). A disagreement is therefore not necessarily an extractor error. A 30-item adjudication sample is provided for hand review. **It has not been reviewed yet**, so nothing here is "validated".

## Results (held-out test, 258 patients, run once)

Full tables: [`results/results_tables.md`](results/results_tables.md); raw numbers: `results/test_results.json`.

Per-field **end-to-end agreement** with curated values (abstentions count as non-agreement), **coverage** (answered / curated-available) and **Cohen's κ** (over answered):

| field | n | rules e2e / cov / κ | gpt-4.1 e2e / cov / κ | gpt-4o e2e / cov / κ |
|---|---|---|---|---|
| er_status | 247 | 0.364 / 0.409 / 0.734 | 0.567 / 0.571 / 0.982 | 0.567 / 0.571 / 0.981 |
| pr_status | 247 | 0.364 / 0.417 / 0.722 | 0.514 / 0.538 / 0.902 | 0.494 / 0.522 / 0.881 |
| her2_ihc_status | 219 | 0.215 / 0.251 / 0.670 | 0.374 / 0.438 / 0.719 | 0.438 / 0.502 / 0.748 |
| her2_ihc_score | 157 | 0.127 / 0.178 / 0.590 | 0.369 / 0.427 / 0.809 | 0.376 / 0.439 / 0.790 |
| her2_ish_status | 112 | 0.089 / 0.116 / 0.304 | 0.268 / 0.286 / 0.826 | 0.277 / 0.295 / 0.805 |
| histologic_type | 258 | 0.810 / 0.837 / 0.927 | 0.950 / 0.988 / 0.917 | 0.950 / 0.984 / 0.925 |
| pathologic_t | 258 | 0.581 / 0.616 / 0.897 | 0.671 / 0.713 / 0.893 | 0.674 / 0.713 / 0.902 |
| pathologic_n | 258 | 0.550 / 0.566 / 0.958 | 0.702 / 0.736 / 0.924 | 0.721 / 0.756 / 0.925 |
| laterality | 258 | 0.791 / 0.814 / 0.943 | 0.899 / 0.919 / 0.958 | 0.888 / 0.899 / 0.974 |
| margin_status | 247 | 0.543 / 0.611 / 0.300 | 0.680 / 0.789 / 0.288 | 0.611 / 0.785 / 0.206 |
| ln_examined | 224 | 0.246 / 0.513 / n/a | 0.661 / 0.812 / n/a | 0.652 / 0.808 / n/a |
| ln_positive | 219 | 0.402 / 0.511 / n/a | 0.726 / 0.826 / n/a | 0.726 / 0.817 / n/a |
| **macro (10 categorical)** | | **0.444** | **0.599** | **0.600** |
| macro (all 12) | | 0.424 | 0.615 | 0.614 |

**Primary comparison (prespecified):** macro end-to-end agreement over the 10 categorical fields, gpt-4.1 − rules = **+0.156 (95% CI +0.136 to +0.176)**, paired patient bootstrap B = 2000 → *gpt-4.1 higher agreement*.
Secondary: gpt-4o − rules +0.156 (95% CI +0.135 to +0.178); gpt-4.1 − gpt-4o -0.000 (95% CI -0.011 to +0.009) (no detectable difference between the two LLMs).

**Abstention and grounding.** Of 3,096 field cells (258 × 12):

- rules: 1445 values claimed, 0 rejected by grounding (0.0% of claims: none), 1651 not_stated.
- gpt-4.1: 2081 values claimed, 103 rejected by grounding (4.9% of claims: quote_lacks_field_cue 50, quote_not_in_report 42, number_not_in_quote 11), 1015 not_stated.
- gpt-4o: 2138 values claimed, 149 rejected by grounding (7.0% of claims: quote_not_in_report 66, number_not_in_quote 26, quote_lacks_field_cue 57), 958 not_stated.
- Post hoc (not prespecified, `results/posthoc_rejections.json`): 89 of gpt-4.1's 103 rejected claims (gpt-4o: 127 of 149) had a claimed value equal to the curated value — the strict all-quotes-verbatim rule costs agreement; it was kept as prespecified.

**Cost / latency (test, per report).**

- gpt-4.1: mean 2454 input + 331 output tokens, USD 0.0076/report (USD 1.95 for 258), latency mean 4.32 s / median 3.10 s / p95 10.79 s (2 workers, includes HTTP-429 back-off).
- gpt-4o: mean 2454 input + 334 output tokens, USD 0.0095/report (USD 2.44 for 258), latency mean 2.38 s / median 2.24 s / p95 3.39 s (2 workers, includes HTTP-429 back-off).
- Total LLM spend for the whole project (dev iteration + test, list prices × logged tokens): **USD 5.67** (`results/llm_spend.json`). Rules: < 1 s for all 1,034 reports on CPU.

**Cross-field consistency checks** (violations / patients with both fields answered; these are checks, not relation extraction):

| check | rules | gpt-4.1 | gpt-4o | curated |
|---|---|---|---|---|
| positive_le_examined | 3/118 | 0/189 | 0/189 | 0/219 |
| pn_vs_positive_count | 7/76 | 5/143 | 9/148 | 15/217 |
| her2_score_vs_status | 6/22 | 0/81 | 3/97 | 12/154 |

The curated values themselves violate the score→status and count→pN checks in some patients (possible reasons include status recorded after a reflex test, micrometastases/ITC and IHC-only nodes; not investigated), which is one more reason to read disagreement as *disagreement*.

### How to read this

- For histology, pT, pN, laterality, margin and HER2 IHC status, agreement *among answered cases* is similar for rules and gpt-4.1 (within about 0.03, e.g. pT 0.943 vs 0.940); there the LLM's advantage is mainly **coverage** (it answers more often while staying grounded). For ER/PR, HER2 score, HER2 ISH and node counts the LLM is also more often in agreement when it answers (e.g. `ln_examined` 0.478 rules vs 0.813 gpt-4.1, where the rules' sum heuristic double-counts).
- Receptor fields have low end-to-end agreement for *every* extractor (ER at most 0.567) because the status is often not in this OCR'd report at all (separate IHC report / addendum). 390 curated-available (patient, field) cells have no field cue anywhere in the report text (automatic tag `missing_in_report`, `test_results.json → error_tags`).
- `margin_status` κ is low (≈ 0.2–0.3) for all extractors: the curated field is mostly `negative`, and `close` vs `negative` is definitional.
- **Adjudication sample** (30 test disagreements, stratified by field): [`results/adjudication_sample.md`](results/adjudication_sample.md) / `.csv` — **unreviewed**. An agent pre-read (explicitly *not* an adjudication) is in [`results/adjudication_agent_preread.md`](results/adjudication_agent_preread.md): it tentatively attributes ~11 of 30 to the curated value disagreeing with what this report states, 8–9 to rules errors, 3–4 to gpt-4.1 (two prompt-induced HER2 'POSITIVE (2+)' → equivocal errors, one grounding rejection of a correct value), and ~7 to ambiguity/definitions. Until Lu reviews it, none of this is validated.

### What was verified on the test run

- Test extraction ran against the frozen commit `1fb21c1` (`results/freeze.json`); the runner refuses to run if `src/` or `protocol.json` changed since.
- The first test attempt stopped after gpt-4.1 because 7 calls still hit HTTP 429 after retries (`results/test_run_attempt1.log`); per the prespecified failed-call rule the run was re-executed, which only filled the 7 missing calls (all others came from cache). All 516 test calls finished with `finish_reason = stop`.
- Deployment model versions were logged per response: `gpt-4.1-2025-04-14`, `gpt-4o-2024-11-20`.

## Limitations

- **Agreement ≠ accuracy**, and the adjudication sample is not yet reviewed. No claim of validated extraction performance.
- **Reference is imperfect and partly out-of-report:** curated TCGA fields can come from other documents; receptor/HER2 fields are often absent from the OCR'd report.
- **Template sharing:** the split is by patient, not tissue source site (39 sites); rules tuned on dev have seen the same templates as test. This favours the rules baseline; an LLM-vs-rules gap on unseen sites could be larger.
- **Single run** per model at temperature 0; run-to-run variance not measured. Dev LLM iteration used only 80 patients and two prompt versions.
- **Grounding checks are lexical**: they prove the quote exists and mentions the field, not that it entails the value (see the HER2 2+ errors).
- **Error-source tags are heuristics**, not adjudications. Node counts summed across specimens are inherently hard to evidence with short quotes.
- **Cost** is list price × logged tokens; actual Azure billing was not checked. Latency includes rate-limit back-off on a low-quota personal deployment.
- Public, de-identified TCGA research data only; no PHI/EHR. Not a clinical tool.

## Not done

- Hand adjudication (prepared, awaiting Lu).
- Relation extraction proper (only cross-field consistency checks), knowledge graph, fine-tuning, a trained ML classifier baseline, site-grouped split, repeated LLM runs, prompt repair loop for rejected quotes.


## Design in one screen

- **Data:** 1,034 TCGA-BRCA patients, one OCR'd pathology report each, from TCGA-Reports (Kefeli & Tatonetti 2024, CC BY 4.0). The curated reference is the UCSC Xena `BRCA_clinicalMatrix` (TCGA BCR clinical data). URLs and SHA-256 hashes are in `data/manifest.json`. The data are public and de-identified. They are not PHI and not EHR data.
- **Split:** patient-level and deterministic, by SHA-256 of the patient ID: 776 dev and 258 test patients (`data/membership.json`, re-derived in tests).
  - The rules were tuned on dev.
  - The LLM prompt was tuned on an 80-patient dev sample only (prompt v2 → v3).
  - The test set was extracted and scored once, after the freeze commit (`results/freeze.json`).
- **Schema:** ER, PR, HER2 IHC status, HER2 IHC score, HER2 ISH status, histologic type, pT, pN, laterality, margin status, nodes examined, nodes positive. Every field allows an explicit `not_stated`. The curated-value mapping is in `docs/protocol.md` and `src/prel/schema.py`.
- **Grounding (both extractors):** every value must cite at least one quote. The code itself locates the quote in the report and computes the character offsets. The match must be exact, or exact after collapsing whitespace, with no fuzzy matching. The quote must also contain a field cue and, for counts, the number. A failure becomes a *rejected* abstention, which is reported separately from `not_stated`.
- **Primary metric:** per field, end-to-end agreement = agreeing answers / patients with a curated value. Abstentions count against the extractor, so abstaining cannot inflate the score. Agreement among answered patients, coverage and kappa are reported next to it.
- **Primary comparison:** macro end-to-end agreement over the 10 categorical fields, gpt-4.1 minus rules, with a paired patient bootstrap (B = 2000) for the 95% CI.
- **Cross-field consistency checks** (not relation extraction): positive nodes ≤ examined nodes, pN vs the positive-node-count bucket, and HER2 IHC score vs status.

## Reproduce

```bash
uv sync
uv run python scripts/build_data.py        # copy/download + verify inputs, build cohort + split
uv run pytest -q                           # unit tests
uv run python scripts/run_eval.py dev      # dev tables (LLM part reads the cache)
uv run python scripts/run_eval.py test     # one-shot test run (needs Azure CLI login; ~USD 4.6 uncached)
uv run python scripts/make_report.py       # results/results_tables.md
uv run python scripts/spend.py             # results/llm_spend.json
```

**LLM access.** The model is a personal Azure OpenAI deployment. Calls use a short-lived token from `az account get-access-token`, with the subscription passed explicitly, and no API key is read. Ambient `OPENAI_API_KEY` / `AZURE_OPENAI_API_KEY` values are removed from the process environment. Settings are temperature 0 and seed 0. Every response is cached in `results/cache/llm_cache.jsonl`, which is gitignored because it contains report text. See `.env.example`.

## Layout

```
src/prel/schema.py      fields, curated-value mapping, grounding cues
src/prel/grounding.py   quote location + support checks
src/prel/rules.py       regex baseline
src/prel/llm.py         prompt, strict JSON schema, keyless Azure client, cache, cost
src/prel/metrics.py     agreement, kappa, paired bootstrap
src/prel/analysis.py    consistency checks, cost summary, error tags, adjudication sample
scripts/                build_data, dev_rules, dev_llm, dev_errors, run_eval, make_report, spend
results/                dev_results.json, freeze.json, test_results.json, results_tables.md,
                        adjudication_sample.{md,csv}, llm_spend.json
docs/                   protocol.md (prespecified), ai-assisted-engineering.md
```

## License and attribution

Code: MIT (`LICENSE`). Data attribution: [`THIRD_PARTY.md`](THIRD_PARTY.md). The results are based on data generated by the TCGA Research Network. This is research and education only, not a clinical tool.
