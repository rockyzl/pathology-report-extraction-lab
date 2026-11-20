# Agent pre-read of the adjudication sample (NOT an adjudication)

The AI coding agent wrote this tentative first pass after the test run. It read only the quoted evidence and the context window for each item in `adjudication_sample.md`, never the full reports. **These notes do not replace Lu's hand review and must not be cited as validation.** For an unbiased review, fill in `adjudication_sample.csv` first and compare against these notes afterwards.

The sample was selected for disagreement, so it does **not** estimate error rates in the full test set.

| # | patient | field | tentative read | tentative source |
|---|---|---|---|---|
| 1 | TCGA-E2-A14X | er_status | The report says "ER: Negative … Allred 0". The rules matched a different "ESTROGEN RECEPTOR. Positive" string. The LLMs agree with curated. | rules error |
| 2 | TCGA-AO-A03R | pr_status | The report gives "<5% nuclear staining". The extractors read negative and curated says positive, so this looks like a 1%-vs-10% threshold or era convention. | threshold / mapping |
| 3 | TCGA-AC-A3TN | her2_ihc_status | The report says "Her2/neu: 1+" and curated says positive. Probably a different specimen or document. | curated from other document? |
| 4 | TCGA-E2-A14P | her2_ihc_score | gpt-4.1 quotes "Intensity: 3+", which matches curated. The rules took "HER2 IHC results: A HER2, 2+" from another block. | rules error (multiple blocks) |
| 5 | TCGA-BH-A18H | her2_ish_status | The report twice says FISH "not amplified" and curated says equivocal. | curated vs report conflict |
| 6 | TCGA-AR-A1AW | histologic_type | The report says "Infiltrating ductal carcinoma, with medullary like features". gpt-4.1 said other; curated, rules and gpt-4o say ductal. | LLM judgement / mapping ambiguity |
| 7 | TCGA-A2-A0SV | pathologic_t | The report says "pT4d" and all extractors say T4. Curated says T2. | curated vs report conflict |
| 8 | TCGA-E2-A154 | pathologic_n | The report says "pT 2 N 1c" and curated says N0. | curated vs report conflict |
| 9 | TCGA-AR-A5QM | laterality | The carcinoma is in "Breast, right, wide local excision", and the left side has benign intramammary nodes. gpt-4.1 said right; rules (majority vote), gpt-4o and curated say left. | needs full-report review (multiple specimens) |
| 10 | TCGA-A2-A0ST | margin_status | The tumor is "<0.1 cm from" margins. The LLMs said close and curated says negative. | definitional (close vs negative) |
| 11 | TCGA-E2-A1L6 | ln_examined | The LLMs say 6, matching curated. The rules summed overlapping x/y mentions and got 11. | rules error (sum heuristic) |
| 12 | TCGA-EW-A1IZ | ln_positive | The report says "macrometastases: 4" and curated says 5. A micrometastasis may have been counted, or the count comes from another document. | curated vs report conflict |
| 13 | TCGA-EW-A1PE | er_status | The rules read the template dash in "Estrogen Receptor: -" as negative. The report says ">1% immunoreactive". | rules error |
| 14 | TCGA-A2-A3XW | pr_status | The report says "PROGESTERONE RECEPTORS POSITIVE (10%…)" and curated says negative. | curated vs report conflict |
| 15 | TCGA-AO-A03L | her2_ihc_status | The report says "POSITIVE (STAINING INTENSITY OF 2+)". gpt-4.1 said equivocal, applying the prompt's "weakly positive / borderline 2+ → equivocal" convention beyond its wording. | LLM error, prompt-induced |
| 16 | TCGA-E2-A1L6 | her2_ihc_score | The LLMs quote "Interpretation: Negative. Intensity: 1+", which matches curated. The rules took "A HER2, 2+". | rules error (multiple blocks) |
| 17 | TCGA-E2-A109 | her2_ish_status | gpt-4.1's value (not amplified) matches curated but was **rejected**, because one of its two quotes was not verbatim. The rules read boilerplate ("FISH assay as amplified"). | grounding cost (LLM) + rules error |
| 18 | TCGA-B6-A0IE | histologic_type | The report says "features of lobular carcinoma" and curated says mixed. | ambiguous / other document |
| 19 | TCGA-A2-A3KD | pathologic_t | The report says "pT2N1mi" and curated says T3. | curated vs report conflict |
| 20 | TCGA-AQ-A7U7 | pathologic_n | The report says "pT2 pN1a" and curated says N2. | curated vs report conflict |
| 21 | TCGA-LL-A50Y | laterality | The report says "Specimen Laterality: Right". The rules majority vote picked "Left breast". | rules error |
| 22 | TCGA-BH-A0DT | margin_status | The report says invasive carcinoma "extends focally to the anterior margin" and curated says negative. A later re-excision is possible. | curated from other document? |
| 23 | TCGA-AR-A0U1 | ln_examined | The LLMs summed 5+2+23 = 30 and curated says 31. | off-by-one; needs full report |
| 24 | TCGA-EW-A1IW | ln_positive | The report says "two of eight" and "macrometastases: 2". The rules took "(0/1)". | rules error |
| 25 | TCGA-EW-A1IW | er_status | The report says "Immunoreactive tumor cells present (1%)". The rules read the template dash as negative. | rules error |
| 26 | TCGA-EW-A423 | pr_status | The report has both "PgR … POSITIVE (1-10%)" and "Progesterone Receptor: NEGATIVE". | conflicting statements in report |
| 27 | TCGA-BH-A1EX | her2_ihc_status | The report says "INTERPRETED AS POSITIVE (SCORE 2+)". gpt-4.1 said equivocal; gpt-4o and curated say positive. | LLM error, prompt-induced |
| 28 | TCGA-A2-A0D0 | her2_ihc_score | The report says "NEGATIVE, 1+ (REFER TO PRIOR SPECIMEN…)" and curated says 0. | curated from other document? |
| 29 | TCGA-AC-A23G | her2_ish_status | The report says "FISH: NEGATIVE" and curated says amplified. | curated from other document? |
| 30 | TCGA-E9-A1N4 | histologic_type | The report says "Histologic type: Lobular carcinoma" and curated says mixed. | ambiguous / other document |

## Tentative tally (agent, unverified)

| tentative source | items | count |
|---|---|---|
| rules extractor error | 1, 4, 11, 13, 16, 21, 24, 25 (+17) | 8–9 |
| gpt-4.1 error or loss | 6, 15, 27, plus a grounding rejection of a correct value in 17 | 3–4 |
| curated value disagrees with what this report states (curated from another document, or curated error) | 3, 5, 7, 8, 12, 14, 19, 20, 22, 28, 29 | ~11 |
| threshold / definitional / ambiguous / needs full report | 2, 9, 10, 18, 23, 26, 30 | ~7 |

### Two concrete LLM-side lessons (post hoc; not acted on in this run)

1. The prompt's convention "weakly positive / borderline 2+ → equivocal" was applied by gpt-4.1 to reports that literally say "POSITIVE (2+)" (items 15 and 27). A tighter instruction would say to keep the report's own interpretation word when it is given.
2. The rule that *every* quote must ground rejects a claim whose first quote is verbatim but whose second is not (item 17). Post hoc, 89 of gpt-4.1's 103 rejected claims had a claimed value equal to the curated value (gpt-4o: 127 of 149). The strict grounding rule therefore costs agreement. That is the intended trade-off, but it is now quantified.
