# GitHub to RedNote 🚀

将 GitHub 仓库一键转换为小红书风格的技术文章。

**基于 OpenClaw 内置 Agent 能力 - 无需外部 LLM API**

## 功能特性

- 🔍 **智能数据获取** - 自动获取仓库信息、Releases、Contributors
- 🤖 **内置 Agent 生成** - 使用 OpenClaw 内置 Agent 完成内容创作，无需外部 API Key
- 📝 **5种文章模板** - 项目介绍、深度测评、使用教程、工具清单、版本发布
- 🎨 **5种写作风格** - 轻松随意、专业严谨、热情推荐、故事叙事、极简干练
- 💾 **智能缓存** - 缓存 GitHub API 响应，避免重复请求
- 📋 **一键复制** - 直接复制到剪贴板，方便发布

## 快速开始

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd github-to-rednote

# 安装依赖（可选，用于剪贴板功能）
pip install pyperclip
```

### 配置

**仅需设置 GitHub Token（必需）：**

```bash
export GITHUB_TOKEN="your_github_token_here"
```

**无需 LLM API Key！** 本工具使用 OpenClaw 内置的 Agent 能力完成内容生成。

### 使用

#### 基础用法

```bash
# 基本生成（项目介绍 + 轻松风格）
python3 scripts/generate_article.py https://github.com/pallets/flask

# 深度测评 + 专业风格
python3 scripts/generate_article.py https://github.com/torvalds/linux --template review --style professional

# 保存到文件
python3 scripts/generate_article.py https://github.com/microsoft/vscode -o vscode_article.txt

# 复制到剪贴板
python3 scripts/generate_article.py https://github.com/expressjs/express --clipboard
```

#### 查看可用选项

```bash
# 查看文章模板
python3 scripts/generate_article.py --list-templates

# 查看写作风格
python3 scripts/generate_article.py --list-styles
```

#### 高级用法

```bash
# 禁用缓存（强制刷新数据）
python3 scripts/generate_article.py https://github.com/golang/go --no-cache
```

## 文章模板

| 模板 | 说明 | 适用场景 |
|------|------|----------|
| `intro` | 项目介绍 | 快速了解项目，突出亮点 |
| `review` | 深度测评 | 详细分析优缺点，适合技术选型 |
| `tutorial` | 使用教程 | 入门指南，包含代码示例 |
| `list` | 工具清单 | 同类对比，适合系列推荐 |
| `release` | 版本发布 | 新特性解读，更新说明 |

## 写作风格

| 风格 | 说明 | 语气特点 |
|------|------|----------|
| `casual` | 轻松随意 | 像朋友聊天，口语化 |
| `professional` | 专业严谨 | 技术深度，数据驱动 |
| `enthusiastic` | 热情推荐 | 感染力强，强烈推荐 |
| `story` | 故事叙事 | 有情节，有代入感 |
| `minimal` | 极简干练 | 信息密度高，无废话 |

## 项目结构

```
github-to-rednote/
├── README.md              # 本文档
├── SKILL.md              # Skill 说明
├── manifest.yaml         # Skill 配置
├── prompts.md            # Prompt 设计文档
├── rednote-style.md      # 小红书风格指南
└── scripts/
    ├── generate_article.py    # 主脚本
    ├── github_api.py          # GitHub API 封装
    ├── llm_generator.py       # OpenClaw Agent 内容生成
    ├── formatters.py          # 小红书格式工具
    └── test_github_api.py     # 测试脚本
```

## API 说明

### GitHubAPI

```python
from scripts.github_api import GitHubAPI, GitHubCache

# 初始化（带缓存）
cache = GitHubCache(ttl_hours=1)
api = GitHubAPI(cache=cache)

# 获取仓库摘要
summary = api.get_repo_summary("https://github.com/pallets/flask")

# 数据包含：
# - stars, forks, watchers, issues
# - languages, topics, license
# - releases, contributors, recent_commits
# - readme 内容
```

### ArticleGenerator

```python
from scripts.llm_generator import OpenClawAgentClient, ArticleGenerator

# 初始化 Agent 客户端
client = OpenClawAgentClient()
generator = ArticleGenerator(client)

# 生成文章
article = generator.generate(
    repo_data=summary,
    template="intro",      # intro/review/tutorial/list/release
    style="casual"         # casual/professional/enthusiastic/story/minimal
)
```

### 格式化工具

```python
from scripts.formatters import RedNoteFormatter, format_rednote_article

formatter = RedNoteFormatter()

# 格式化标题
formatter.add_title_emoji("项目介绍", emoji="🔥")

# 格式化段落标题
formatter.format_section_header("核心特性")

# 格式化列表
formatter.format_bullet("快速轻量")
formatter.format_bullet("易于扩展", indent=1)

# 格式化仓库统计
formatter.format_repo_stats(stars=15000, forks=1200, language="Python")

# 一键格式化完整文章
article = format_rednote_article(
    content=content,
    title=title,
    repo_data=repo_data,
    tags=["#Python", "#开源"]
)
```

## 缓存机制

GitHub API 响应默认缓存 1 小时，缓存位置：`~/.cache/github-to-rednote/`

```python
from scripts.github_api import GitHubCache

# 查看缓存统计
cache = GitHubCache()
print(cache.stats())

# 清除缓存
cache.clear()
```

## 测试

```bash
# 运行完整测试套件
cd scripts
python3 test_github_api.py

# 测试单个仓库
python3 github_api.py https://github.com/pallets/flask

# 测试文章生成
python3 llm_generator.py https://github.com/pallets/flask intro casual
```

## 环境要求

- Python 3.8+
- GitHub Token（必需）
- OpenClaw 环境（用于 Agent 内容生成）

## 技术栈

- **GitHub API** - 仓库数据获取
- **OpenClaw Agent** - 内置内容生成
- **缓存** - 文件系统缓存（JSON）
- **输出格式** - 小红书风格 Markdown

## 变更日志

### v1.1.0 (2026-03-18)
- ✨ **重大更新**：从外部 LLM API 迁移到 OpenClaw 内置 Agent 能力
- 🔥 移除所有外部 LLM 配置需求（OpenAI、Anthropic、Moonshot、DeepSeek）
- 🎨 简化配置流程，仅需 GitHub Token

### v1.0.0
- 初始版本，支持多种 LLM 提供商

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 PR！

---

Made with ❤️ for the open source community
