# Prespecified evaluation protocol

Version 1.0, 2026-11-20. Machine-readable copy: [`protocol.json`](../protocol.json).

This protocol was committed **before** any test-set extraction or evaluation. The commit used for the single test run is recorded in `results/freeze.json`. Any later change goes in a dated addendum at the end of this file.

## Question

How well do two extractors agree with curated TCGA clinical fields when they extract a fixed schema from OCR'd TCGA-BRCA pathology reports? The extractors are (1) a rules/regex baseline and (2) a quote-grounded LLM.

**This is agreement, not accuracy.** The curated values come from the TCGA clinical data forms, and those may draw on documents other than this OCR'd report: addenda, separate IHC/FISH reports, outside consults, or later surgery. A disagreement can therefore be an extractor error, a curated-value error, or simply information that is missing from this report. Only hand adjudication can tell these apart (see "Adjudication").

## Data and cohort

- **Reports:** TCGA-Reports (Kefeli & Tatonetti 2024). Machine-readable OCR text of the TCGA pathology-report PDFs, one report per patient, BRCA subset. The data are public and de-identified. They are not EHR data.
- **Curated reference:** the UCSC Xena `TCGA.BRCA.sampleMap/BRCA_clinicalMatrix` (TCGA BCR clinical data). It is sample-keyed. The curated columns used here were asserted identical across each patient's sample rows, and one row per patient was kept.
- **Cohort:** 1,034 BRCA patients. All of them have both a report and a clinical row.
- **Provenance:** URLs and a SHA-256 hash for each source file (4 files) are in `data/manifest.json`.

## Split

- Unique patient IDs are sorted by `SHA256(patient_id|pathology-extraction-v1)`. The first `round(0.25·n)` are **test** (258), and the rest are **dev** (776). No outcome or label is read.
- The membership is committed in `data/membership.json` and re-derived in a test.
- The **LLM dev sample** is the first 80 dev patients sorted by `SHA256(patient_id|pathology-extraction-llm-dev-v1)`. It is the only dev data the LLM has seen.
- Rules were iterated on all 776 dev reports. The LLM prompt was iterated on the 80-patient dev sample (two prompt versions, v2 → v3). The test set was not looked at.
- **Known limitation: template sharing.** Reports from the same tissue source site share templates, and the split is not grouped by site. Dev-tuned regexes have therefore effectively seen the test templates. This favors the rules baseline.

## Schema (12 fields)

Each field takes a value or `not_stated`, and every value must cite evidence.

| field | values | curated column |
|---|---|---|
| er_status, pr_status | positive / negative | breast_carcinoma_{estrogen,progesterone}_receptor_status |
| her2_ihc_status | positive / equivocal / negative | lab_proc_her2_neu_immunohistochemistry_receptor_status |
| her2_ihc_score | 0 / 1+ / 2+ / 3+ | her2_immunohistochemistry_level_result |
| her2_ish_status | amplified / equivocal / not_amplified | lab_procedure_her2_neu_in_situ_hybrid_outcome_type |
| histologic_type | ductal / lobular / mixed_ductal_lobular / mucinous / other | histological_type (+ histological_type_other) |
| pathologic_t | T1–T4 / TX | pathologic_T (main category) |
| pathologic_n | N0–N3 / NX | pathologic_N (main category) |
| laterality | left / right | anatomic_neoplasm_subdivision (Left/Right prefix) |
| margin_status | negative / close / positive | margin_status |
| ln_examined | integer | lymph_node_examined_count |
| ln_positive | integer | number_of_lymphnodes_positive_by_he |

Mapping details:
- Indeterminate, `[Not Available]`, bilateral and missing curated values are excluded from that field.
- HER2 IHC and ISH stay separate fields. No combined HER2 call is invented.
- The full mapping is in `protocol.json` and `src/prel/schema.py`.

## Extractors

1. **Rules** (`src/prel/rules.py`): regular expressions with first-match, majority-vote or sum heuristics. The evidence is the exact matched substring.
2. **LLM** (`src/prel/llm.py`), with gpt-4.1 as the primary model and gpt-4o as the secondary.
   - Models: pinned snapshots `gpt-4.1-2025-04-14` and `gpt-4o-2024-11-20`. Provider: the OpenAI API, from Addendum 2 on. The original v1.0 runs used a provisional Azure OpenAI endpoint serving the same snapshots; they are superseded.
   - Prompt v3; temperature 0, seed 0.
   - Strict JSON-schema structured output: each field has an enum or integer value plus a list of quotes. The prompt asks for 1–3 verbatim quotes. The schema does not enforce the count, and an empty list for a non-`not_stated` value is caught by grounding as `no_quote`.
   - The prompt forbids inference: no pT from tumor size, no pN from node counts, and clinical (history) staging is ignored.
   - Auth (from Addendum 2): `OPENAI_API_KEY` from the environment, with the base URL `https://api.openai.com/v1` passed explicitly.

## Grounding (applies to both extractors)

1. Every non-`not_stated` value needs at least one quote.
2. Each quote must occur in the report text **exactly**, or exactly after collapsing whitespace runs to a single space. There is no case folding, no fuzzy matching and no OCR correction. Character offsets are computed by the code, not by the model.
3. At least one quote must match a field-specific cue regex. For example, an ER quote must mention estrogen/ER.
4. For count fields, the number must appear in the quote as digits or a number word, unless several quotes are summed.
5. A failure replaces the value with an abstention marked **rejected**, which is reported separately from `not_stated`.

## Metrics

Per field, over the patients whose curated value is available:

- **agreement_e2e**, the primary per-field metric: agreeing answers / eligible patients. `not_stated` and rejected both count as non-agreement, so an extractor cannot inflate agreement by abstaining.
- **agreement_answered** together with **coverage** (answered / eligible), plus the not_stated and rejected counts.
- **Cohen's kappa** (unweighted), curated vs extracted, over answered patients. Categorical fields only.
- Count fields use exact match; within ±1 is reported descriptively.
- **Macro** = the unweighted mean of per-field agreement_e2e.

### Primary comparison (one)

- **Estimand:** macro agreement_e2e over the 10 categorical fields, **gpt-4.1 minus rules**, on the test set.
- **CI:** paired patient bootstrap, with test patients resampled with replacement (B = 2000, seed 20261120, percentile 95% CI).
- **Decision:** if the CI is entirely above 0, gpt-4.1 has higher agreement. If it is entirely below 0, gpt-4.1 has lower agreement. Otherwise the result is inconclusive.

### Secondary (descriptive)

- gpt-4o − rules
- gpt-4.1 − gpt-4o
- macro over all 12 fields
- per-field paired-bootstrap CIs (no multiplicity correction)
- cost, latency and tokens per report

## Cross-field consistency checks

These are consistency checks, not relation extraction. Violation rates are computed among patients where both fields are answered, for each extractor and for the curated values:

- `ln_positive ≤ ln_examined`
- `pathologic_n` equals the AJCC bucket of `ln_positive` (0→N0, 1–3→N1, 4–9→N2, ≥10→N3), excluding NX. Legitimate exceptions exist: micrometastases/ITC, IHC-only nodes, internal mammary nodes and the neoadjuvant setting.
- HER2 IHC score → status (0/1+ negative, 2+ equivocal, 3+ positive).

## Adjudication

- **Sample:** 30 test (patient, field) pairs where gpt-4.1 or rules answered a value that differs from the curated value. Sampling is round-robin over fields, shuffled within field (seed 20261120).
- **Shown side by side:** curated value, the rules / gpt-4.1 / gpt-4o values with their quotes, and the report context.
- **Files:** `results/adjudication_sample.{md,csv}`.
- It is **unreviewed** until Lu completes it. No result is called "validated" before then.

## Error sources

Every test disagreement gets automatic heuristic tags:

- `missing_in_report`
- `multiple_specimens_or_sides`
- `ocr_noise_in_evidence`
- `extractors_conflict`
- `curated_vs_report_conflict`

The tags are not adjudicated.

## Budget

- v1.0: total LLM spend under USD 10. gpt-4.1 ran on the 80-patient dev sample and on all 258 test reports; gpt-4o ran on the 258 test reports only.
- Addendum 2 replication: a cap of USD 6 on the OpenAI API key, covering test reports only (2 × 258 calls).
- Prices (USD per 1M tokens, list prices, actual billing not checked): gpt-4.1 2.00 input / 0.50 cached input / 8.00 output; gpt-4o 2.50 / 1.25 / 10.00.
- All responses are cached in `results/cache/llm_cache.jsonl` (gitignored, since it contains report-derived text).

## Addenda

### Addendum 1 — 2026-11-20 (after the test run; no change to the prespecified analysis)

- **Failed calls.** The first test attempt stopped after the gpt-4.1 pass because 7 calls still returned HTTP 429 after 8 SDK retries (`results/test_run_attempt1.log`). As prespecified ("a report whose call still fails is re-run until success"), the runner was re-executed unchanged; it served the 251 cached gpt-4.1 responses from cache, made the 7 missing calls, then ran gpt-4o. No code, prompt or protocol change.
- **Error-tag vocabulary.** Between the protocol commit (`3ee8e84`) and the freeze (`1fb21c1`), `src/prel/analysis.py` added two tags not listed in `protocol.json`: `not_extracted_by_any` (field cue present in the report but no extractor answered) and `untagged` (no heuristic fired). Both were added before any test-set call.
- **Post hoc analyses (labelled as such, not prespecified):** `scripts/posthoc.py` → `results/posthoc_rejections.json` (claimed value of grounding-rejected fields vs curated value) and `results/adjudication_agent_preread.md` (agent's tentative read of the 30 adjudication items; not an adjudication).

### Addendum 2 — 2026-11-20 (written and committed before the replication run)

- **Why.** The v1.0 LLM runs used a provisional Azure OpenAI endpoint that is no longer used. Earlier text called it "personal"; that was inaccurate and has been removed. That endpoint must no longer be used.
- **Change.** The provider is now the official OpenAI API (`https://api.openai.com/v1`), authenticated with `OPENAI_API_KEY` from the project owner's OpenAI account. The pinned model snapshots are the same as the superseded deployments: `gpt-4.1-2025-04-14` and `gpt-4o-2024-11-20`.
- **Frozen, unchanged:**
  - prompt v3 (`SYSTEM_PROMPT` text identical)
  - JSON schema, strict mode, temperature 0, seed 0, max_tokens 3000
  - rules baseline, grounding rule, curated mapping, split, metrics, primary estimand, bootstrap settings, consistency checks, adjudication selection rule (seed 20261120)
  - No prompt or rule changes. The known HER2 "POSITIVE (2+)" → equivocal prompt issue stays as a documented limitation.
- **Code changes, limited to the provider layer** (`src/prel/llm.py`, `src/prel/analysis.py` cost summary, budget arguments):
  - OpenAI client; the hard-coded Azure endpoint and subscription defaults are removed
  - provider and snapshot added to the cache key
  - cached-input tokens logged from `usage.prompt_tokens_details`, with cost at the cached-input rate
  - USD 6 budget cap with an in-run stop
- **What is re-run.** Rules (deterministic) and both LLM arms on the 258 held-out test reports, once, against the new freeze commit recorded in `results/freeze.json`. Dev LLM iteration (prompt v2 → v3 on 80 dev reports) happened on the superseded endpoint and is not repeated; the prompt is frozen.
- **Status of the old results.** The v1.0 test results are moved to `results/superseded_azure/` and kept only for comparison. The headline results are the replication. Agreement between the two runs will be reported in `results/replication_vs_superseded.json`: primary estimate, and field-level identity of extracted values per model.
- **Adjudication sample.** Regenerated with the identical selection rule. Items that changed relative to the superseded sample are listed.
