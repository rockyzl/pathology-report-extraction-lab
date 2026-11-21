# Commit-hash mapping after the pre-publication history rewrite (2026-11-20)

Before first publication, on 2026-11-20, the history was rewritten twice with git filter-repo (`--replace-text`, literal replacements in file contents):

- **Pass 1** replaced local file-system paths and a cloud-resource identifier with placeholders, including the v1.0 `src/prel/llm.py` endpoint and subscription defaults.
- **Pass 2** reworded a few provenance and process sentences in the docs and in two comments for neutrality, and removed one sentence that pass 1 had made false. One of those comments is the `src/prel/llm.py` module docstring. It was changed identically in the replication freeze commit and every later commit, so `git diff <freeze> HEAD -- src protocol.json` is still empty.

As a result, the frozen trees differ from the code that actually ran only in those placeholder values and comment/docstring text. Prompt, schema, rules, grounding, metrics, protocol.json and all result values are unaffected; the only result file touched is the committed log `results/superseded_azure/test_run_attempt1.log`, where pass 1 replaced local paths in a traceback with `<repo>`. In both passes git filter-repo also updated commit-hash references inside commit messages to the new IDs. Commit order, dates, authors and all other content are unchanged.

Hashes cited inside files (`results/freeze.json`, `results/test_results.json`, `results/results_tables.md` and the `results/superseded_azure/` copies, `docs/protocol.md`, `docs/ai-assisted-engineering.md`) are the **original** IDs; use this table to map them. `scripts/run_eval.py` resolves the recorded freeze commit through this table.

| original | after pass 1 | final | commit |
|---|---|---|---|
| 3ee8e84 | 37c4ca0 | 37c4ca0 | Add data pipeline, extractors, grounding, metrics and prespecified protocol |
| 1fb21c1 | 80a785b | 80a785b | Add evaluation runner, consistency checks, adjudication sampler and dev results (v1.0 freeze) |
| ac1f6bc | fc05d1c | fc05d1c | Record freeze commit for the one-shot test run |
| 8840760 | c8b5ccf | c8b5ccf | Add held-out test results, adjudication sample, README and docs |
| 8188823 | 355f811 | 355f811 | Record rules timing, measured test cost and error-tag addendum |
| 2b0a44b | 4aab63d | 49d89eb | Switch LLM provider to the OpenAI API and add protocol Addendum 2 |
| 70b4bf1 | 5a36aa4 | 40eb518 | Record freeze commit for the OpenAI API replication run |
| e26bfcb | 17c25d7 | 952d90c | Log blocked OpenAI replication attempt; fail fast on insufficient quota (replication freeze) |
| 7e265f9 | c496670 | 6278cc9 | Re-record freeze for the pending OpenAI API replication |
| 67fc531 | e4b1177 | c3c01a1 | Add OpenAI API replication results and comparison with superseded run |
| fdf0bb6 | 62a4ae0 | ccf14c8 | Document replication scripts in README |
| — | d0d7a09 | 55bb15d | Add old-to-new commit hash map after history scrub (created after pass 1) |

Commits after `55bb15d` were made after both passes and keep their IDs.
