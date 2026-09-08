"""Streamlit 快捷演示界面（非核心模块）。

⚠️ 当前为 MOCK 模式：计算结果使用内置模拟数据，仅用于展示页面布局。
真实引擎实现后，将 engine_ibs / engine_fsi 的计算函数接入即可。

启动：
    streamlit run app.py
"""
from __future__ import annotations

import io
import json
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="全同胞关系鉴定双引擎系统", layout="wide")


# ---------- Mock 数据与工具 ----------
LOCI = [
    "vWA", "D21S11", "D18S51", "D5S818", "D7S820",
    "D13S317", "D16S539", "FGA", "D8S1179", "D3S1358",
    "CSF1PO", "TH01", "TPOX", "Penta_E", "Penta_D",
    "D2S1338", "D19S433", "D12S391", "D6S1043",
]


def mock_genotype():
    """生成一个看起来合理的杂合或纯合基因型。"""
    a = np.random.randint(7, 18)
    if np.random.rand() > 0.6:
        return f"{a},{a}"
    b = np.random.randint(7, 18)
    while b == a:
        b = np.random.randint(7, 18)
    return f"{min(a,b)},{max(a,b)}"


def build_mock_samples(n=3):
    samples = {}
    for i in range(1, n + 1):
        samples[f"S{i:03d}"] = {loc: mock_genotype() for loc in LOCI}
    return samples


def mock_pair_result():
    cibs = np.random.randint(20, 45)
    log_cfsi = round(np.random.uniform(-3.0, 5.0), 3)
    if cibs >= 35 and log_cfsi >= 2.0:
        conclusion = "支持全同胞"
    elif cibs <= 25 and log_cfsi <= -1.0:
        conclusion = "不支持全同胞"
    else:
        conclusion = "无法判断"
    return {
        "CIBS": cibs,
        "n_loci": 19,
        "Log10(CFSI)": log_cfsi,
        "IBS结论": conclusion,
        "FSI结论": conclusion,
        "最终结论": conclusion,
    }


def genotype_table(sample_a: str, sample_b: str, data: dict):
    rows = []
    for loc in LOCI:
        rows.append({"基因座": loc, sample_a: data[sample_a][loc], sample_b: data[sample_b][loc]})
    return pd.DataFrame(rows)


# ---------- 页面布局 ----------
st.title("🔬 全同胞关系鉴定双引擎智能计算系统")
st.caption("依据 GB/T 43641-2024 | IBS + FSI 双引擎 | 当前为演示模式，结果系模拟数据")

mode = st.sidebar.radio("选择模式", ["双体鉴定", "多体比对"])

st.sidebar.markdown("---")
st.sidebar.info(
    "本界面用于快速预览系统功能。\n\n"
    "真实计算须待：\n"
    "1. data/ 下频率表录入完成\n"
    "2. engine_ibs / engine_fsi 人工实现\n"
    "3. 将 Mock 替换为真实调用"
)

# 示例数据开关
use_demo = st.checkbox("使用示例数据（不上传文件）", value=True)

uploaded = None
if not use_demo:
    uploaded = st.file_uploader(
        "上传 STR 分型数据（CSV/Excel，长格式：sample_id, locus, allele1, allele2）",
        type=["csv", "xlsx"],
    )

if mode == "双体鉴定":
    st.subheader("双体全同胞关系鉴定")

    col1, col2 = st.columns(2)
    with col1:
        sample_a = st.selectbox("样本 A", ["S001", "S002", "S003"], index=0)
    with col2:
        sample_b = st.selectbox("样本 B", ["S001", "S002", "S003"], index=1)

    if st.button("🚀 运行鉴定", type="primary"):
        with st.spinner("双引擎计算中..."):
            mock_samples = build_mock_samples(3)
            result = mock_pair_result()

        st.success("计算完成")

        # 关键指标卡片
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CIBS", result["CIBS"])
        m2.metric("有效基因座", result["n_loci"])
        m3.metric("Log₁₀(CFSI)", result["Log10(CFSI)"])
        m4.metric("最终结论", result["最终结论"])

        # 基因型比对表
        st.subheader("基因型比对表")
        df_gt = genotype_table(sample_a, sample_b, mock_samples)
        st.dataframe(df_gt, width="stretch")

        # 结论详情
        st.subheader("引擎判定详情")
        st.json(
            {
                "IBS引擎": {"CIBS": result["CIBS"], "结论": result["IBS结论"]},
                "FSI引擎": {"Log10(CFSI)": result["Log10(CFSI)"], "结论": result["FSI结论"]},
                "双引擎融合": result["最终结论"],
            }
        )

        # 报告下载
        report_text = f"""全同胞关系鉴定意见书（模拟）
样本：{sample_a} vs {sample_b}
CIBS：{result['CIBS']}
Log10(CFSI)：{result['Log10(CFSI)']}
结论：{result['最终结论']}
"""
        st.download_button(
            label="📄 下载鉴定报告（占位）",
            data=report_text,
            file_name=f"report_{sample_a}_{sample_b}.txt",
            mime="text/plain",
        )

else:
    st.subheader("多体全同胞关系比对")

    sample_ids = ["S001", "S002", "S003"]
    selected = st.multiselect("选择要比对的样本", sample_ids, default=sample_ids)

    if st.button("🚀 运行多体比对", type="primary"):
        if len(selected) < 2:
            st.warning("请至少选择 2 个样本")
        else:
            n = len(selected)
            matrix = np.random.randint(15, 45, size=(n, n))
            np.fill_diagonal(matrix, 40)  # 自己与自己最高
            df_matrix = pd.DataFrame(matrix, index=selected, columns=selected)

            st.subheader("关系热力图（CIBS）")
            fig, ax = plt.subplots(figsize=(6, 5))
            cax = ax.imshow(df_matrix.values, cmap="YlGnBu", vmin=15, vmax=45)
            ax.set_xticks(range(n))
            ax.set_yticks(range(n))
            ax.set_xticklabels(selected)
            ax.set_yticklabels(selected)
            for i in range(n):
                for j in range(n):
                    ax.text(j, i, df_matrix.iloc[i, j], ha="center", va="center", color="black")
            fig.colorbar(cax, ax=ax, label="CIBS")
            st.pyplot(fig)

            st.subheader("两两关系矩阵")
            st.dataframe(df_matrix, width="stretch")

            st.subheader("判定摘要")
            summary = []
            for a, b in combinations(selected, 2):
                r = mock_pair_result()
                summary.append({"样本对": f"{a}-{b}", "CIBS": r["CIBS"], "Log10(CFSI)": r["Log10(CFSI)"], "结论": r["最终结论"]})
            st.dataframe(pd.DataFrame(summary), width="stretch")

st.markdown("---")
st.caption("⚠️ 当前为 MOCK 演示模式 | 真实引擎接入后，所有数字将由 IBS + FSI 双引擎实际计算得出")
