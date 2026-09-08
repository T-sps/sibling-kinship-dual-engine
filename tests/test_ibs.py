"""IBS 引擎单测（测试脚手架 —— AI 可辅助）。

预期值须由团队手算或取国标附录算例核对后确认。
引擎未实现前这些用例会报 NotImplementedError（预期行为）。
"""
from sibling_engine import engine_ibs


# (alleles_a, alleles_b, expected_ibs, description)
# TODO(团队确认): 把预期值换成按 GB/T 43641-2024 手算结果，并标注算例来源
CASES = [
    (("10", "12"), ("10", "12"), 2, "杂合相同"),
    (("10", "12"), ("10", "14"), 1, "杂合共享一个"),
    (("10", "12"), ("14", "15"), 0, "杂合无共享"),
    (("10", "10"), ("10", "12"), 1, "纯合 vs 杂合命中"),
    (("10", "10"), ("10", "10"), 2, "纯合相同"),
    (("10", "10"), ("12", "12"), 0, "纯合不同"),
    (("10", "10"), ("12", "14"), 0, "纯合 vs 杂合未命中"),
    ((), ("10", "12"), None, "A 缺失"),
    (("10", "12"), (), None, "B 缺失"),
]


def test_ibs_count_cases():
    for a, b, expected, desc in CASES:
        got = engine_ibs.ibs_count(a, b)
        assert got == expected, f"{desc}: {a} vs {b} 应为 {expected}，实际 {got}"
