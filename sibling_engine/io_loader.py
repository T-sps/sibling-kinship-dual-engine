"""STR 分型数据导入（非核心模块）。

CSV 长格式（每行一个 样本-基因座 记录）：
    sample_id,locus,allele1,allele2
    S001,D8S1179,10,12
    S001,D21S11,29,30
Excel(.xlsx) 同结构，经 pandas 读取。格式可按实际仪器导出调整。
"""
from __future__ import annotations
import csv
from pathlib import Path
from .models import GenotypeRecord, Sample


def load_samples_csv(path) -> list[Sample]:
    samples: dict[str, Sample] = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = (row.get("sample_id") or "").strip()
            locus = (row.get("locus") or "").strip()
            a = (row.get("allele1") or "").strip()
            b = (row.get("allele2") or "").strip()
            if not sid or not locus:
                continue
            alleles = tuple(x for x in (a, b) if x)
            s = samples.setdefault(sid, Sample(sid))
            s.records[locus] = GenotypeRecord(locus, alleles)
    return list(samples.values())


def load_samples_excel(path) -> list[Sample]:
    try:
        import pandas as pd
    except ImportError:
        raise RuntimeError("需安装 pandas: pip install pandas openpyxl")
    df = pd.read_excel(path, dtype=str).fillna("")
    samples: dict[str, Sample] = {}
    for _, row in df.iterrows():
        sid = str(row.get("sample_id", "")).strip()
        locus = str(row.get("locus", "")).strip()
        if not sid or not locus:
            continue
        a = str(row.get("allele1", "")).strip()
        b = str(row.get("allele2", "")).strip()
        alleles = tuple(x for x in (a, b) if x)
        s = samples.setdefault(sid, Sample(sid))
        s.records[locus] = GenotypeRecord(locus, alleles)
    return list(samples.values())
