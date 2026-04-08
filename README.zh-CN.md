# BPDU SlideGen

> English version: [:link: README.md](README.md)

一套为 BP Debate Union（BPDU）视觉风格生成自包含 HTML 幻灯片演示的 [Claude Code](https://claude.ai/code) 智能体技能集。

相当于 PPT，但以 HTML 呈现——支持键盘导航、无需构建步骤、输出为单文件。

## 技能

| 技能 | 触发词 | 功能 |
|------|--------|------|
| `deep-analysis` | *"Analyze the motion..."* | 对 BP 辩题进行战略性多层分析（利益相关方、冲突点、论点） |
| `slidegen` | *"Generate a slide deck on…"* | 根据主题或大纲生成带有品牌标识的单文件 HTML 演示 |
| `slide-theme` | *"Apply the BPDU theme to…"* | 将现有 HTML 演示更新为 BPDU 设计系统 |
| `slide-export-tips` | *"How do I export this to PDF?"* | 提供 HTML 导出 PDF/打印的建议 |
| `imagegen` | *"Generate an illustration for…"* | 通过 Gemini API 生成 BPDU 扁平卡通风格的插画 |

## 输出规格

每份生成的演示都是**单个 `.html` 文件**，具备：
- 键盘导航（`←` `→` `Space`）和触摸滑动
- 幻灯片计数器与进度条
- 每页固定 BPDU 品牌栏
- 素材全嵌入（除 Google Fonts CDN 外无外部依赖）

## 安装

### 第一步 — 安装 AI 编程智能体

任选其一：

**[Claude Code](https://claude.ai/code)**（推荐——技能在此环境下构建和测试）
```bash
npm install -g @anthropic-ai/claude-code
```

**[Gemini CLI](https://github.com/google-gemini/gemini-cli)**
```bash
npm install -g @google/gemini-cli
```

**[OpenCode](https://opencode.ai)**
```bash
curl -fsSL https://opencode.ai/install | bash
# 或：npm install -g opencode-ai
```

三者均需 **Node.js 20+**。

---

### 第二步 — 安装技能

**方式 A：Claude Code 内置安装（推荐）**

在 Claude Code 中运行：
```
/plugins install https://github.com/AntonySilverhand/BPDU-SlideGen
```
*注：这将安装本仓库中的所有技能。*

**方式 B：手动符号链接（面向开发者）**

如果你已克隆本仓库到本地并希望在编辑时同步更新：
```bash
./scripts/symlink.sh
```

**方式 C：单独安装（通过 agentskill.sh）**

如果你只需要部分技能：
```bash
ags install AntonySilverhand/BPDU-SlideGen@deep-analysis
ags install AntonySilverhand/BPDU-SlideGen@slidegen
# ... 以此类推
```

**手动安装**

克隆或下载本仓库，将 `skills/` 目录复制到你的项目根目录。

---

### 第三步 — 图片生成（可选）

`imagegen` 技能需要 Gemini API 密钥：

```bash
export GEMINI_API_KEY="你的密钥"
```

安装 Python 依赖：

```bash
python3 -m venv venv && source venv/bin/activate
pip install requests
```

## 使用方法

在 Claude Code 中描述你的需求即可调用任何技能：

```
Analyze the motion "THBT social media companies do more harm than good to democracy"
```

```
Generate a case file deck on the motion "This House Would ban social media for under-16s"
```

```
Generate an illustration of students debating, BPDU style, 16:9
```

```
Apply the BPDU theme to my existing presentation.html
```

## 设计系统

BPDU 视觉识别系统采用：
- **主色调：** `#F5C842`（暖琥珀色）
- **字体：** Poppins / Nunito / DM Sans
- **风格：** 暖色扁平卡通插画；大量留白；卡片式布局
- **正方 / 反方：** 蓝色 `#3B82F6` / 红色 `#EF4444`（BP 辩论惯例）

完整规格见 [`CLAUDE.md`](./CLAUDE.md)。

---

## 授权免责声明

本仓库及其技能以 MIT 许可证开源发布。

**使用这些工具生成的内容不代表 BP Debate Union，除非通过官方 BPDU 渠道明确发布。**

BPDU 官方发布渠道为 [bpdebate.club](https://bpdebate.club) 及 BPDU 认证社交账号。任何第三方使用本工具制作的幻灯片、文档或材料——即使包含 BPDU 品牌元素——均不构成 BPDU 官方声明，不得被表述为官方声明。

---

## 许可证

MIT © 2026 BP Debate Union

详见 [`LICENSE`](./LICENSE)。品牌素材（`BPDU_LOGO.png`、`BPDU_theme_image.png`）为 BP Debate Union 版权，不得用于歪曲与 BPDU 的隶属关系。
