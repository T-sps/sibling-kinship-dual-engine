"""静态资源加载（非核心模块）：基因座注册表 / 频率 / 阈值表。

所有数据从 data/ 目录的 JSON 读取，内容由团队依据国标人工录入。
"""
from __future__ import annotations
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def load_registry() -> dict:
    return _load("locus_registry.json")


def load_freqs() -> dict:
    return _load("allele_freqs.json")


def load_thresholds_ibs() -> dict:
    return _load("thresholds_ibs.json")


def load_thresholds_fsi() -> dict:
    return _load("thresholds_fsi.json")


def required_loci(registry: dict | None = None) -> list[str]:
    """返回参与 IBS/FSI 计算的必检基因座（排除性别位点）。"""
    reg = registry or load_registry()
    return [
        l["name"] for l in reg.get("loci", [])
        if l.get("required") and l.get("type") != "SEX"
    ]


def get_freq(freqs: dict, locus: str, allele: str) -> float:
    """返回某等位基因频率。表外等位基因按 rare_allele_rule 处理（待实现）。"""
    table = freqs.get("frequencies", {}).get(locus, {})
    if allele in table:
        return float(table[allele])
    # TODO: 按 rare_allele_rule 处理表外/稀有等位基因（待导师确认国标规则后实现）
    raise KeyError(
        f"等位基因 {allele} 不在 {locus} 频率表中，且 rare_allele_rule 尚未实现"
    )
