"""数据模型（非核心模块）。

基因型与样本的规范表示。仅定义数据结构，不涉及任何国标公式。
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GenotypeRecord:
    locus: str
    alleles: tuple[str, ...]   # 纯合: ("10","10"); 杂合: ("10","12"); 缺失: ()

    @property
    def is_missing(self) -> bool:
        return len(self.alleles) == 0


@dataclass
class Sample:
    id: str
    records: dict[str, GenotypeRecord] = field(default_factory=dict)

    def alleles_at(self, locus: str) -> tuple[str, ...]:
        rec = self.records.get(locus)
        return rec.alleles if rec else ()

    def loci_present(self) -> set[str]:
        return set(self.records)
