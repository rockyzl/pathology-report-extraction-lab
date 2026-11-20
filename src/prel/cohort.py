"""Cohort assembly and the deterministic patient-level dev/test split."""
from __future__ import annotations

import hashlib
import json

import pandas as pd

from . import data
from .schema import FIELDS, map_curated

SPLIT_SALT = "pathology-extraction-v1"
LLM_DEV_SALT = "pathology-extraction-llm-dev-v1"
TEST_FRACTION = 0.25
LLM_DEV_N = 80


def _h(pid: str, salt: str) -> str:
    return hashlib.sha256(f"{pid}|{salt}".encode()).hexdigest()


def assign_split(patient_ids: list[str], salt: str = SPLIT_SALT, test_fraction: float = TEST_FRACTION) -> dict[str, str]:
    """Patient-level split: sort unique patient IDs by SHA256(pid|salt); first round(f*n) are test. No outcome is read."""
    pids = sorted(set(patient_ids), key=lambda p: _h(p, salt))
    n_test = round(test_fraction * len(pids))
    return {p: ("test" if i < n_test else "dev") for i, p in enumerate(pids)}


def llm_dev_sample(dev_ids: list[str], n: int = LLM_DEV_N) -> list[str]:
    return sorted(sorted(set(dev_ids), key=lambda p: _h(p, LLM_DEV_SALT))[:n])


def build() -> dict:
    reports = data.load_reports()
    clin = data.load_clinical_raw()
    cols = sorted({FIELDS[f]["curated"] for f in FIELDS} | {"histological_type_other"})
    # clinical columns are patient-level and identical across a patient's sample rows (checked here)
    nun = clin.groupby("patient_id")[cols].nunique(dropna=False).max()
    assert (nun <= 1).all(), f"curated values differ across samples: {nun[nun > 1]}"
    clin = clin.sort_values("sampleID").drop_duplicates("patient_id")
    clin = clin[clin.patient_id.isin(reports.patient_id)]
    curated = pd.DataFrame([{"patient_id": r["patient_id"], **map_curated(r)} for r in clin[["patient_id"] + cols].to_dict("records")])
    reports = reports[reports.patient_id.isin(curated.patient_id)].reset_index(drop=True)
    split = assign_split(reports.patient_id.tolist())
    reports["split"] = reports.patient_id.map(split)
    curated["split"] = curated.patient_id.map(split)
    data.DERIVED.mkdir(parents=True, exist_ok=True)
    reports.to_json(data.DERIVED / "reports.jsonl", orient="records", lines=True, force_ascii=False)
    curated.to_csv(data.DERIVED / "curated.csv", index=False)
    dev = sorted(reports.loc[reports.split == "dev", "patient_id"])
    test = sorted(reports.loc[reports.split == "test", "patient_id"])
    membership = {"split_rule": f"sort unique patient IDs by SHA256(patient_id|{SPLIT_SALT}); first round({TEST_FRACTION}*n) are test",
                  "llm_dev_rule": f"sort dev patient IDs by SHA256(patient_id|{LLM_DEV_SALT}); first {LLM_DEV_N}",
                  "dev": dev, "test": test, "llm_dev_sample": llm_dev_sample(dev)}
    return {"reports": reports, "curated": curated, "membership": membership}


def load_reports() -> pd.DataFrame:
    return pd.read_json(data.DERIVED / "reports.jsonl", lines=True, dtype={"tss": str})


def load_curated() -> pd.DataFrame:
    return pd.read_csv(data.DERIVED / "curated.csv", dtype=str, keep_default_na=False).replace("", None)


def load_membership() -> dict:
    return json.loads((data.ROOT / "data" / "membership.json").read_text())
