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
- **Provenance:** URLs and SHA-256 hashes for every input are in `data/manifest.json`.

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
   - Deployments: gpt-4.1 (`gpt-4.1-2025-04-14`) and gpt-4o (`gpt-4o-2024-11-20`), on a personal Azure OpenAI resource.
   - Prompt v3; temperature 0, seed 0.
   - Strict JSON-schema structured output: each field has an enum or integer value plus 1–3 verbatim quotes.
   - The prompt forbids inference: no pT from tumor size, no pN from node counts, and clinical (history) staging is ignored.
   - Auth uses a short-lived Azure CLI token with the subscription passed explicitly. No API key is used.

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

- Total LLM spend must stay under USD 10.
- gpt-4.1 runs on the 80-patient dev sample and on all 258 test reports. gpt-4o runs on the 258 test reports only.
- Prices (USD per 1M input/output tokens, Azure list prices, actual billing not checked): gpt-4.1 2.00/8.00, gpt-4o 2.50/10.00.
- All responses are cached in `results/cache/llm_cache.jsonl` (gitignored, since it contains report-derived text).

## Addenda

### Addendum 1 — 2026-11-20 (after the test run; no change to the prespecified analysis)

- **Failed calls.** The first test attempt stopped after the gpt-4.1 pass because 7 calls still returned HTTP 429 after 8 SDK retries (`results/test_run_attempt1.log`). As prespecified ("a report whose call still fails is re-run until success"), the runner was re-executed unchanged; it served the 251 cached gpt-4.1 responses from cache, made the 7 missing calls, then ran gpt-4o. No code, prompt or protocol change.
- **Post hoc analyses (labelled as such, not prespecified):** `scripts/posthoc.py` → `results/posthoc_rejections.json` (claimed value of grounding-rejected fields vs curated value) and `results/adjudication_agent_preread.md` (agent's tentative read of the 30 adjudication items; not an adjudication).
