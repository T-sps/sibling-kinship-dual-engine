"""IBS 引擎（核心模块 —— 人工硬编码，禁止 AI 实现）。

依据 GB/T 43641-2024《生物学全同胞关系鉴定技术规范》。
所有公式须由团队成员人工推导并逐行实现，代码注释标注国标条款出处。
"""
from __future__ import annotations
from .models import Sample


def ibs_count(alleles_a: tuple[str, ...], alleles_b: tuple[str, ...]) -> int:
    """单基因座 IBS 评分：数两个基因型共享的等位基因数（0/1/2）。

    依据 GB/T 43641-2024 第 X 条 / 表 Y（请按原文替换条款号）。

    输入约定（与 models.GenotypeRecord 一致）：
      - 缺失：()
      - 纯合子：(a, a)
      - 杂合子：(a, b)，通常约定 a != b

    计算规则（仅作实现参考，须以国标原文为准）：

    1. 任一基因型缺失 → 该基因座 IBS 记为 None，不参与 CIBS 累计，
       有效基因座数 n 相应减 1（具体缺失处理规则见国标）。

    2. 均为纯合子：
         (a,a) vs (a,a)  → 2
         (a,a) vs (b,b)  → 0  (a != b)

    3. 均为杂合子（去重后比较）：
         (a,b) vs (a,b)  → 2
         (a,b) vs (a,c)  → 1  (b != c)
         (a,b) vs (c,d)  → 0  {a,b} 与 {c,d} 无交集

    4. 纯合子 vs 杂合子：
         (a,a) vs (a,b)  → 1
         (a,a) vs (b,c)  → 0  (a 不在 {b,c} 中)

    实现伪代码（供参考）：
      if not alleles_a or not alleles_b:
          return None
      set_a = set(alleles_a)
      set_b = set(alleles_b)
      shared = len(set_a & set_b)
      # 纯合子 vs 纯合子相同应得 2，纯合 vs 杂合命中应得 1，
      # 上述集合交集长度已涵盖：
      #   (10,10)&{10,12} = {10} -> 1
      #   (10,10)&{10,10} = {10} -> 1，但期望是 2，需特判纯合同型
      if len(set_a) == 1 and len(set_b) == 1 and set_a == set_b:
          return 2
      return min(shared, 2)

    返回：
      int 或 None。None 表示该座缺失/无效，不计入 CIBS。
    """
    raise NotImplementedError("IBS 评分须由团队依据 GB/T 43641-2024 人工实现")


def compute_cibs(sample_a: Sample, sample_b: Sample, loci: list[str]) -> dict:
    """累计 IBS 评分（CIBS）与逐座明细。

    依据 GB/T 43641-2024。

    处理要点（须以国标原文为准）：
      1. 遍历 loci 列表中的每个基因座；
      2. 用 sample_a.alleles_at(locus) 与 sample_b.alleles_at(locus) 取基因型；
      3. 调用 ibs_count() 得单座 IBS；
      4. 若 ibs_count 返回 None，该座跳过，n_loci 不减入；
      5. 否则 ibs 累加，得到 CIBS；
      6. 记录 per_locus 明细，便于报告生成与复核。

    返回示例：
      {
        "cibs": 35,
        "n_loci": 19,
        "per_locus": [
          {"locus": "D8S1179", "alleles_a": ["10","12"], "alleles_b": ["10","12"], "ibs": 2},
          ...
        ]
      }
    """
    raise NotImplementedError


def conclude_ibs(cibs: int, n_loci: int, thresholds: dict) -> dict:
    """按 n_loci 查 CIBS 阈值，输出 '支持全同胞 / 无法判断 / 不支持'。

    依据 GB/T 43641-2024 附录阈值表（thresholds_ibs.json）。

    thresholds 结构（由 dataio.load_thresholds_ibs() 读取）：
      {
        "by_n_loci": {
          "19": {"support_ge": X, "undetermined_range": [L, U], "no_support_le": Y},
          ...
        }
      }

    判定逻辑（参考）：
      - cibs >= support_ge            → "支持全同胞"
      - cibs <= no_support_le         → "不支持全同胞"（或"支持无关"）
      - L <= cibs <= U                → "无法判断"
      - 若 cibs 接近阈值边界，附加 "margin" 提示临界预警

    注意： thresholds 的键为字符串化的 n_loci，使用前需 str(n_loci)。
    """
    raise NotImplementedError
