"""命令行入口（非核心模块）：导入 → 校验 → 双引擎 → 结论。

用法:
    python -m sibling_engine.cli <sample_a.csv> <sample_b.csv>

注：引擎实现前会以 NotImplementedError 提示，符合预期。
"""
from __future__ import annotations
import json
import sys

from . import engine_fsi, engine_ibs, fusion
from .dataio import (load_freqs, load_registry, load_thresholds_fsi,
                     load_thresholds_ibs, required_loci)
from .io_loader import load_samples_csv
from .validate import validate


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("用法: python -m sibling_engine.cli <sample_a.csv> <sample_b.csv>")
        return 1

    a_samples = load_samples_csv(argv[1])
    b_samples = load_samples_csv(argv[2])
    if len(a_samples) != 1 or len(b_samples) != 1:
        print("双体模式：每个文件须恰好 1 个样本")
        return 1
    A, B = a_samples[0], b_samples[0]

    reg = load_registry()
    errs = validate([A, B], reg)
    if errs:
        print("数据校验未通过：")
        for e in errs:
            print(" -", e)
        return 2

    loci = required_loci(reg)
    freqs = load_freqs()
    try:
        ibs = engine_ibs.compute_cibs(A, B, loci)
        ibs_v = engine_ibs.conclude_ibs(
            ibs["cibs"], ibs["n_loci"], load_thresholds_ibs()
        )
        fsi = engine_fsi.compute_cfsi(A, B, loci, freqs)
        fsi_v = engine_fsi.conclude_fsi(
            fsi["cfsi"], fsi["n_loci"], load_thresholds_fsi()
        )
        verdict = fusion.fuse(ibs_v, fsi_v)
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
    except NotImplementedError as e:
        print(f"[引擎未实现] {e}")
        print("→ 先完成 data/ 频率表录入与 engine_ibs/engine_fsi 的手工实现。")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
