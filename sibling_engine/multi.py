"""多体比对（非核心模块）：两两组合拆矩阵，批量调双引擎，聚合关系矩阵。

依赖 engine_ibs / engine_fsi（待人工实现后即可接通）。
"""
from __future__ import annotations
from itertools import combinations
from .models import Sample


def pairwise_index(n: int) -> list[tuple[int, int]]:
    """返回 n 个样本的所有两两组合下标。"""
    return list(combinations(range(n), 2))


def build_pair_matrix(samples: list[Sample], loci: list[str], freqs: dict,
                      compute_fn) -> dict:
    """对每对样本调用 compute_fn(sample_a, sample_b, loci, freqs)，
    聚合成 { (i,j): result } 矩阵。compute_fn 由上层注入（双体引擎）。

    热力图数据可由本矩阵的标量字段（如 CIBS 或 Log10(CFSI)）派生。
    """
    results: dict[tuple[int, int], dict] = {}
    for i, j in pairwise_index(len(samples)):
        results[(i, j)] = compute_fn(samples[i], samples[j], loci, freqs)
    return results
