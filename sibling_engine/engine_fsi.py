"""FSI 引擎（核心模块 —— 人工硬编码，禁止 AI 实现）。

依据 GB/T 43641-2024，使用全同胞 IBD 系数 k0=1/4, k1=1/2, k2=1/4
与中国汉族人群等位基因频率计算似然比。
所有公式须由团队人工推导并逐行实现，代码注释标注国标条款出处。
"""
from __future__ import annotations
from .models import Sample


def fsi_locus(locus: str, alleles_a: tuple[str, ...], alleles_b: tuple[str, ...],
              freqs: dict) -> float:
    """单基因座全同胞指数 FSI = P(gA,gB | H_全同胞) / P(gA,gB | H_无关)。

    依据 GB/T 43641-2024 附录（基因型配对模式分情况公式表）。
    TODO(人工实现): 按基因型配对 case 查表硬编码，使用 dataio.get_freq 取频率。
    """
    raise NotImplementedError("FSI 须由团队依据 GB/T 43641-2024 人工实现")


def compute_cfsi(sample_a: Sample, sample_b: Sample, loci: list[str],
                 freqs: dict) -> dict:
    """复合全同胞指数 CFSI = Π FSI，并返回逐座明细与 Log10(CFSI)。

    依据 GB/T 43641-2024。
    返回: {"cfsi": float, "log10_cfsi": float, "n_loci": int, "per_locus": [...]}
    """
    raise NotImplementedError


def conclude_fsi(cfsi: float, n_loci: int, thresholds: dict) -> dict:
    """按 n_loci 查 Log10(CFSI) 阈值输出结论。

    依据 GB/T 43641-2024 阈值表。
    返回: {"conclusion": str, "log10_cfsi": ..., "threshold_used": ...}
    """
    raise NotImplementedError
