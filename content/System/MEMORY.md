# Long-Term Memory

## Preferences

### Search
- **Default search tool:** searxng skill (privacy-respecting local metasearch)
- When any web search is needed, prioritize the searxng skill over web_search (Brave API)
- SearXNG instance: configured via `SEARXNG_URL` env var (default: `http://localhost:8080`)

## Notes

- Memory file created: 2026-02-28
- User prefers privacy-focused search tools

## Core Principles (核心原则)

> **"你认为你记住的东西，那是你的幻觉。不靠脑子，靠文件。"**

**含义：**
- 所有重要信息必须写入文件才能持久保存
- 不要依赖短期记忆（context window）
- 文件是长期记忆的唯一可靠方式
- 每次会话都要读取相关文件来恢复记忆

**实践方式：**
- ✅ 用户说"记住这个" → 立即写入 `MEMORY.md` 或相关文件
- ✅ 完成重要任务 → 记录到 `memory/YYYY-MM-DD.md`
- ✅ 收录文章/配置 → 保存到 `obsidian-docs/` 并推送到 GitHub
- ✅ 每日总结 → 自动生成日报到 `content/Daily/`
- ✅ 定期整理 → 将每日笔记精华提炼到 `MEMORY.md`

**记录时间：** 2026-03-03

## Obsidian 文档仓库

- **地址：** https://kevin850115.github.io/oc-obdoc/
- **GitHub 仓库：** kevin850115/oc-obdoc
- **记录时间：** 2026-03-03
- **用途：** 用户长期记忆/个人知识库
