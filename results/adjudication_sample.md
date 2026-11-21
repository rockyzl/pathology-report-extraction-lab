# Adjudication sample (UNREVIEWED)

30 held-out test (patient, field) pairs where gpt-4.1 or the rules baseline answered a value that differs from the curated TCGA value.
Sampled round-robin over fields, shuffled within field (seed 20261120). **Nothing here has been reviewed by a human yet.**

For each item, read the report context (and, if needed, the full report) and fill in the CSV columns `lu_true_value` (what this report says, or `not_in_report`),
`lu_source_of_disagreement` (one of: `extractor_error`, `curated_error_or_other_document`, `report_ambiguous_or_conflicting`, `multiple_specimens`, `ocr_noise`, `mapping_issue`) and `lu_notes`.

Report excerpts: TCGA-Reports (Kefeli & Tatonetti 2024), CC BY 4.0. `auto_tags` are automatic heuristics, not adjudications.

## 1. TCGA-E2-A14X — `er_status`

- **curated:** `negative`  ·  auto tags: extractors_conflict
- **rules:** `positive` — “ESTROGEN RECEPTOR. Positive”
- **gpt-4.1:** `negative` — “ER: Negative | ER: Negative Allred Score: 0 = Proportion Score 0 + Intensity Score. 0.”
- **gpt-4o:** `negative` — “ER: Negative Allred Score: 0 = Proportion Score 0 + Intensity Score. 0”
- **context:** …ic areas: fibroadenoma. DCIS present. Margins uninvolved by DCIS. DCIS Quantity: Estimate 5%. DCIS Type: Solid. DCIS Location: :Associated with invasive tumor. Nuclear grade: High. Necrosis: Present. ER/PR/HER2 Results. ER: Negative. PR: Negative. HER2: Negative by IHC. Pathological staging (pTN): pT 2 N 2. SYNOPTIC REPORT - BREAST, ER/PR RESULTS. Specimen: Surgical Excision. Block Number: A22 and F12 (lymph node). ER: Negative Allred Score: 0 = Pr…
- **Lu:** true value ____ · source ____ · notes ____

## 2. TCGA-AO-A03R — `pr_status`

- **curated:** `positive`  ·  auto tags: curated_vs_report_conflict
- **rules:** `negative` — “PR-”
- **gpt-4.1:** `negative` — “PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY”
- **gpt-4o:** `negative` — “PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY.”
- **context:** …lary contents. Block. Sect. Site. PCs. 1. bln. 1. 1. In. 1. Procedures/Addenda: Addendum. Date Complete: Addendum Diagnosis. ADDENDUM REPORT. SITE: LEFT BREAST (PART 4). ER: 95% NUCLEAR STAINING WITH MODERATE INTENSITY. PR: <5% NUCLEAR STAINING WITH MODERATE INTENSITY. HER2/NEU (HERCEPTEST) : NEGATIVE (STAINING INTENSITY OF 0). CONTROLS ARE SATISFACTORY. . M.D. Intraoperative Consultation: Note: The diagnoses given in this section pertain only to the tissue sample. examined at the ti…
- **Lu:** true value ____ · source ____ · notes ____

## 3. TCGA-AC-A3TN — `her2_ihc_status`

- **curated:** `positive`  ·  auto tags: multiple_specimens_or_sides
- **rules:** `[not_stated]`
- **gpt-4.1:** `negative` — “Her2/neu: 1+”
- **gpt-4o:** `negative` — “Her2/neu: 1+.”
- **context:** …nt metastasis (pM): Not applicable. Tumor Stage: IIB. RECEPTOR STATUS AND HER2/NEU: Biomarkers performed on. two separate core needle biopsies. Estrogen receptors: 95%. Progesterone receptors: 80% and 50%, respectively. Her2/neu: 1+. Printed: Acct No. Pathology Report - Page 3/6. - Page 3. Datient: FINAL SURGICAL PATHOLOGY REPORT. Ki-67 proliferative index: 1-2%. Source of Specimen: A. Sentinel lymph node;Sentinel node #1, Right breast. B. Breast;L…
- **Lu:** true value ____ · source ____ · notes ____

## 4. TCGA-E2-A1L6 — `her2_ihc_score`

- **curated:** `1+`  ·  auto tags: extractors_conflict
- **rules:** `2+` — “HER2 IHC results: A HER2, 2+”
- **gpt-4.1:** `1+` — “Interpretation: Negative. Intensity: 1+. % Tumor Staining: 40%”
- **gpt-4o:** `1+` — “Intensity: 1+.”
- **context:** …cinoma extends to within 3 mm. of the deep margin. Specimens Involved. Specimens: D: LEFT BREAST. HER2 Status Results, Immunohistochemistry Evaluation. SPECIMEN. Surgical Excision. Block Number: Block. D4. TEST RESULTS. Interpretation: Negative. Intensity: 1+. % Tumor Staining: 40%. FISH ORDERED. METHODOLOGY. Methodology: Fixation Type and Length: Tissue was fixed in 10% neutral buffered formalin. ) for no less than 8 and no longer than 24 hours. Antibody and Assay Methodology: Rabbit anti-human H…
- **Lu:** true value ____ · source ____ · notes ____

## 5. TCGA-BH-A18H — `her2_ish_status`

- **curated:** `equivocal`  ·  auto tags: multiple_specimens_or_sides,curated_vs_report_conflict
- **rules:** `not_amplified` — “FISH not amplified”
- **gpt-4.1:** `not_amplified` — “FISH not amplified | HER2/NEU (FISH): Not amplified”
- **gpt-4o:** `not_amplified` — “NEGATIVE FOR HER-2/NEU (IHC 2+, FISH not amplified)”
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

## 8. TCGA-A2-A04W — `pathologic_n`

- **curated:** `N1`  ·  auto tags: curated_vs_report_conflict
- **rules:** `N0` — “pT2 NO”
- **gpt-4.1:** `N0` — “PATHOLOGIC STAGE: pT2 NO (i+) MX (AJCC Stage II).”
- **gpt-4o:** `N0` — “PATHOLOGIC STAGE: pT2 NO (i+) MX (AJCC Stage II).”
- **context:** …SENT. MULTICENTRICITY ABSENT. ESTROGEN RECEPTORS: NEGATIVE (PREVIOUSLY EVALUATED FROM. PROGESTERONE RECEPTORS: NEGATIVE (PREVIOUSLY EVALUATED FROM. HER 2 NEU by IHC: POSITIVE (3+) (PREVIOUSLY EVALUATED FROM. $05-12958). PATHOLOGIC STAGE: pT2 NO (i+) MX (AJCC Stage II). ADDITIONAL PATHOLOGIC CHANGES CYSTIC CHANGE, SCLEROSING ADENOSIS,. FIBROADENOMATOID CHANGE, APOCRINE METAPLASIA. COMMENT: COMMENT #2 (. Specimen #: FINAL DIAGNOSIS (continued) : This case is amended to change the lymph …
- **Lu:** true value ____ · source ____ · notes ____

## 9. TCGA-BH-A0DD — `laterality`

- **curated:** `right`  ·  auto tags: extractors_conflict
- **rules:** `left` — “BREAST, LEFT”
- **gpt-4.1:** `right` — “LATERALITY: Right.”
- **gpt-4o:** `right` — “LATERALITY: Right.”
- **context:** …LE, LYMPH HISTOLOGICALLY NODES, NEGATIVE UNREMARKABLE FOR METASTATIC CARCINOMA (0/22). H. PATHOLOGIC STAGE (see comment): I. RECEPTOR STATUS (see comment). CASE SYNOPSIS: SYNOPTIC - PRIMARY INVASIVE CARCINOMA OF BREAST. LATERALITY: Right. PROCEDURE: Modified radical mastectomy. Upper inner quadrant. SIZE OF TUMOR: Maximum dimension invasive component: 3.0 cm. MULTICENTRICITY/MULTIFOCALITY OF INVASIVE FOCI: TUMOR TYPE (invasive component): Ductal adenocar…
- **Lu:** true value ____ · source ____ · notes ____

## 10. TCGA-B6-A0IH — `margin_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `close` — “margin close”
- **gpt-4.1:** `negative` — “ALL SURGICAL MARGINS APPEAR FREE OF INVOLVEMENT”
- **gpt-4o:** `negative` — “ALL SURGICAL MARGINS APPEAR FREE OF INVOLVEMENT”
- **context:** …PRESENT IN TWENTY FIVE OF TWENTY SEVEN (25/27). AXILLARY LYMPH NODES. SEE COMMENT. INFILTRATING CARCINOMA EXTENDS INTO SECTIONS OF LACTIFEROUS DUCT AND NIPPLE. AS WELL AS RANDOM SECTIONS OF BREAST QUADRANT. SEE COMMENT. ALL SURGICAL MARGINS APPEAR FREE OF INVOLVEMENT. COMMENT: Because of the multifocal and extensive nature of the tumor, exact. measurement are difficult to assess. Immunohistochemical staining for keratin on each block of lymphoid tissue. reveals extensive infiltratio…
- **Lu:** true value ____ · source ____ · notes ____

## 11. TCGA-E2-A14Y — `ln_examined`

- **curated:** `5`  ·  auto tags: extractors_conflict
- **rules:** `3` — “LYMPH NODE #1, RIGHT AXILLA, BIOPSY: - ONE LYMPH NODE, NO TUMOR SEEN (0/1) | LYMPH NODE #4, RIGHT AXILLA, BIOPSY: - TWO LYMPH NODES, NO TUMOR SEEN (0/2)”
- **gpt-4.1:** `5` — “Lymph node status: Negative 0/5”
- **gpt-4o:** `5` — “Lymph node status: Negative 0/5.”
- **context:** …r Score: 3. Nuclear Grade: 3. Mitotic Score: 3. Modified Scarff Bloom Richardson Grade: 3. Necrosis: Present. Vascular/Lymphatic Invasion: None identified. Lobular neoplasia: None. Lymph nodes: Sentinel lymph node only. Lymph node status: Negative 0/5. DCIS present. Margins uninvolved by DCIS. DCIS Quantity: Estimate 15%. DCIS Type: Solid. Cribriform. DCIS Location Both associated and separate from invasive tumor mass. Nuclear grade: High. Necrosis: Present. Location…
- **Lu:** true value ____ · source ____ · notes ____

## 12. TCGA-B6-A0WW — `ln_positive`

- **curated:** `5`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `8` — “METASTATIC CARCINOMA IN EIGHT OF 15 RIGHT AXILLARY. LYMPH NODES”
- **gpt-4o:** `8` — “LYMPH NODE STATUS: METASTATIC CARCINOMA IN EIGHT OF 15 RIGHT AXILLARY. LYMPH NODES.”
- **context:** …IVE INTRADUCTAL COMPONENT, NO. NIPPLE STATUS, FREE OF TUMOR. SKIN STATUS, FREE OF TUMOR. MUSCLE STATUS, NOT SAMPLED. STATUS OF NON-NEOPLASTIC BREAST TISSUE: FIBROSIS. SURGICAL MARGIN STATUS: NEGATIVE. LYMPH NODE STATUS: METASTATIC CARCINOMA IN EIGHT OF 15 RIGHT AXILLARY. LYMPH NODES. SIZE OF LARGEST LYMPH NODE METASTASIS 1.5 CM (SLIDE C14). EXTRANODAL INVASION PRESENT (SLIDE C14). ESTROGEN/PROGESTERONE RECEPTOR AND CELL CYCLE ANALYSIS PENDING. METHODOLOGY: IMMUNOHISTOCHEMISTRY, PARAFFIN BLOCK (C6).…
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

## 15. TCGA-BH-A0AZ — `her2_ihc_status`

- **curated:** `negative`  ·  auto tags: curated_vs_report_conflict
- **rules:** `equivocal` — “HER-2/NEU - EQUIVOCAL”
- **gpt-4.1:** `equivocal` — “HER-2/NEU - EQUIVOCAL”
- **gpt-4o:** `equivocal` — “HER-2/NEU - EQUIVOCAL”
- **context:** …ANGES. M. IMMUNOHISTOCHEMICAL STAINING FOR ESTROGEN RECEPTOR, PROGESTERONE RECEPTOR AND HER-. 2/NEU WERE PREVIOUSLY PERFORMED ON. WERE REPORTED AS FOLLOWS: ESTROGEN RECEPTOR - POSITIVE, PROGESTERONE RECEPTOR - POSITIVE, HER-2/NEU - EQUIVOCAL. (SCORE +2). HER-2/NEU BY FISH WAS NOT AMPLIFIED. PART 2: LYMPH NODE, RIGHT AXILLARY SENTINEL #1, BIOPSY -. METASTATIC ADENOCARCINOMA INVOLVING ONE LYMPH NODE (2C, 2D and 2E), WITH EXTRACAPSULAR. EXTENSION (2D) (1/1) (s…
- **Lu:** true value ____ · source ____ · notes ____

## 16. TCGA-EW-A1IW — `her2_ihc_score`

- **curated:** `3+`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `2+` — “HER2/neu. - Performed on another specimen: Results: Equivocal (Score 2+)”
- **gpt-4o:** `2+` — “HER2/neu. - Performed on another specimen: Results: Equivocal (Score 2+).”
- **context:** …ry Studies: Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%). Progesterone Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%). HER2/neu. - Performed on another specimen: Results: Equivocal (Score 2+). CISH for HER2/Neu: - Performed on another specimen: Results: Not amplified (HER2 gene copy <4.0 or ratio <1.8). TNM Descriptors: - m (multiple foci of invasive carcinoma). Primary Tumor (invasive Carcinoma) (pT). pT4b.…
- **Lu:** true value ____ · source ____ · notes ____

## 17. TCGA-E2-A109 — `her2_ish_status`

- **curated:** `not_amplified`  ·  auto tags: extractors_conflict
- **rules:** `amplified` — “FISH assay as amplified”
- **gpt-4.1:** `not_amplified` — “HER-2 NOT AMPLIFIED”
- **gpt-4o:** `not_amplified` — “HER-2 NOT AMPLIFIED | HER2/CEP17 ratio: 1.46”
- **context:** …thologists Guideline Recommendations for Human Epidermal Growth Factor Recepto 2. Testing in Breast Cancer. Arch of Path and Lab Med 2007; 131:18-43. PathVysion HER-2 DNA Probe Kit. Analytical Interpretation of Results: HER-2 NOT AMPLIFIED. Clinical Interpretation of results. Amplification of the HER-2 gene was evaluated with interphase fluorescence in-situ. hybridization (FISH) on formalin-fixed paraffin embedded tissue sections using a chromosome. 17 ce…
- **Lu:** true value ____ · source ____ · notes ____

## 18. TCGA-B6-A0RH — `histologic_type`

- **curated:** `ductal`  ·  auto tags: extractors_conflict
- **rules:** `other` — “infiltrating tubular”
- **gpt-4.1:** `ductal` — “INFILTRATING DUCTAL CARCINOMA AT THE JUNCTION OF INNER-UPPER AND INNER-. LOWER QUADRANT | The histologic pattern of this carcinoma, is similar to the so-called. cribriform ductal carcinoma | this carcinoma does. not fit in the category of cribriform carcinoma as defined by Page et al. The. lesion may be better regarded as infiltrating breast carcinoma of no special. type”
- **gpt-4o:** `ductal` — “INFILTRATING DUCTAL CARCINOMA AT THE JUNCTION OF INNER-UPPER AND INNER-. LOWER QUADRANT.”
- **context:** …ock A11), there is. a. focus of atypical ductal hyperplasia. No frank ductal, intraductal or. infiltrating carcinoma is observed at this site. DIAGNOSIS: "LEFT BREAST": LEFT MODIFIED RADICAL MASTECTOMY SPECIMEN WITH: 1. INFILTRATING DUCTAL CARCINOMA AT THE JUNCTION OF INNER-UPPER AND INNER-. LOWER QUADRANT. THE CANCER HAS A PREDOMINANTLY CRIBRIFORM PATTERN WITH AREAS OF COMEDO. NECROSIS; SEE COMMENT. THE TUMOR MEASURES 2.5 CM IN GREATEST DIMENSION. NSABP NUCLEAR GRADE MODERATELY DIFFERENTIATED, HISTOLOGIC GRADE 2 OF 3. LO…
- **Lu:** true value ____ · source ____ · notes ____

## 19. TCGA-A2-A3KD — `pathologic_t`

- **curated:** `T3`  ·  auto tags: curated_vs_report_conflict
- **rules:** `T2` — “pT2”
- **gpt-4.1:** `T2` — “PATHOLOGIC STAGE: pT2N1mi (”
- **gpt-4o:** `T2` — “PATHOLOGIC STAGE: pT2N1mi”
- **context:** …"B"). ESTROGEN RECEPTORS : POSITIVE (>95%, please see report. PROGESTERONE RECEPTORS: POSITIVE (90%, please see report. /. HER2NEU by IHC: NEGATIVE (Score 1+, please see report. Specimen #: FINAL DIAGNOSIS (continued) : PATHOLOGIC STAGE: pT2N1mi (. - ADDITIONAL PATHOLOGIC FINDINGS: STROMAL SCLEROSIS AND FOCAL MICROCYST FORMATION. FOCAL PRIOR BIOPSY SITE CHANGES. CLINICAL DIAGNOSIS AND HISTORY: Right breast cancer -year-old female. PRE-OPERATIVE DIAGNOSIS: None pr…
- **Lu:** true value ____ · source ____ · notes ____

## 20. TCGA-E9-A1N3 — `pathologic_n`

- **curated:** `N2`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `N1` — “Lymph nodes: 7/7 positive for metastasis (Regional 7/7).”
- **gpt-4o:** `[not_stated]`
- **context:** …tomy. Specimen size: Not specified. Tumor site: Breast. Tumor size: 1.8 x 1 x 1 cm. Grossly evident lesion: Yes. Histologic type: Infiltrating ductal and lobular carcinoma. Histologic grade: Tumor extent: Not specified. Lymph nodes: 7/7 positive for metastasis (Regional 7/7). Right,Jupper. Extracapsular invasion of the lymph nodes: Not specified. inner. Margins: Not specified. quadrant. Nottingham Histologic Score. Tubule formation: Not specified. Nuclear pleomorphism: Not specified. Mitotic…
- **Lu:** true value ____ · source ____ · notes ____

## 21. TCGA-LL-A50Y — `laterality`

- **curated:** `right`  ·  auto tags: multiple_specimens_or_sides,extractors_conflict
- **rules:** `left` — “Left breast”
- **gpt-4.1:** `right` — “Specimen Laterality: Right. | Pre-Op Diagnosis: Right breast lobular CA.”
- **gpt-4o:** `right` — “Specimen Laterality: Right.”
- **context:** …SUMMARY CHECKLIST. COMMENT (s). SURGICAL PATHOLOGY CANCER CASE SUMMARY - CAP APPROVED. Procedure: Total mastectomy (including nipple and skin). Lymph Node Sampling: Axillary dissection (partial or complete. dissection). Specimen Laterality: Right. Tumor Site: Other; multifocal. Histologic Type: Invasive lobular carcinoma. Tumor Size: Greatest dimension of largest focus of invasion. RUN DATE. RUN TIME. RUN USER. SPEC #: COMMENT (s). >1 mm: 30 mm (3.0 cm). Histolog…
- **Lu:** true value ____ · source ____ · notes ____

## 22. TCGA-A2-A0ST — `margin_status`

- **curated:** `negative`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `close` — “TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS”
- **gpt-4o:** `close` — “TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS.”
- **context:** …2. FINAL DIAGNOSIS: A. BREAST, RIGHT; EXCISION: - INFILTRATING DUCTAL CARCINOMA, POORLY DIFFERENTIATED (MODIFIED. BLOOM-RICHARDSON GRADE 9: MITOSES=3, NUCLEAR PLEOMORPHISM=3, TUBULE. FORMATION=3). -TUMOR SIZE 2.0 CM. - -TUMOR IS LESS THAN 0.1 CM FROM ANTERIOR AND MEDIAL SURGICAL MARGINS. - -ASSOCIATED FINDINGS: FIBROCYSTIC CHANGES INCLUDING STROMAL SCLEROSIS. AND MICROCYSTS. -MICROCALCIFICATIONS IDENTIFIED, ASSOCIATED WITH BENIGN BREAST TISSUE. - IMMUNOHISTOCHEMICAL STAINS FOR ESTROGEN AND PROGESTERONE…
- **Lu:** true value ____ · source ____ · notes ____

## 23. TCGA-E2-A1LI — `ln_examined`

- **curated:** `2`  ·  auto tags: extractors_conflict
- **rules:** `3` — “LYMPH NODE #1, LEFT AXILLA: -ONE LYMPH NODE, NO TUMOR SEEN (0/1) | Lymph nodes: Negative (0/2)”
- **gpt-4.1:** `2` — “Lymph nodes: Negative (0/2)”
- **gpt-4o:** `2` — “Lymph nodes: Negative (0/2).”
- **context:** …IS component. DCIS Quantity: <25%. DCIS Type: Clining. DCIS Location: outside main mass: diffuse. Nuclear grade: high. Necrosis: absent. Margins: DCIS present within 1 hpf of lateral and 1 mm of deep and medial margins. Lymph nodes: Negative (0/2). Stage, Pathology : T2N1. Hormone receptor status (by IHC): ER & PR: PENDING. HERCEPTEST (by IHC): Pending. ADDENDUM. The ER/PR/HER2 status of the invasive breast carcinoma was determined by immunohistochemistry. and qu…
- **Lu:** true value ____ · source ____ · notes ____

## 24. TCGA-BH-A0DD — `ln_positive`

- **curated:** `0`  ·  auto tags: curated_vs_report_conflict
- **rules:** `1` — “LYMPH NODES POSITIVE: 1”
- **gpt-4.1:** `1` — “LYMPH NODES POSITIVE: 1.”
- **gpt-4o:** `1` — “LYMPH NODES POSITIVE: 1.”
- **context:** …activity score: 3. Total Nottingham score: 8. Nottingham grade (1, 2, 3): 3. ANGIOLYMPHATIC INVASION: DERMAL LYMPHATIC INVASION: CALCIFICATION: SURGICAL MARGINS INVOLVED BY INVASIVE COMPONENT: PAGET'S DISEASE OF NIPPLE: LYMPH NODES POSITIVE: 1. LYMPH NODES EXAMINED: 23. METHOD(S) OF LYMPH NODE EXAMINATION: H/E stain. SIZE OF NODAL METASTASES: Diameter of largest lymph node metastasis: 30.0 mm. LYMPH NODE METASTASIS(-ES) WITH EXTRACAPSULAR EXTENSION: SKIN INVOL…
- **Lu:** true value ____ · source ____ · notes ____

## 25. TCGA-EW-A1IW — `er_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `negative` — “Estrogen Receptor: -”
- **gpt-4.1:** `positive` — “Estrogen Receptor: - Performed on another specimen: Results: Immunoreactive tumor cells present (1%)”
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

## 27. TCGA-BH-A42T — `her2_ihc_status`

- **curated:** `positive`  ·  auto tags: extractors_conflict
- **rules:** `negative` — “HER-2/NEU IMMUNOHISTOCHEMISTRY [NEGATIVE”
- **gpt-4.1:** `equivocal` — “HER-2/NEU. Equivocal. | HER-2/NEU IMMUNOHISTOCHEMISTRY [NEGATIVE:0,1+ EQUIVOCAL: 2+; POSITIVE: 3+]. SCORE. HER-2/NEU. Equivocal. 2+.”
- **gpt-4o:** `equivocal` — “HER-2/NEU. Equivocal. | HER-2/NEU IMMUNOHISTOCHEMISTRY [NEGATIVE:0,1+ EQUIVOCAL: 2+; POSITIVE: 3+]. SCORE. HER-2/NEU. Equivocal.”
- **context:** …PTORS: positive. PROGESTERONE RECEPTORS: positive. HER2/NEU: HER2/NEU (FISH): Equivocal. Addendum. BREAST TUMOR IMMUNOHISTOLOGY RESULTS. HER-2/NEU IMMUNOHISTOCHEMISTRY [NEGATIVE:0,1+ EQUIVOCAL: 2+; POSITIVE: 3+]. SCORE. HER-2/NEU. Equivocal. 2+. NOTE (for 2+ cases): HER2 FISH is being performed and the results will be subsequently reported in an addendum. SPECIAL PROCEDURES: FISH (PCL). Interpretation. nucish(D17Z1x2-3,ERBB2x2-6)(40]. Interphase FISH analys…
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
- **gpt-4o:** `not_amplified` — “Her2 Gene Amplification By FISH: NEGATIVE”
- **context:** …: Block 2. TEST. REFERENCE RANGES. DNA Analysis by Image: DNA Index: SEE COMMENT. 0.9-1.1 is Diploid. < 0.9 or > 1.1 le Aneuploid. COMMENT: Insufficient tumor volume is present for quantitation of DNA by Image analysie. Her2 Gene Amplification By FISH: NEGATIVE. Average copies per cell: Her-2/neu: 1.82. Chromosome 17: 1.67. Ratio: 1.09. 20 Her2/neu. Case interpreted by. Notes: Quantitative analysis performed using Chromavision ACIS. The Her2 /neu and CEP17 probes are manufactu…
- **Lu:** true value ____ · source ____ · notes ____

## 30. TCGA-E9-A1N4 — `histologic_type`

- **curated:** `mixed_ductal_lobular`  ·  auto tags: —
- **rules:** `[not_stated]`
- **gpt-4.1:** `lobular` — “Histologic type: Lobular carcinoma”
- **gpt-4o:** `lobular` — “Histologic type: Lobular carcinoma.”
- **context:** …the. BREAST TISSUE CHECKLIST. Specimen type: Radical mastectomy. Specimen size: Not specified. Tumor site: Breast. Tumor size: 3 x 2.7 x 2 cm. Grossly evident lesion: Yes. Histologic type: Lobular carcinoma. Histologic grade: Tumor extent: Not specified. Lymph nodes: 4/7 positive for metastasis (Axillary 4/7). Left, upper. Extracapsular invasion of the lymph nodes: Not specified. inner. Margins: Not specified. quadrant. No…
- **Lu:** true value ____ · source ____ · notes ____

