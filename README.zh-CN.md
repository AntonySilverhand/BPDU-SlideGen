# BPDU SlideGen

> English version: [:link: README.md](README.md)

一套为 BP Debate Union（BPDU）视觉风格生成自包含 HTML 幻灯片演示的 [Claude Code](https://claude.ai/code) 智能体技能集。

相当于 PPT，但以 HTML 呈现——支持键盘导航、无需构建步骤、输出为单文件。

## 技能

| 技能 | 触发词 | 功能 |
|------|--------|------|
| `deep-analysis` | *"Analyze the motion..."* | 对 BP 辩题进行战略性多层分析（利益相关方、冲突点、论点） |
| `slidegen` | *"Generate a slide deck on…"* | 生成带有品牌标识的单文件 HTML 演示、辩题资料包、活动主持稿或邀请函 |
| `imagegen` | *"Generate an illustration for…"* | 通过 Gemini API 生成 BPDU 扁平卡通风格的插画 |

## 输出规格

每份生成的演示都是**单个 `.html` 文件**（约 20–80 KB），具备：
- 键盘导航（`←` `→` `Space`）和触摸滑动
- 幻灯片计数器与进度条
- 每页固定 BPDU 品牌栏
- 品牌图片从 `bpdebate.club` CDN 加载（需网络连接）

> **v1.0.0 变更：** 图片现从托管 URL 加载，不再使用 base64 嵌入。文件体积缩小约 50 倍。如需离线使用，请运行 `embed-images.py` 的 base64 模式。

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

## 脚本工具

| 脚本 | 用途 |
|------|------|
| `scripts/embed-images.py` | 将品牌图片 URI 写入 `.logo_uri.txt` / `.theme_uri.txt`。默认模式编码 base64；使用 `--url` 获取 CDN 地址。 |
| `scripts/validate.py` | 生成后验证：检查品牌栏、`.illo`、CONFIG、文件大小等。 |

### 图片嵌入模式

```bash
# CDN 模式（v1.0+ 默认）— 文件保持约 20–80 KB
python3 skills/slidegen/scripts/embed-images.py --url \
  https://bpdebate.club/wp-content/uploads/2025/05/cropped-ChatGPT-Image-May-8-2025-10_18_18-PM.png \
  https://bpdebate.club/wp-content/uploads/2025/12/Untitled-design-3-1.png

# Base64 模式 — 用于完全离线演示（约 2.7 MB）
python3 skills/slidegen/scripts/embed-images.py
```

## 演示类型

| 类型 | 适用场景 | 大小 |
|------|----------|------|
| **Reference（参考）** | 密集阅读材料、辩论规则 | 约 30–50 KB |
| **Case File（辩题资料）** | 辩题简报、论点卡片、冲突分析 | 约 30–60 KB |
| **Event Host（活动主持）** | 现场投影、每页一个要点、大字体 | 约 15–30 KB |
| **Invitation / Email（邀请函）** | HTML 邮件邀请评委、嘉宾、参赛者 | 约 15–25 KB |

## 使用方法

在 Claude Code 中描述你的需求即可调用任何技能：

```
Analyze the motion "THBT social media companies do more harm than good to democracy"
```

```
Generate a case file deck on the motion "This House Would ban social media for under-16s"
```

```
Generate an event host deck for our weekly round on May 23
```

```
Generate a judge invitation email for the Bowen Cup tournament
```

```
Generate an illustration of students debating, BPDU style, 16:9
```

```
Validate tmp/my-deck.html
```

## 设计系统

BPDU 视觉识别系统采用：
- **主色调：** `#F5C842`（暖琥珀色）
- **字体：** Poppins / Nunito / DM Sans
- **风格：** 暖色扁平卡通插画；大量留白；卡片式布局
- **正方 / 反方：** 蓝色 `#3B82F6` / 红色 `#EF4444`（BP 辩论惯例）

完整规格见 [`CLAUDE.md`](./CLAUDE.md)。

---

## 更新日志

### v1.0.0 — 2026-05-11

- **CDN 优先图片：** 品牌素材现从 `bpdebate.club` URL 加载，不再使用 base64 嵌入。生成文件体积缩小约 50 倍（约 20–80 KB 对比约 2.7–5.3 MB）。
- **`embed-images.py --url`：** 新增标志，将托管 URL 写入 `.logo_uri.txt` / `.theme_uri.txt`。base64 模式仍可用于离线场景。
- **`validate.py`：** 新增生成后验证脚本。检查品牌栏、`.illo`/`.closing-illo`、Event Host 的 `CONFIG`、`.slide` 上无 `display:none`、文件大小合理性。
- **Invitation Letter / Email 演示类型：** 新增品牌 HTML 邮件生成功能，用于邀请评委、嘉宾、参赛者。
- **SKILL.md 加固：** 新增 `anti-triggers`、`allowed-tools`、`metadata`、负面约束和「完成前检查」验证清单。
- **简化工作流：** 移除占位符 + 注入步骤。URL 直接写入生成的 HTML。
- **批量修复现有文件：** 16 份现有 HTML 演示从 base64 更新为 URL。

### v0.x — v1 之前

- 初始技能集：`slidegen`、`deep-analysis`、`slide-theme`、`slide-export-tips`、`imagegen`。
- Base64 嵌入品牌图片，实现完全自包含的离线演示。
- 73 块模板库（`slide-templates.html`）。

---

## 授权免责声明

本仓库及其技能以 MIT 许可证开源发布。

**使用这些工具生成的内容不代表 BP Debate Union，除非通过官方 BPDU 渠道明确发布。**

BPDU 官方发布渠道为 [bpdebate.club](https://bpdebate.club) 及 BPDU 认证社交账号。任何第三方使用本工具制作的幻灯片、文档或材料——即使包含 BPDU 品牌元素——均不构成 BPDU 官方声明，不得被表述为官方声明。

---

## 许可证

MIT © 2026 BP Debate Union

详见 [`LICENSE`](./LICENSE)。品牌素材（`BPDU_LOGO.png`、`BPDU_theme_image.png`）为 BP Debate Union 版权，不得用于歪曲与 BPDU 的隶属关系。
