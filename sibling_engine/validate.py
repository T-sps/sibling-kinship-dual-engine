"""数据三重校验（非核心模块）：完整性 / 合规性 / 一致性。

未通过校验的数据不进入计算。返回错误清单（空清单表示通过）。
"""
from __future__ import annotations
import re
from .models import Sample
from .dataio import required_loci, load_registry

# 等位基因命名规范示例（如 "10"、"29.2"），可按国标调整
ALLELE_RE = re.compile(r"^\d{1,2}(\.\d)?$")


def validate(samples: list[Sample], registry: dict | None = None) -> list[str]:
    errors: list[str] = []
    reg = registry or load_registry()
    req = set(required_loci(reg))

    for s in samples:
        present = s.loci_present()
        missing = req - present
        if missing:
            errors.append(f"[{s.id}] 缺失必检基因座: {sorted(missing)}")

        for locus, rec in s.records.items():
            for a in rec.alleles:
                if not ALLELE_RE.match(a):
                    errors.append(f"[{s.id}] {locus} 等位基因格式异常: '{a}'")
            if len(rec.alleles) > 2:
                errors.append(
                    f"[{s.id}] {locus} 出现 >2 个等位基因: {rec.alleles}（疑似三体/污染）"
                )
            # 一致性：杂合座两个等位不应被标成同一值之外的情况由上层判定
    return errors
