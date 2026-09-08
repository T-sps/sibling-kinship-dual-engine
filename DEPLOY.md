# Streamlit Community Cloud 部署手册

> 目标：把本项目永久部署到公网，获得一个可分享给任何人的 URL。

## 前置条件
- 一个 GitHub 账号（免费注册：https://github.com/signup）
- 一个 Streamlit Community Cloud 账号（用 GitHub 登录：https://streamlit.io/cloud）

## 第一步：在 GitHub 创建仓库

1. 登录 GitHub，点击右上角 **+** → **New repository**。
2. 填写信息：
   - Repository name：`sibling-kinship-dual-engine`（或你喜欢的英文名）
   - Description：`全同胞关系鉴定双引擎智能计算系统`
   - 选择 **Public**（公开；Streamlit Cloud 免费版只支持公开仓库）
   - **不要**勾选 "Initialize this repository with a README"
3. 点击 **Create repository**。

创建后，GitHub 会显示类似下面的命令，复制 "…or push an existing repository from the command line" 那一段备用。

## 第二步：把本地代码推送到 GitHub

在 PowerShell 中进入项目目录执行：

```powershell
cd "C:\Users\HONOR\Desktop\DNA鉴定科研立项\sibling-engine"
git remote add origin https://github.com/你的用户名/sibling-kinship-dual-engine.git
git branch -M main
git push -u origin main
```

如果提示登录，按浏览器弹出的 GitHub 授权流程完成认证。

推送成功后，刷新 GitHub 仓库页面，应能看到所有文件。

## 第三步：在 Streamlit Cloud 部署

1. 访问 https://streamlit.io/cloud，用 GitHub 账号登录。
2. 点击 **Create app**。
3. 在 "Deploy an app" 页面：
   - Repository：`你的用户名/sibling-kinship-dual-engine`
   - Branch：`main`
   - Main file path：`app.py`
   - App URL：可自定义，如 `sibling-kinship-demo`
4. 点击 **Deploy**。

等待 1–3 分钟，部署完成后会显示公网 URL：

```
https://sibling-kinship-demo.streamlit.app
```

把这个链接发给导师、评委或队友即可。

## 后续代码更新

每次修改本地代码后：

```powershell
git add .
git commit -m "修改说明"
git push origin main
```

Streamlit Cloud 会自动重新部署。

## 注意事项

- 当前 `app.py` 为 **MOCK 演示模式**，结果系模拟数据，仅供界面预览。
- 待 `engine_ibs.py` / `engine_fsi.py` 真实实现并接入后，页面才会输出真实鉴定结论。
- 不要在本仓库中上传真实案件 DNA 数据。
