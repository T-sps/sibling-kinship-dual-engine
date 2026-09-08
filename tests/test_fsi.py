"""FSI 引擎单测（测试脚手架 —— AI 可辅助）。

预期 CFSI / Log10(CFSI) 须取国标附录算例或导师李海霞论文
《两个已知全同胞参与的同胞鉴定分析》的已知值作为黄金标准填入。
"""
import pytest

from sibling_engine import engine_fsi


@pytest.mark.skip(reason="待团队录入频率表并实现 FSI 后，填入已知算例")
def test_fsi_known_case():
    # TODO: 取 GB/T 43641-2024 附录算例 / 李海霞论文已知值
    # alleles_a = ...
    # alleles_b = ...
    # expected_fsi = ...
    # assert abs(engine_fsi.fsi_locus(locus, a, b, freqs) - expected_fsi) < 1e-9
    pass
