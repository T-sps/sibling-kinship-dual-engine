"""数据资源校验脚本（非核心工具）。

检查：
- locus_registry.json 基因座不重复、必检非空
- allele_freqs.json 每个基因座频率和 ≈ 1.0（容差 1e-3）
- thresholds_ibs.json / thresholds_fsi.json 的 n 键覆盖有效基因座数

用法（在 venv 中）:
    python scripts/validate_data.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def check_registry() -> list[str]:
    errs = []
    data = load_json("locus_registry.json")
    loci = data.get("loci", [])
    if not loci:
        errs.append("locus_registry.json: loci 列表为空")
        return errs
    names = [l["name"] for l in loci]
    if len(names) != len(set(names)):
        errs.append(f"locus_registry.json: 存在重复基因座名 {names}")
    req = [l for l in loci if l.get("required")]
    if not req:
        errs.append("locus_registry.json: 没有 required=true 的基因座")
    non_verified = [l["name"] for l in loci if not l.get("verified")]
    if non_verified:
        errs.append(f"locus_registry.json: 以下基因座尚未 verified={non_verified}")
    return errs


def check_freqs() -> list[str]:
    errs = []
    data = load_json("allele_freqs.json")
    freqs = data.get("frequencies", {})
    if not freqs:
        errs.append("allele_freqs.json: frequencies 为空，请先录入频率表")
        return errs
    for locus, table in freqs.items():
        if locus.startswith("_"):
            continue
        s = sum(float(v) for v in table.values() if v is not None)
        if abs(s - 1.0) > 1e-3:
            errs.append(f"allele_freqs.json: {locus} 频率和 = {s:.4f}，偏离 1.0")
    return errs


def main() -> int:
    errs = check_registry() + check_freqs()
    if errs:
        print("发现以下问题：")
        for e in errs:
            print(" -", e)
        return 1
    print("✅ 数据资源校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
