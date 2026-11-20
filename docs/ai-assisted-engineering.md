# AI-assisted engineering

**Who did what.** An AI coding agent (Claude) implemented this repository under Lu Zhang's direction. Lu set the goal, the constraints and the evaluation requirements:

- the agreement-versus-accuracy framing
- quote grounding
- a prespecified protocol before any test-set evaluation
- a patient-level split
- paired bootstrap CIs
- a hand-adjudication sample
- the budget and data-access rules

The agent wrote the code, the rules, the prompt, the tests and the documents. It ran the dev iteration, the one-shot test run and the provider-change replication. A second model reviewed its plan before implementation, and a separate reviewer agent audited the repo and its public claims afterwards.

**Not yet reviewed by a human:** the 30-item adjudication sample (`results/adjudication_sample.md`) and every result table. Until Lu reviews the adjudication sample, nothing in this repository should be described as "validated".

## How the work was checked

- **Unit tests** (`tests/test_core.py`): span grounding, curated-value mapping, patient-level split determinism and disjointness (including re-deriving the committed membership), kappa and bootstrap code on toy data with known answers, and the rules baseline on a synthetic fixture report written for the tests.
- **Programmatic grounding.** Every extracted value from either extractor must be backed by a verbatim quote. The code locates the quote itself (exact match, or exact after collapsing whitespace), and the quote must contain a field cue and, for counts, the number. Failures are counted as rejections, not silently dropped.
- **Protocol and freeze discipline.** `protocol.json` and `docs/protocol.md` were committed before any test-set call (commit `3ee8e84`). `results/freeze.json` records the code commit used for the single test run, and the test runner refuses to run if `src/` or `protocol.json` changed after that commit.
- **Budget guard.** LLM calls are cached in a jsonl file, and a call that fails is not cached. That means a failed call cannot silently become an "abstention" in the metrics. The runner refuses to start if estimated spend would exceed USD 10.

## Defects caught by verification

| # | Stage | Defect | How it was caught | Fix |
|---|---|---|---|---|
| 1 | Orientation | The keyword-prevalence count used to scope fields had a broken `case=` expression: it always evaluated to `False`, so every pattern ran case-insensitive, and the TNM patterns had no word boundaries. It reported pT in 92% of reports and ER in 62%. | Plan review by a second model before any code was written | The count was redone correctly (pT 57%, case-sensitive `ER` 35%) before the fields and budget were decided. |
| 2 | Dev, rules | The pN grounding cue rejected 197 dev answers. OCR prints the digit zero as the letter O (`pNo`, `pNO`), and run-together stagings (`pT2N1`) have no word boundary before `N`. | Rejection counts on dev were implausibly high | The cue now accepts `O`/`o` and a preceding digit or letter, and accepts `T Stage: 4` / `N Stage: 0` / `pTlc` forms. |
| 3 | Dev, LLM | In the first smoke test, gpt-4.1 cited the *clinical history* ("T1NOMO … on physical exam") as evidence for pathologic N. | Grounding cue rejection | Prompt v3 tells the model to ignore clinical staging and that `pNO` means pN0. |
| 4 | Dev, LLM | gpt-4.1 cited a gross-description sentence ("consists of a 2.0 cm …") as evidence for `ln_examined = 1`. | Number-in-quote check | The value was kept as a rejection, which is the intended behavior. |
| 5 | Dev, LLM | Some prompt-v2 quotes were not verbatim. The model normalized OCR text, used "…" ellipses, or stitched fragments together (e.g. `"B. ... (1/1)"`). | `quote_not_in_report` rejections: 43 of 645 claimed values (6.7%) on the 80 dev reports, re-scored with the final grounding code | Prompt v3 requires one contiguous stretch with no ellipses and no corrected typos. This brought `quote_not_in_report` to 23 of 651 (3.5%). No fuzzy matching was added, so the check stayed strict. |
| 6 | Dev, rules | The HER2 ISH rule read assay boilerplate ("FISH test for HER2 gene amplification") as `amplified`. That gave 8 wrong dev answers. | Error browser (`scripts/dev_errors.py`) on dev disagreements | The rule now needs a result phrase (`not amplified`, `amplified`, `: negative`, …), not the bare word "amplification". |
| 7 | Dev, rules | `HER2/NEU: zero or 1+` was extracted as score 1+. | Dev error browser | Ranges now produce an abstention (unit test `test_rules_abstain_on_empty_and_ambiguous`). |
| 8 | Dev, LLM | With 4 parallel workers, 24 of 80 calls hit HTTP 429 (token rate limit). | Runner raised on missing cache entries instead of scoring them as abstentions | Concurrency was lowered to 2 workers with 8 SDK retries. Failed calls are never cached, and the run is re-executed until complete. |
| 9 | Process | A `pkill -f scripts/dev_llm.py` meant to stop a hung background job also matched and killed the agent's own shell. | Exit code 144 | The job was simply re-run, and the cache made this free. Noted as a process-hygiene lesson. |

| 10 | Provenance | The LLM endpoint was described as a "personal" Azure OpenAI resource in five places, and its subscription ID and endpoint were hard-coded defaults. That description was inaccurate: it was a provisional endpoint, which is no longer used. | Independent review by a separate reviewer agent (read-only) | All "personal" claims and the hard-coded defaults were removed. The LLM arms were re-run once on the official OpenAI API with the same pinned snapshots (`docs/protocol.md`, Addendum 2), and the earlier results were moved to `results/superseded_azure/` for comparison. |
| 11 | Docs | The reviewer found overclaiming wording: the headline macro covers 10 categorical fields, not 12; "verifies the evidence span" suggested an entailment check; the cohort size (1,034) read as the LLM workload (gpt-4.1: 338 reports); the manifest hashes source files, not individual reports; the schema does not enforce "1–3 quotes". | Independent review | README, protocol and handoff wording corrected. |

The test-phase checks are listed in the README under "What was verified on the test run".

## Known limitations of the engineering

- There is one temperature-0 run per model. Run-to-run variance was not measured.
- The rules were tuned on dev reports from the same tissue-source-site templates that appear in test, because the split is not grouped by site. This favors the rules baseline.
- The grounding cue regexes are lexical sanity checks. They do not prove that a quote *entails* the value. For example, a quote containing "ER" and "positive" could still be misread.
- The error-source tags are automatic heuristics and are not adjudicated.
