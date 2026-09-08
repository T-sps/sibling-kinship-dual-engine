# 全同胞关系鉴定双引擎智能计算系统

依据 **GB/T 43641-2024《生物学全同胞关系鉴定技术规范》**，基于 IBS + FSI 双引擎。

## 合规边界（务必遵守）
- ✅ **允许** AI/工具辅助：项目脚手架、数据录入模板、导入/校验/报告/界面等非核心模块、测试脚手架。
- ❌ **禁止** AI/工具参与：国标公式推导、IBS/FSI 引擎实现、结论性判定生成、阈值取值。这些由**团队成员人工实现**，代码注释标注国标条款出处（如 `# 依据 GB/T 43641-2024 附录X 表Y`），并经双人交叉审查。

## 当前状态
脚手架已就绪；4 份静态资源与两引擎为**空壳**，待人工录入/实现。

## 从零路线图
1. **环境**：`py -m venv .venv` → `.venv\Scripts\activate` → `pip install -r requirements.txt`
2. **录入 4 张表**（`data/*.json`）← 最关键、最先做，见 `data/README_RECORDING.md`
3. **实现 `engine_ibs.py`**（人工，依据国标）
4. **实现 `engine_fsi.py`**（人工，依据国标；用附录算例 / 李海霞论文验证）
5. **实现 `fusion.py`**（两引擎仲裁规则）
6. **跑通管线**：`python -m sibling_engine.cli <A.csv> <B.csv>`
7. 多体比对 / Word 报告 / Streamlit 界面 依次接上
8. 测试与优化

## 快速运行
```powershell
.venv\Scripts\activate
python -m sibling_engine.cli examples\sample_pair_example.csv examples\sample_pair_example.csv
pytest
```

## 关键风险（录入前须与导师拍板）
- 稀有/表外等位基因频率处理方法（最小频率 0.01？5/2n？）
- 缺失基因座处理（跳过并减 n？）
- 两引擎结论冲突的仲裁规则（国标是否明文规定？）
- 突变是否纳入 FSI 计算
