"""Acquire raw inputs (copy from sibling repos when present, else download), verify SHA-256, build the cohort."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"
HEALTHCARE = ROOT.parent

SOURCES = {
    "reports": {
        "file": "TCGA_Reports.csv.zip",
        "url": "https://raw.githubusercontent.com/jkefeli/tcga-path-reports/main/TCGA_Reports.csv.zip",
        "sha256": "bbbc0ee0c75d8feb0bb246b4fa40e8e29bba9775d4a9e4f41e0b73a7955e1c12",
        "license": "CC BY 4.0 (Mendeley Data DOI 10.17632/hyg5xkznpx.1); code repo MIT",
        "citation": "Kefeli J, Tatonetti N. TCGA-Reports: A machine-readable pathology report resource for benchmarking text-based AI models. Patterns 5(3):100933 (2024).",
        "local_copy": "tcga-multimodal-text-lab/data/raw/TCGA_Reports.csv.zip",
    },
    "report_cancer_type": {
        "file": "tcga_patient_to_cancer_type.csv",
        "url": "https://raw.githubusercontent.com/jkefeli/tcga-path-reports/main/data/tcga_metadata/tcga_patient_to_cancer_type.csv",
        "sha256": "acb7ac3aba8b2daa69aab493e94f06c289b1f3365a0bd07e09222b9c4af791b3",
        "license": "MIT (jkefeli/tcga-path-reports)",
        "citation": "Kefeli & Tatonetti 2024",
        "local_copy": "tcga-multimodal-text-lab/data/raw/tcga_patient_to_cancer_type.csv",
    },
    "clinical": {
        "file": "BRCA_clinicalMatrix",
        "url": "https://tcga.xenahubs.net/download/TCGA.BRCA.sampleMap/BRCA_clinicalMatrix",
        "sha256": "39eb3be0fb86e6a577bd2cc01502a7fa5a271e1e1cba294e9dc644ad99580d7f",
        "license": "UCSC Xena TCGA hub phenotype matrix; TCGA open-access clinical data (TCGA BCR clinical supplement), redistribution allowed",
        "citation": "Goldman MJ, et al. Visualizing and interpreting cancer genomics data via the Xena platform. Nat Biotechnol 2020. TCGA Research Network.",
        "local_copy": "research-cohort-explorer/data/raw/BRCA_clinicalMatrix",
    },
    "clinical_metadata": {
        "file": "BRCA_clinicalMatrix.json",
        "url": "https://tcga.xenahubs.net/download/TCGA.BRCA.sampleMap/BRCA_clinicalMatrix.json",
        "sha256": "62d77fb63892b7f2c000b2b7594a9d36edb20fc563875943e6278fb8ffe8085c",
        "license": "UCSC Xena dataset metadata",
        "citation": "UCSC Xena",
        "local_copy": "research-cohort-explorer/data/raw/BRCA_clinicalMatrix.json",
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def acquire() -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, s in SOURCES.items():
        dest = RAW / s["file"]
        obtained = "already present"
        if not dest.exists():
            src = HEALTHCARE / s["local_copy"]
            if src.exists():
                shutil.copy2(src, dest)
                obtained = f"copied read-only from sibling repo {s['local_copy']}"
            else:
                import requests  # optional; only needed when no local copy exists

                with requests.get(s["url"], stream=True, timeout=300) as r:
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                obtained = "downloaded"
        digest = sha256(dest)
        if digest != s["sha256"]:
            raise RuntimeError(f"SHA-256 mismatch for {dest}: {digest}")
        manifest[key] = {k: v for k, v in s.items() if k != "local_copy"} | {
            "bytes": dest.stat().st_size,
            "obtained": obtained,
            "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    return manifest


def load_reports() -> pd.DataFrame:
    with zipfile.ZipFile(RAW / "TCGA_Reports.csv.zip") as z:
        d = pd.read_csv(z.open("TCGA_Reports.csv"))
    d["patient_id"] = d["patient_filename"].str[:12]
    ct = pd.read_csv(RAW / "tcga_patient_to_cancer_type.csv")
    brca = set(ct.loc[ct.cancer_type == "BRCA", "patient_id"])
    d = d[d.patient_id.isin(brca)].copy()
    assert d.patient_id.is_unique, "expected one report per patient"
    d["tss"] = d.patient_id.str[5:7]
    return d[["patient_id", "patient_filename", "tss", "text"]].sort_values("patient_id").reset_index(drop=True)


def load_clinical_raw() -> pd.DataFrame:
    c = pd.read_csv(RAW / "BRCA_clinicalMatrix", sep="\t", low_memory=False, dtype=str)
    c["patient_id"] = c["sampleID"].str[:12]
    return c
