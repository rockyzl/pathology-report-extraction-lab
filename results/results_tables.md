# Held-out test results (n = 258 patients, frozen commit `1fb21c1`)

Agreement with curated TCGA clinical fields, **not accuracy**. e2e = agreeing answers / patients with a curated value
(not_stated and grounding rejections count as non-agreement). ans = agreement among answered. κ = Cohen's kappa over answered.

## Per-field agreement

| field | n curated | rules cov | rules e2e | rules ans | rules κ | gpt-4.1 cov | gpt-4.1 e2e | gpt-4.1 ans | gpt-4.1 κ | gpt-4o cov | gpt-4o e2e | gpt-4o ans | gpt-4o κ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| er_status | 247 | 0.409 | 0.364 | 0.891 | 0.734 | 0.571 | 0.567 | 0.993 | 0.982 | 0.571 | 0.567 | 0.993 | 0.981 |
| pr_status | 247 | 0.417 | 0.364 | 0.874 | 0.722 | 0.538 | 0.514 | 0.955 | 0.902 | 0.522 | 0.494 | 0.946 | 0.881 |
| her2_ihc_status | 219 | 0.251 | 0.215 | 0.855 | 0.670 | 0.438 | 0.374 | 0.854 | 0.719 | 0.502 | 0.438 | 0.873 | 0.748 |
| her2_ihc_score | 157 | 0.178 | 0.127 | 0.714 | 0.590 | 0.427 | 0.369 | 0.866 | 0.809 | 0.439 | 0.376 | 0.855 | 0.790 |
| her2_ish_status | 112 | 0.116 | 0.089 | 0.769 | 0.304 | 0.286 | 0.268 | 0.938 | 0.826 | 0.295 | 0.277 | 0.939 | 0.805 |
| histologic_type | 258 | 0.837 | 0.810 | 0.968 | 0.927 | 0.988 | 0.950 | 0.961 | 0.917 | 0.984 | 0.950 | 0.965 | 0.925 |
| pathologic_t | 258 | 0.616 | 0.581 | 0.943 | 0.897 | 0.713 | 0.671 | 0.940 | 0.893 | 0.713 | 0.674 | 0.946 | 0.902 |
| pathologic_n | 258 | 0.566 | 0.550 | 0.973 | 0.958 | 0.736 | 0.702 | 0.953 | 0.924 | 0.756 | 0.721 | 0.954 | 0.925 |
| laterality | 258 | 0.814 | 0.791 | 0.971 | 0.943 | 0.919 | 0.899 | 0.979 | 0.958 | 0.899 | 0.888 | 0.987 | 0.974 |
| margin_status | 247 | 0.611 | 0.543 | 0.887 | 0.300 | 0.789 | 0.680 | 0.862 | 0.288 | 0.785 | 0.611 | 0.778 | 0.206 |
| ln_examined | 224 | 0.513 | 0.246 | 0.478 | n/a | 0.812 | 0.661 | 0.813 | n/a | 0.808 | 0.652 | 0.807 | n/a |
| ln_positive | 219 | 0.511 | 0.402 | 0.786 | n/a | 0.826 | 0.726 | 0.878 | n/a | 0.817 | 0.726 | 0.888 | n/a |
| **macro, 10 categorical** | |  | 0.444 | |  |  | 0.599 | |  |  | 0.600 | |  |
| **macro, all 12** | |  | 0.424 | |  |  | 0.615 | |  |  | 0.614 | |  |

## Primary comparison (prespecified)

- macro agreement_e2e over the 10 categorical fields, gpt-4.1 minus rules, test set: **+0.156 [+0.136, +0.176]** (paired patient bootstrap, B = 2000, seed 20261120); gpt-4.1 0.599 vs rules 0.444. Decision: **gpt-4.1 higher agreement**.
- gpt-4o − rules (10 categorical): +0.156 [+0.135, +0.178]
- gpt-4.1 − gpt-4o (10 categorical): -0.000 [-0.011, +0.009]
- gpt-4.1 − rules (all 12): +0.192 [+0.172, +0.211]; gpt-4o − rules (all 12): +0.191 [+0.171, +0.211]

Per-field e2e difference vs rules (descriptive, no multiplicity correction):

| field | gpt-4.1 − rules [95% CI] | gpt-4o − rules [95% CI] |
|---|---|---|
| er_status | +0.202 [+0.154, +0.255] | +0.202 [+0.154, +0.255] |
| pr_status | +0.150 [+0.101, +0.202] | +0.130 [+0.077, +0.186] |
| her2_ihc_status | +0.160 [+0.096, +0.228] | +0.224 [+0.164, +0.283] |
| her2_ihc_score | +0.242 [+0.172, +0.312] | +0.248 [+0.172, +0.318] |
| her2_ish_status | +0.179 [+0.107, +0.250] | +0.188 [+0.116, +0.259] |
| histologic_type | +0.140 [+0.093, +0.190] | +0.140 [+0.093, +0.186] |
| pathologic_t | +0.089 [+0.054, +0.128] | +0.093 [+0.054, +0.136] |
| pathologic_n | +0.151 [+0.101, +0.202] | +0.171 [+0.116, +0.225] |
| laterality | +0.109 [+0.070, +0.155] | +0.097 [+0.054, +0.143] |
| margin_status | +0.138 [+0.081, +0.198] | +0.069 [+0.008, +0.134] |
| ln_examined | +0.415 [+0.353, +0.478] | +0.406 [+0.344, +0.469] |
| ln_positive | +0.324 [+0.251, +0.393] | +0.324 [+0.251, +0.397] |

## Abstention and grounding

| extractor | field cells | claimed values | grounding rejections | rejection rate of claims | not_stated | rejection reasons |
|---|---|---|---|---|---|---|
| rules | 3096 | 1445 | 0 | 0.000 | 1651 | {} |
| gpt-4.1 | 3096 | 2081 | 103 | 0.049 | 1015 | {"quote_lacks_field_cue": 50, "quote_not_in_report": 42, "number_not_in_quote": 11} |
| gpt-4o | 3096 | 2138 | 149 | 0.070 | 958 | {"quote_not_in_report": 66, "number_not_in_quote": 26, "quote_lacks_field_cue": 57} |

## Cross-field consistency checks (violations / patients with both fields answered)

| check | rules | gpt-4.1 | gpt-4o | curated |
|---|---|---|---|---|
| positive_le_examined | 3/118 | 0/189 | 0/189 | 0/219 |
| pn_vs_positive_count | 7/76 | 5/143 | 9/148 | 15/217 |
| her2_score_vs_status | 6/22 | 0/81 | 3/97 | 12/154 |

## Cost and latency per report (test set)

| model | reports | input tokens mean (p95) | output tokens mean (p95) | latency s mean / median / p95 | USD mean | USD total |
|---|---|---|---|---|---|---|
| gpt-4.1 (gpt-4.1-2025-04-14) | 258 | 2454 (4227) | 331 (533) | 4.32 / 3.10 / 10.79 | 0.0076 | 1.95 |
| gpt-4o (gpt-4o-2024-11-20) | 258 | 2454 (4227) | 334 (524) | 2.38 / 2.24 / 3.39 | 0.0095 | 2.44 |

Latency is wall-clock per call with 2 concurrent workers and SDK retries on HTTP 429, so it includes rate-limit back-off.

## Automatic error-source tags (unadjudicated heuristics; one disagreement can carry several tags)

- **rules**: abstained: untagged 429, missing_in_report 390, not_extracted_by_any 334, multiple_specimens_or_sides 235, ocr_noise_in_evidence 20; wrong_value: extractors_conflict 99, multiple_specimens_or_sides 63, curated_vs_report_conflict 57, untagged 9, ocr_noise_in_evidence 1
- **gpt-4.1**: abstained: missing_in_report 390, not_extracted_by_any 334, multiple_specimens_or_sides 131, untagged 55, ocr_noise_in_evidence 14; wrong_value: curated_vs_report_conflict 57, multiple_specimens_or_sides 53, extractors_conflict 38, untagged 38, ocr_noise_in_evidence 4
- **gpt-4o**: abstained: missing_in_report 390, not_extracted_by_any 334, multiple_specimens_or_sides 126, untagged 50, ocr_noise_in_evidence 12, extractors_conflict 3, curated_vs_report_conflict 1; wrong_value: curated_vs_report_conflict 56, multiple_specimens_or_sides 54, untagged 51, extractors_conflict 33, ocr_noise_in_evidence 3

