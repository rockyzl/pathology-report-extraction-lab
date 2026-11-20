# Adjudication sample (UNREVIEWED)

30 held-out test (patient, field) pairs where gpt-4.1 or the rules baseline answered a value that differs from the curated TCGA value.
Sampled round-robin over fields, shuffled within field (seed 20261120). **Nothing here has been reviewed by a human yet.**

For each item, read the report context (and, if needed, the full report) and fill in the CSV columns `lu_true_value` (what this report says, or `not_in_report`),
`lu_source_of_disagreement` (one of: `extractor_error`, `curated_error_or_other_document`, `report_ambiguous_or_conflicting`, `multiple_specimens`, `ocr_noise`, `mapping_issue`) and `lu_notes`.

Report excerpts: TCGA-Reports (Kefeli & Tatonetti 2024), CC BY 4.0. `auto_tags` are automatic heuristics, not adjudications.

## 1. TCGA-E2-A14X — `er_status`

- **curated:** `negative`  ·  auto tags: extractors_conflict
- **rules:** `positive` — “ESTROGEN RECEPTOR. Positive”
- **gpt-4.1:** `negative` — “ER: Negative. | ER: Negative Allred Score: 0 = Proportion Score 0 + Intensity Score. 0.”
- **gpt-4o:** `negative` — “ER: Negative Allred Score: 0 = Proportion Score 0 + Intensity Score. 0.”
- **context:** …ic areas: fibroadenoma. DCIS present. Margins uninvolved by DCIS. DCIS Quantity: Estimate 5%. DCIS Type: Solid. DCIS Location: :Associated with invasive tumor. Nuclear grade: High. Necrosis: Present. ER/PR/HER2 Results. ER: Negative. PR: Negative. HER2: Negative by IHC. Pathological staging (pTN): pT 2 N 2. SYNOPTIC REPORT - BREAST, ER/PR RESULTS. Specimen: Surgical Excision. Block Number: A22 and F12 (lymph node). ER: Negative Allred Score: 0 = Pro…
- **Lu:** true value ____ · source ____ · notes ____

## 2. TCGA-AO-A03R — `pr_status`

- **curated:** `positive`  ·  auto tags: curated_vs_report_conflict
- **rules:** `negative` — “PR-”
- **gpt-4.1:** `negative` — “PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY”
- **gpt-4o:** `negative` — “PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY”
- **context:** …lary contents. Block. Sect. Site. PCs. 1. bln. 1. 1. In. 1. Procedures/Addenda: Addendum. Date Complete: Addendum Diagnosis. ADDENDUM REPORT. SITE: LEFT BREAST (PART 4). ER: 95% NUCLEAR STAINING WITH MODERATE INTENSITY. PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY. HER2/NEU (HERCEPTEST) : NEGATIVE (STAINING INTENSITY OF 0). CONTROLS ARE SATISFACTORY. . M.D. Intraoperative Consultation: Note: The diagnoses given in this section pertain only to the tissue sample. examined at the ti…
- **Lu:** true value ____ · source ____ · notes ____

## 3. TCGA-AC-A3TN — `her2_ihc_status`

- **curated:** `positive`  ·  auto tags: multiple_specimens_or_sides
- **rules:** `[not_stated]`
- **gpt-4.1:** `negative` — “Her2/neu: 1+”
- **gpt-4o:** `negative` — “Her2/neu: 1+.”
- **context:** …nt metastasis (pM): Not applicable. Tumor Stage: IIB. RECEPTOR STATUS AND HER2/NEU: Biomarkers performed on. two separate core needle biopsies. Estrogen receptors: 95%. Progesterone receptors: 80% and 50%, respectively. Her2/neu: 1+. Printed: Acct No. Pathology Report - Page 3/6. - Page 3. Datient: FINAL SURGICAL PATHOLOGY REPORT. Ki-67 proliferative index: 1-2%. Source of Specimen: A. Sentinel lymph node;Sentinel node #1, Right breast. B. Breast;L…
- **Lu:** true value ____ · source ____ · notes ____

## 4. TCGA-E2-A14P — `her2_ihc_score`

- **curated:** `3+`  ·  auto tags: extractors_conflict
- **rules:** `2+` — “HER2 IHC results: A HER2, 2+”
- **gpt-4.1:** `3+` — “Intensity: 3+.”
- **gpt-4o:** `[rejected]` — “Intensity: 3+ | Scoring Criterion and Scoring System: IHC Level of Expression(Score) /Tumor Cell Membrane Staining Pattern. Positive (3+)/Strong complete membrane Staining, >10% of Cells.”
- **context:** …in breast cancer. J Clin Oncol. 17:1474-1481, 1999. SYNOPTIC REPORT - BREAST HER-2 RESULTS. HER2 Status Results, Immunohistochemistry Evaluation. Specimen: Surgical Excision. Block Number: B14. Interpretation: POSITIVE. Intensity: 3+. % Tumor Staining: 100%. Fish Ordered: No. METHODOLOGY. Methodology: Fixation Type and Length: Tissue was fixed in 10% neutral buffered formalin. for no less than 8 and no longer than 24 hours. Antibody and Assay Methodo…
- **Lu:** true value ____ · source ____ · notes ____

## 5. TCGA-BH-A18H — `her2_ish_status`

- **curated:** `equivocal`  ·  auto tags: multiple_specimens_or_sides,curated_vs_report_conflict
- **rules:** `not_amplified` — “FISH not amplified”
- **gpt-4.1:** `not_amplified` — “FISH not amplified | HER2/NEU (FISH): Not amplified.”
- **gpt-4o:** `not_amplified` — “HER-2/NEU (IHC 2+, FISH not amplified)”
- **context:** …ANGES. L. THE NON-NEOPLASTIC BREAST SHOWS FIBROCYSTIC CHANGES. M. THE INVASIVE TUMOR CELLS ARE POSITIVE FOR ESTROGEN (H-score 230), POSITIVE FOR. PROGESTERONE RECEPTORS (H-score 180), AND NEGATIVE FOR HER-2/NEU (IHC 2+, FISH not amplified). AS PER THE PREVIOUS PATHOLOGY REPORT. PART 2: RIGHT AXILLARY SENTINEL LYMPH NODE #1, BIOPSY -. ONE LYMPH NODE, NEGATIVE FOR METASTATIC TUMOR (0/1). PART 3: BREAST, LEFT. AT 12 O'CLOCK, SEGMENTAL MASTECTOMY -. A. INVAS…
- **Lu:** true value ____ · source ____ · notes ____

## 6. TCGA-AR-A1AW — `histologic_type`

- **curated:** `ductal`  ·  auto tags: extractors_conflict
- **rules:** `ductal` — “Infiltrating ductal”
- **gpt-4.1:** `other` — “Infiltrating ductal carcinoma, with medullary like. features”
- **gpt-4o:** `ductal` — “Infiltrating ductal carcinoma, with medullary like. features”
- **context:** …Final Diagnosis. Breast,Meft ypper inner quadrant, lumpectomy: Infiltrating ductal carcinoma, with medullary like. features, Nottingham grade III (of III), [tubules 3/3, nuclei 3/3, mitoses 2/3; Nottingham score. 8/9], forming a 2.7 x 2.5 x 2.0 cm yellow-tan, somewhat circumscribed, sclerotic mass. [AJCCpT2]. Ductal carcinoma in situ is abse…
- **Lu:** true value ____ · source ____ · notes ____

## 7. TCGA-A2-A0SV — `pathologic_t`

- **curated:** `T2`  ·  auto tags: curated_vs_report_conflict
- **rules:** `T4` — “pT4”
- **gpt-4.1:** `T4` — “PATHOLOGIC STAGE: pT4d N2a MX.”
- **gpt-4o:** `T4` — “PATHOLOGIC STAGE: pT4d N2a MX.”
- **context:** …T). ESTROGEN RECEPTORS: Previously ordered and positive. PROGESTERONE RECEPTORS: Previously ordered and positive. HER 2 NEU by IHC: Previously ordered; weakly positive. HER 2 Neu BY FISH: Previously ordered and pending. PATHOLOGIC STAGE: pT4d N2a MX. ADDITIONAL PATHOLOGIC CHANGES. -DUCTAL CARCINOMA IN-SITU, HIGH GRADE. - -CYSTIC CHANGE WITH APOCRINE METAPLASIA. B. LYMPH NODES, RIGHT AXILLA, DISSECTION: EIGHT LYMPH NODES POSITIVE FOR TUMOR, WITH EXTENSIVE EXTRACAPSUL…
- **Lu:** true value ____ · source ____ · notes ____

## 8. TCGA-E2-A154 — `pathologic_n`

- **curated:** `N0`  ·  auto tags: multiple_specimens_or_sides,curated_vs_report_conflict
- **rules:** `N1` — “pT 2 N 1”
- **gpt-4.1:** `N1` — “pT 2 N 1c”
- **gpt-4o:** `N1` — “Pathological staging (pTN): pT 2 N 1c.”
- **context:** …id. Cribriform. DCIS Location Associated with invasive tumor. Nuclear grade: High. Necrosis: Present. ER/PR/HER2 Results. ER: Positive. PR: Negative. HER2: Negative by IHC. Performed on Case: Pathological staging (pTN): pT 2 N 1c. CLINICAL HISTORY: None given. PRE-OPERATIVE DIAGNOSIS: Left breast cancer. Microscopic/Diagnostic Dictation: Pathologist. Final Review: Pathologist,. Final: Pathologist, I.…
- **Lu:** true value ____ · source ____ · notes ____

## 9. TCGA-AR-A5QM — `laterality`

- **curated:** `left`  ·  auto tags: multiple_specimens_or_sides,extractors_conflict
- **rules:** `left` — “Breast, left”
- **gpt-4.1:** `right` — “Breast, right, wide local excision”
- **gpt-4o:** `left` — “Breast, left, wide local excision: Infiltrating lobular carcinoma, Nottingham grade II (of III).”
- **context:** …ue dye is not. identified in any of the three left axillary sentinel lymph nodes. Immunohistochemical cytokeratin stain was performed on the paraffin embedded sentinel lymph. node tissue and confirms the H&E impression. Breast, right, wide local excision: Infiltrating ductal carcinoma, Nottingham grade II (of III). [tubules 3/3, nuclei 2/3, mitoses 2/3; Nottingham score 7/9], forming a mass (1.4 x 1.0 x 0.9 cm). [AJCC pT1c]. Extensive ductal carcinoma in situ, low to in…
- **Lu:** true value ____ · source ____ · notes ____

## 10. TCGA-A2-A0ST — `margin_status`

- **curated:** `negative`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `close` — “TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS”
- **gpt-4o:** `close` — “-TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS.”
- **context:** …2. FINAL DIAGNOSIS: A. BREAST, RIGHT; EXCISION: - INFILTRATING DUCTAL CARCINOMA, POORLY DIFFERENTIATED (MODIFIED. BLOOM-RICHARDSON GRADE 9: MITOSES=3, NUCLEAR PLEOMORPHISM=3, TUBULE. FORMATION=3). -TUMOR SIZE 2.0 CM. - -TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS. - -ASSOCIATED FINDINGS: FIBROCYSTIC CHANGES INCLUDING STROMAL SCLEROSIS. AND MICROCYSTS. -MICROCALCIFICATIONS IDENTIFIED, ASSOCIATED WITH BENIGN BREAST TISSUE. - IMMUNOHISTOCHEMICAL STAINS FOR ESTROGEN AND PROGESTERONE…
- **Lu:** true value ____ · source ____ · notes ____

## 11. TCGA-E2-A1L6 — `ln_examined`

- **curated:** `6`  ·  auto tags: extractors_conflict
- **rules:** `11` — “LYMPH NODES, NEGATIVE FOR MALIGNANCY (0/2) | LYMPH NODES, NEGATIVE FOR TUMOR (0/3) | lymph nodes one positive, (1/6)”
- **gpt-4.1:** `6` — “SENTINEL LYMPH NODE #1 LEFT AXILLA, EXCISION: - METASTATIC ADENOCARCINOMA, IDENTIFIED IN ONE LYMPH NODE | SENTINEL LYMPH NODES #2-3, LEFT AXILLA, EXCISION: - TWO LYMPH NODES, NEGATIVE FOR MALIGNANCY (0/2) | THREE ADDITIONAL LYMPH NODES, NEGATIVE FOR TUMOR (0/3)”
- **gpt-4o:** `6` — “Lymph nodes: Sentinel lymph nodes and axillary. lymph nodes one positive, (1/6).”
- **context:** …SPECIMENS: A. SENTINEL LYMPH NODE 1 LEFT AXILLA. B. SENTINEL LYMPH NODE 2 LEFT AXILLA. C. SENTINEL LYMPH NODE 3 LEFT AXILLA. D. LEFT BREAST. DIAGNOSIS: A. SENTINEL LYMPH NODE #1 LEFT AXILLA, EXCISION: - METASTATIC ADENOCARCINOMA, IDENTIFIED IN ONE LYMPH NODE (MICROMETASTASES,. 1.8 MM IN GREATEST DIAMETER). B., C. SENTINEL LYMPH NODES #2-3, LEFT AXILLA, EXCISION: - TWO LYMPH NODES, NEGATIVE FOR MALIGNANCY (0/2). D. LEFT BREAST, MASTECTOMY: - WELL DIFFERENTIATED INFILTRATING …
- **Lu:** true value ____ · source ____ · notes ____

## 12. TCGA-EW-A1IZ — `ln_positive`

- **curated:** `5`  ·  auto tags: multiple_specimens_or_sides,curated_vs_report_conflict
- **rules:** `4` — “Number of lymph nodes with macrometastases: 4”
- **gpt-4.1:** `4` — “Number of lymph nodes with macrometastases: 4”
- **gpt-4o:** `4` — “Metastatic carcinoma in four out of nine lymph nodes (4/9)”
- **context:** …f present). Lymph-Vascular Invasion: Present. Dermal Lymph-Vascular Invasion: Not identified. Lymph Nodes: Number of sentinel lymph nodes examined: 0. Total number of lymph nodes examined (sentinel and nonsentinel): 13. Number of lymph nodes with macrometastases: 4. Size of largest metastatic deposit: 2.0 cm. Extranodal Extension: Not identified. SURGICAL PATHOL Report. Method of Evaluation of Sentinel Lymph Nodes: Hematoxylin and eosin (H&E), one level. Pathologic Staging (pTNM).…
- **Lu:** true value ____ · source ____ · notes ____

## 13. TCGA-EW-A1PE — `er_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `negative` — “Estrogen Receptor: -”
- **gpt-4.1:** `positive` — “Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (>1%)”
- **gpt-4o:** `positive` — “Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (>1%).”
- **context:** …est metastatic deposit (if present): 2.5 mm. Extranodal Extension: Not identified. Pathologic Staging (pTNM). - Primary Tumor: pTic. - Regional Lymph Nodes: pN1a. - Distant Metastasis: Not applicable. Ancillary Studies: Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (>1%). Progesterone Receptor: . Performed on another specimen. ; Results: Immunoreactive tumor cells present (1%). Her2: - Performed on another specimen: , Results: Negative. AJCC classification (7th ed) pT1c, pN1a, pMn/a. NO…
- **Lu:** true value ____ · source ____ · notes ____

## 14. TCGA-A2-A3XW — `pr_status`

- **curated:** `negative`  ·  auto tags: curated_vs_report_conflict
- **rules:** `positive` — “PROGESTERONE RECEPTORS POSITIVE”
- **gpt-4.1:** `positive` — “PROGESTERONE RECEPTORS POSITIVE (10% Nuclear staining, per.”
- **gpt-4o:** `positive` — “PROGESTERONE RECEPTORS POSITIVE (10% Nuclear staining, per.”
- **context:** …UT DEFINITE NECROSIS. - LYMPH NODES: SEE PARTS B-E. - NIPPLE INVOLVEMENT: PRESENT WITHIN THE STROMA. - SKIN INVOLVEMENT ABSENT. - MULTICENTRICITY ABSENT. - ESTROGEN RECEPTORS : POSITIVE (95-100% Nuclear staining, per. - PROGESTERONE RECEPTORS POSITIVE (10% Nuclear staining, per. - HER2 by IHC: NEGATIVE (1+; per. - HER2 BY FISH: NOT PERFORMED. - PATHOLOGIC STAGE: pT2 N1a Mx. - ADDITIONAL PATHOLOGIC CHANGES: -FIBROCYSTIC CHANGES INCLUDING STROMAL FIBROSIS, MICROCYSTS AND. APOCRINE METAPLASIA. - N…
- **Lu:** true value ____ · source ____ · notes ____

## 15. TCGA-AO-A03L — `her2_ihc_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `positive` — “HER2/NEU (HERCEPTEST) : POSITIVE”
- **gpt-4.1:** `equivocal` — “HER2/NEU (HERCEPTEST) : POSITIVE (STAINING INTENSITY OF 2+)”
- **gpt-4o:** `positive` — “HER2/NEU (HERCEPTEST) : POSITIVE (STAINING INTENSITY OF 2+) .”
- **context:** …. UOQ. 2. Procedures/Addenda: Addendum. Date Complete: Addendum Diagnosis. ADDENDUM. SITE: RIGHT BREAST. PART #2. ER: 70% OF NUCLEAR STAINING WITH MODERATE INTENSITY. PR: 10% OF NUCLEAR STAINING WITH MODERATE INTENSITY. HER2/NEU (HERCEPTEST) : POSITIVE (STAINING INTENSITY OF 2+) . MD PHD. Intraoperative Consultation: Note: The diagnoses given in this section pertain only to the. tissue sample examined at the time of the intraoperative. consultation. 1). FROZEN SECTION DIAGNOSIS: METASTATIC CARC…
- **Lu:** true value ____ · source ____ · notes ____

## 16. TCGA-E2-A1L6 — `her2_ihc_score`

- **curated:** `1+`  ·  auto tags: extractors_conflict
- **rules:** `2+` — “HER2 IHC results: A HER2, 2+”
- **gpt-4.1:** `1+` — “Interpretation: Negative. Intensity: 1+. % Tumor Staining: 40%.”
- **gpt-4o:** `1+` — “Intensity: 1+.”
- **context:** …cinoma extends to within 3 mm. of the deep margin. Specimens Involved. Specimens: D: LEFT BREAST. HER2 Status Results, Immunohistochemistry Evaluation. SPECIMEN. Surgical Excision. Block Number: Block. D4. TEST RESULTS. Interpretation: Negative. Intensity: 1+. % Tumor Staining: 40%. FISH ORDERED. METHODOLOGY. Methodology: Fixation Type and Length: Tissue was fixed in 10% neutral buffered formalin. ) for no less than 8 and no longer than 24 hours. Antibody and Assay Methodology: Rabbit anti-human HE…
- **Lu:** true value ____ · source ____ · notes ____

## 17. TCGA-E2-A109 — `her2_ish_status`

- **curated:** `not_amplified`  ·  auto tags: —
- **rules:** `amplified` — “FISH assay as amplified”
- **gpt-4.1:** `[rejected]` — “HER-2 NOT AMPLIFIED | HER-2/CEP17 ratio: 1.46”
- **gpt-4o:** `not_amplified` — “HER-2 NOT AMPLIFIED | HER2/CEP17 ratio: 1.46”
- **context:** …by IHC as outline above and interpreted as, negative. (score 0/1+) equivocal (score 2+) and positive (score 3+) without knowledge of the previous reported. results. These cases were also blindly read using two different FISH assay as amplified or non-amplified and. the HER2/CEP17 ratios were recorded. After analyzing these results, there was 100% concordance. between the IHC and FISH results for cases that were interpreted as either positive or negative by IH…
- **Lu:** true value ____ · source ____ · notes ____

## 18. TCGA-B6-A0IE — `histologic_type`

- **curated:** `mixed_ductal_lobular`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `lobular` — “THE TUMOR HAS FEATURES OF LOBULAR CARCINOMA”
- **gpt-4o:** `lobular` — “NOTE: THE TUMOR HAS FEATURES OF LOBULAR CARCINOMA”
- **context:** …ecimen. Representative sections are submitted in Blocks A1 and A2. DIAGNOSIS: A. BREAST, LEFT, INCISIONAL BIOPSY: POORLY DIFFERENTIATED CARCINOMA WITH EXTENSIVE VASCULAR INVASION. IN SITU CARCINOMA IS NOT PRESENT. NOTE: THE TUMOR HAS FEATURES OF LOBULAR CARCINOMA, BUT AN IN SITU COMPONENT. IS NOT PRESENT. eBrowser Result for: 1 of 1.…
- **Lu:** true value ____ · source ____ · notes ____

## 19. TCGA-A2-A3KD — `pathologic_t`

- **curated:** `T3`  ·  auto tags: curated_vs_report_conflict
- **rules:** `T2` — “pT2”
- **gpt-4.1:** `T2` — “PATHOLOGIC STAGE: pT2N1mi (”
- **gpt-4o:** `T2` — “PATHOLOGIC STAGE: pT2N1mi (.”
- **context:** …"B"). ESTROGEN RECEPTORS : POSITIVE (>95%, please see report. PROGESTERONE RECEPTORS: POSITIVE (90%, please see report. /. HER2NEU by IHC: NEGATIVE (Score 1+, please see report. Specimen #: FINAL DIAGNOSIS (continued) : PATHOLOGIC STAGE: pT2N1mi (. - ADDITIONAL PATHOLOGIC FINDINGS: STROMAL SCLEROSIS AND FOCAL MICROCYST FORMATION. FOCAL PRIOR BIOPSY SITE CHANGES. CLINICAL DIAGNOSIS AND HISTORY: Right breast cancer -year-old female. PRE-OPERATIVE DIAGNOSIS: None pr…
- **Lu:** true value ____ · source ____ · notes ____

## 20. TCGA-AQ-A7U7 — `pathologic_n`

- **curated:** `N2`  ·  auto tags: curated_vs_report_conflict
- **rules:** `N1` — “pN1”
- **gpt-4.1:** `N1` — “AJCC PATHOLOGIC TNM STAGE: pT2 pN1a.”
- **gpt-4o:** `N1` — “AJCC PATHOLOGIC TNM STAGE: pT2 pN1a.”
- **context:** …ith benign breast changes. Other pathologic findings: Extensive stromal fibrosis with patchy amyloid deposition. - Fibrocystic changes. - Columnar cell change. - Epidermal inclusion cyst. - Previous biopsy site changes. AJCC PATHOLOGIC TNM STAGE: pT2 pN1a. BREAST STAGE GROUPING: IIB. Note: This pathologic stage assessment is based on information. available at the time of this report, and is subject to change. pending clinical review and additional information. Ancillary s…
- **Lu:** true value ____ · source ____ · notes ____

## 21. TCGA-LL-A50Y — `laterality`

- **curated:** `right`  ·  auto tags: multiple_specimens_or_sides,extractors_conflict
- **rules:** `left` — “Left breast”
- **gpt-4.1:** `right` — “Specimen Laterality: Right | Pre-Op Diagnosis: Right breast lobular CA.”
- **gpt-4o:** `right` — “Specimen Laterality: Right.”
- **context:** …SUMMARY CHECKLIST. COMMENT (s). SURGICAL PATHOLOGY CANCER CASE SUMMARY - CAP APPROVED. Procedure: Total mastectomy (including nipple and skin). Lymph Node Sampling: Axillary dissection (partial or complete. dissection). Specimen Laterality: Right. Tumor Site: Other; multifocal. Histologic Type: Invasive lobular carcinoma. Tumor Size: Greatest dimension of largest focus of invasion. RUN DATE. RUN TIME. RUN USER. SPEC #: COMMENT (s). >1 mm: 30 mm (3.0 cm). Histolo…
- **Lu:** true value ____ · source ____ · notes ____

## 22. TCGA-BH-A0DT — `margin_status`

- **curated:** `negative`  ·  auto tags: curated_vs_report_conflict
- **rules:** `positive` — “MARGINS INVOLVED”
- **gpt-4.1:** `positive` — “SURGICAL MARGINS INVOLVED BY INVASIVE COMPONENT: Yes, fincal. | INVASIVE CARCINOMA EXTENDS FOCALLY TO THE ANTERIOR MARGIN (SLIDE 3E).”
- **gpt-4o:** `positive` — “SURGICAL MARGINS INVOLVED BY INVASIVE COMPONENT: Yes, fincal.”
- **context:** …r grade: 2. ubule formation 2. Mitolic activity acore. 1. Total Nottingham sexte: 5. Nollingham grade (1,2,3). 1. ANGIOLYMPHATIC INVASION: DERMAL LYMPHATIC INVASIÓN: CALCIFICATION: TUMOR TVPE, IN SITU: Cribriform. LCIS. SURGICAL MARGINS INVOLVED BY INVASIVE COMPONENT: Yes, fincal. SURG MARGINS INVOLVED BY IN SITU COMPONENT: PAGET'S DISEASE OF NIPPLE: LYMPM NODES POSITIVE: 1. LYMPH NODES EXAMINED: 18. METHOD(S) OF LYMPH NODE CXAMINATION. H/E Mair. SENTINEL NODE METASTA9IS: SIZE OF NODAL METASTASES…
- **Lu:** true value ____ · source ____ · notes ____

## 23. TCGA-AR-A0U1 — `ln_examined`

- **curated:** `31`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `30` — “Multiple (5) left axillary sentinel lymph nodes | left highest (2) and left axillary (23) lymph nodes”
- **gpt-4o:** `30` — “Multiple (5) left axillary sentinel lymph nodes are. | Multiple left highest (2) and left axillary (23) lymph nodes are.”
- **context:** …tely submitted inferior margin, are. negative for tumor. Lymph node, left breast intramammary, excision: Metastatic adenocarcinoma. no extranodal extension is. identified. Lymph nodes, left axillary sentinel, excisions: Multiple (5) left axillary sentinel lymph nodes are. negative for tumor (blue dye identified in left axillary lymph node No. 1 only). Lymph nodes, left axillary, dissection: Multiple left highest (2) and left axillary (23) lymph nodes are. negative for tumor. Her-2/N…
- **Lu:** true value ____ · source ____ · notes ____

## 24. TCGA-EW-A1IW — `ln_positive`

- **curated:** `2`  ·  auto tags: multiple_specimens_or_sides,extractors_conflict
- **rules:** `0` — “lymph node (0/1)”
- **gpt-4.1:** `2` — “Number of lymph nodes with macrometastases (>0.2 cm): 2. | Metastatic carcinoma to two of eight lymph nodes (/2/8).”
- **gpt-4o:** `2` — “Number of lymph nodes with macrometastases (>0.2 cm): 2.”
- **context:** …n: - Present. Dermal Lymph-Vascular Invasion: SURGICAL PATHOL Report. - Not identified. Lymph Nodes: - Number of sentinel lymph nodes examined: 2. - Total number of lymph nodes examined (sentinel and Nonsentinel): 10. - Number of lymph nodes with macrometastases (>0.2 cm): 2. Extranodal Extension: - Not identified. Method of Evaluation of Sentinel Lymph Nodes: - Hematoxylin and eosin (H&E, one level). - Immunohistochemistry. Anciliary Studies: Estrogen Receptor: - Performed on another specim…
- **Lu:** true value ____ · source ____ · notes ____

## 25. TCGA-EW-A1IW — `er_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `negative` — “Estrogen Receptor: -”
- **gpt-4.1:** `positive` — “Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%) | Ancillary Studies: Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%)”
- **gpt-4o:** `positive` — “Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%).”
- **context:** …f lymph nodes with macrometastases (>0.2 cm): 2. Extranodal Extension: - Not identified. Method of Evaluation of Sentinel Lymph Nodes: - Hematoxylin and eosin (H&E, one level). - Immunohistochemistry. Anciliary Studies: Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%). Progesterone Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%). HER2/neu. - Performed on another specimen: Results: Equivocal (Score 2+). CISH for HER2/Neu: - Performed on anot…
- **Lu:** true value ____ · source ____ · notes ____

## 26. TCGA-EW-A423 — `pr_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `negative` — “Progesterone Receptor: NEGATIVE”
- **gpt-4.1:** `positive` — “Progesterone receptor. PgR 636. POSITIVE (1-10%)”
- **gpt-4o:** `positive` — “Progesterone receptor. PgR 636. POSITIVE (1-10%)”
- **context:** …CALIZATION LUMPECTOMY: Immunohistochemical studies were performed on formalin fixed tissue with the following results for [invasive. carcinoma/DCIS/metastatic carcinoma] (block xx): Estrogen receptor. POSITIVE ( > 90%). Progesterone receptor. PgR 636. POSITIVE (1-10%). HER-2/neu (c-erb-B2). NEGATIVE 0. B. HOT SPOT #1, AXILLA I, CT-xx: Immunohistochemical studies were performed on formalin fixed tissue with the following results for metastatic. carcinoma (block B): Keratin: NEGATIVE (…
- **Lu:** true value ____ · source ____ · notes ____

## 27. TCGA-BH-A1EX — `her2_ihc_status`

- **curated:** `positive`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `equivocal` — “HER-2/NEU IS INTERPRETED AS POSITIVE (SCORE 2+).”
- **gpt-4o:** `positive` — “HER-2/NEU IS INTERPRETED AS POSITIVE (SCORE 2+).”
- **context:** …0- 70%; 1+ 10%; 2+ 10%; 3+ 10%) HSCORE OF 60. PROGESTERONI RECEPTOR IS INTERPRETED AS. POSITIVE. HER-2/NEU-DAKO HERCEPTEST. A WEAK TO MODERATE COMPLETE MEMBRANE STAINING IS OBSERVED IN MORE THAN 10% OF THE. TUMOR CELLS. HER-2/NEU IS INTERPRETED AS POSITIVE (SCORE 2+). HSCORE: <= 15 NEGATIVE. >15<=30 BORDERLINE. FINAL DIAGNOSIS: FINAL DIAGNOSIS: A) RIGHT SENTINEL LYMPH NODE #1: - MICROMIETASTATIC DUCTAL CARCINOMA OF THE BREAST (SEE NOTE). B) RIGHT SEGMENTAL MASTECTOMY: INFILTRATING MO…
- **Lu:** true value ____ · source ____ · notes ____

## 28. TCGA-A2-A0D0 — `her2_ihc_score`

- **curated:** `0`  ·  auto tags: curated_vs_report_conflict
- **rules:** `1+` — “HER 2 NEU by IHC: NEGATIVE, 1+”
- **gpt-4.1:** `1+` — “HER 2 NEU by IHC: NEGATIVE, 1+ (REFER TO PRIOR SPECIMEN”
- **gpt-4o:** `1+` — “HER 2 NEU by IHC: NEGATIVE, 1+ (REFER TO PRIOR SPECIMEN.”
- **context:** … NODES NEGATIVE FOR TUMOR. NIPPLE INVOLVEMENT: ABSENT. SKIN INVOLVEMENT: ABSENT. MULTICENTRICITY: ABSENT. ESTROGEN RECEPTORS: NEGATIVE (REFER TO PRIOR SPECIMEN. PROGESTERONE RECEPTORS: NEGATIVE (REFER TO PRIOR SPECIMEN. HER 2 NEU by IHC: NEGATIVE, 1+ (REFER TO PRIOR SPECIMEN. PATHOLOGIC STAGE: pT2 NO MX. ADDITIONAL PATHOLOGIC FINDINGS: - PERIDUCTAL CHRONIC INFLAMMATION. B. SKIN, LEFT BREAST, EXCISION: - -UNREMARKABLE SKIN AND SUBCUTANEOUS SOFT TISSUE. - -NO EVIDENCE OF MALIGNANCY. 1. Specim…
- **Lu:** true value ____ · source ____ · notes ____

## 29. TCGA-AC-A23G — `her2_ish_status`

- **curated:** `amplified`  ·  auto tags: curated_vs_report_conflict
- **rules:** `not_amplified` — “FISH: NEGATIVE”
- **gpt-4.1:** `not_amplified` — “Her2 Gene Amplification By FISH: NEGATIVE”
- **gpt-4o:** `not_amplified` — “Her2 Gene Amplification By FISH: NEGATIVE. Average copies per cell: Her-2/neu: 1.82.”
- **context:** …: Block 2. TEST. REFERENCE RANGES. DNA Analysis by Image: DNA Index: SEE COMMENT. 0.9-1.1 is Diploid. < 0.9 or > 1.1 le Aneuploid. COMMENT: Insufficient tumor volume is present for quantitation of DNA by Image analysie. Her2 Gene Amplification By FISH: NEGATIVE. Average copies per cell: Her-2/neu: 1.82. Chromosome 17: 1.67. Ratio: 1.09. 20 Her2/neu. Case interpreted by. Notes: Quantitative analysis performed using Chromavision ACIS. The Her2 /neu and CEP17 probes are manufactu…
- **Lu:** true value ____ · source ____ · notes ____

## 30. TCGA-E9-A1N4 — `histologic_type`

- **curated:** `mixed_ductal_lobular`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `lobular` — “Histologic type: Lobular carcinoma”
- **gpt-4o:** `lobular` — “Histologic type: Lobular carcinoma.”
- **context:** …the. BREAST TISSUE CHECKLIST. Specimen type: Radical mastectomy. Specimen size: Not specified. Tumor site: Breast. Tumor size: 3 x 2.7 x 2 cm. Grossly evident lesion: Yes. Histologic type: Lobular carcinoma. Histologic grade: Tumor extent: Not specified. Lymph nodes: 4/7 positive for metastasis (Axillary 4/7). Left, upper. Extracapsular invasion of the lymph nodes: Not specified. inner. Margins: Not specified. quadrant. No…
- **Lu:** true value ____ · source ____ · notes ____

