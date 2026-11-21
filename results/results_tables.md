# Held-out test results (n = 258 patients, frozen commit `e26bfcb`, LLM provider: openai)

Agreement with curated TCGA clinical fields, **not accuracy**. e2e = agreeing answers / patients with a curated value
(not_stated and grounding rejections count as non-agreement). ans = agreement among answered. κ = Cohen's kappa over answered.

## Per-field agreement

| field | n curated | rules cov | rules e2e | rules ans | rules κ | gpt-4.1 cov | gpt-4.1 e2e | gpt-4.1 ans | gpt-4.1 κ | gpt-4o cov | gpt-4o e2e | gpt-4o ans | gpt-4o κ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| er_status | 247 | 0.409 | 0.364 | 0.891 | 0.734 | 0.575 | 0.571 | 0.993 | 0.982 | 0.563 | 0.559 | 0.993 | 0.981 |
| pr_status | 247 | 0.417 | 0.364 | 0.874 | 0.722 | 0.543 | 0.514 | 0.948 | 0.887 | 0.494 | 0.466 | 0.943 | 0.875 |
| her2_ihc_status | 219 | 0.251 | 0.215 | 0.855 | 0.670 | 0.425 | 0.361 | 0.849 | 0.721 | 0.498 | 0.429 | 0.862 | 0.731 |
| her2_ihc_score | 157 | 0.178 | 0.127 | 0.714 | 0.590 | 0.427 | 0.369 | 0.866 | 0.809 | 0.433 | 0.369 | 0.853 | 0.785 |
| her2_ish_status | 112 | 0.116 | 0.089 | 0.769 | 0.304 | 0.295 | 0.277 | 0.939 | 0.827 | 0.295 | 0.277 | 0.939 | 0.805 |
| histologic_type | 258 | 0.837 | 0.810 | 0.968 | 0.927 | 0.992 | 0.953 | 0.961 | 0.918 | 0.977 | 0.946 | 0.968 | 0.930 |
| pathologic_t | 258 | 0.616 | 0.581 | 0.943 | 0.897 | 0.713 | 0.674 | 0.946 | 0.902 | 0.713 | 0.674 | 0.946 | 0.902 |
| pathologic_n | 258 | 0.566 | 0.550 | 0.973 | 0.958 | 0.709 | 0.674 | 0.951 | 0.922 | 0.733 | 0.705 | 0.963 | 0.940 |
| laterality | 258 | 0.814 | 0.791 | 0.971 | 0.943 | 0.915 | 0.899 | 0.983 | 0.966 | 0.891 | 0.884 | 0.991 | 0.983 |
| margin_status | 247 | 0.611 | 0.543 | 0.887 | 0.300 | 0.781 | 0.672 | 0.860 | 0.287 | 0.761 | 0.619 | 0.814 | 0.254 |
| ln_examined | 224 | 0.513 | 0.246 | 0.478 | n/a | 0.821 | 0.696 | 0.848 | n/a | 0.790 | 0.661 | 0.836 | n/a |
| ln_positive | 219 | 0.511 | 0.402 | 0.786 | n/a | 0.840 | 0.758 | 0.902 | n/a | 0.804 | 0.731 | 0.909 | n/a |
| **macro, 10 categorical** | |  | 0.444 | |  |  | 0.597 | |  |  | 0.593 | |  |
| **macro, all 12** | |  | 0.424 | |  |  | 0.618 | |  |  | 0.610 | |  |

## Primary comparison (prespecified)

- macro agreement_e2e over the 10 categorical fields, gpt-4.1 minus rules, test set: **+0.153 [+0.134, +0.173]** (paired patient bootstrap, B = 2000, seed 20261120); gpt-4.1 0.597 vs rules 0.444. Decision: **gpt-4.1 higher agreement**.
- gpt-4o − rules (10 categorical): +0.149 [+0.128, +0.172]
- gpt-4.1 − gpt-4o (10 categorical): +0.004 [-0.007, +0.014]
- gpt-4.1 − rules (all 12): +0.195 [+0.176, +0.214]; gpt-4o − rules (all 12): +0.186 [+0.167, +0.207]

Per-field e2e difference vs rules (descriptive, no multiplicity correction):

| field | gpt-4.1 − rules [95% CI] | gpt-4o − rules [95% CI] |
|---|---|---|
| er_status | +0.206 [+0.158, +0.259] | +0.194 [+0.142, +0.247] |
| pr_status | +0.150 [+0.101, +0.202] | +0.101 [+0.049, +0.158] |
| her2_ihc_status | +0.146 [+0.078, +0.215] | +0.215 [+0.155, +0.274] |
| her2_ihc_score | +0.242 [+0.172, +0.312] | +0.242 [+0.172, +0.312] |
| her2_ish_status | +0.188 [+0.116, +0.259] | +0.188 [+0.116, +0.259] |
| histologic_type | +0.143 [+0.097, +0.194] | +0.136 [+0.085, +0.186] |
| pathologic_t | +0.093 [+0.058, +0.132] | +0.093 [+0.054, +0.132] |
| pathologic_n | +0.124 [+0.074, +0.171] | +0.155 [+0.097, +0.209] |
| laterality | +0.109 [+0.070, +0.155] | +0.093 [+0.047, +0.143] |
| margin_status | +0.130 [+0.077, +0.186] | +0.077 [+0.020, +0.138] |
| ln_examined | +0.451 [+0.388, +0.518] | +0.415 [+0.348, +0.478] |
| ln_positive | +0.356 [+0.283, +0.425] | +0.329 [+0.256, +0.397] |

## Abstention and grounding

| extractor | field cells | claimed values | grounding rejections | rejection rate of claims | not_stated | rejection reasons |
|---|---|---|---|---|---|---|
| rules | 3096 | 1445 | 0 | 0.000 | 1651 | {} |
| gpt-4.1 | 3096 | 2075 | 106 | 0.051 | 1021 | {"quote_not_in_report": 40, "quote_lacks_field_cue": 56, "number_not_in_quote": 10} |
| gpt-4o | 3096 | 2128 | 178 | 0.084 | 968 | {"quote_not_in_report": 105, "quote_lacks_field_cue": 53, "number_not_in_quote": 20} |

## Cross-field consistency checks (violations / patients with both fields answered)

| check | rules | gpt-4.1 | gpt-4o | curated |
|---|---|---|---|---|
| positive_le_examined | 3/118 | 0/190 | 0/183 | 0/219 |
| pn_vs_positive_count | 7/76 | 5/138 | 3/138 | 15/217 |
| her2_score_vs_status | 6/22 | 1/74 | 2/95 | 12/154 |

## Cost and latency per report (test set)

| model | reports | input tokens mean (p95) | cached input tokens mean | output tokens mean (p95) | latency s mean / median / p95 | USD mean | USD total |
|---|---|---|---|---|---|---|---|
| gpt-4.1 (gpt-4.1-2025-04-14) | 258 | 2454 (4227) | 157 | 327 (501) | 1.80 / 1.69 / 2.78 | 0.0073 | 1.88 |
| gpt-4o (gpt-4o-2024-11-20) | 258 | 2454 (4227) | 183 | 333 (497) | 1.53 / 1.50 / 2.15 | 0.0092 | 2.38 |

Latency is wall-clock per call with 2 concurrent workers, including any SDK retry back-off. Cost = API usage x list price (cached-input rate where reported); billing not checked.

## Automatic error-source tags (unadjudicated heuristics; one disagreement can carry several tags)

- **rules**: abstained: untagged 425, missing_in_report 390, not_extracted_by_any 338, multiple_specimens_or_sides 235, ocr_noise_in_evidence 20; wrong_value: extractors_conflict 102, multiple_specimens_or_sides 63, curated_vs_report_conflict 56, untagged 8
- **gpt-4.1**: abstained: missing_in_report 390, not_extracted_by_any 338, multiple_specimens_or_sides 135, untagged 49, ocr_noise_in_evidence 15; wrong_value: curated_vs_report_conflict 56, multiple_specimens_or_sides 43, untagged 39, extractors_conflict 30, ocr_noise_in_evidence 2
- **gpt-4o**: abstained: missing_in_report 390, not_extracted_by_any 338, multiple_specimens_or_sides 141, untagged 64, ocr_noise_in_evidence 11, extractors_conflict 8, curated_vs_report_conflict 1; wrong_value: curated_vs_report_conflict 54, untagged 44, multiple_specimens_or_sides 43, extractors_conflict 26, ocr_noise_in_evidence 2

