# 平台适配

> 本技能主用 Claude Code。在其他平台（Codex / Cowork / 纯提示词环境）运行时读本文件，把工具名映射到当前平台等价能力——找不到等价能力时走兜底，不能伪装"我有这个工具"。

## 工具映射表

| 能力 | Claude Code | Codex / Cowork | 兜底（纯提示词环境） |
|---|---|---|---|
| 子代理调度（并行 / 单） | Agent 工具 · 同消息发多个调用并发 | 按 `agents/openai.yaml` 映射到 Codex 子任务能力；若不支持 → 同会话兜底 | 同会话执行 · 严格按各模块"兜底"小节的清单走 |
| PDF 读取 | `anthropic-skills:pdf` | Codex 内置 PDF 阅读能力 | 提示研究员粘贴关键段落原文 |
| Word 读取 | `anthropic-skills:docx` | Codex 内置 Word 能力 | 同上 |
| Excel 读取 | `anthropic-skills:xlsx` | Codex 内置表格能力 | 同上 |
| PPT 读取 | `anthropic-skills:pptx` | Codex 内置 PPT 能力 | 同上 |
| 联网搜索 | 联网搜索工具 | Codex 内置联网能力 | 标"未联网·待补"，禁止假装查过 |
| 取原文（按 URL） | 取原文工具 | Codex 内置网页读取能力 | 同上 |

## 适配纪律

- 子代理派出后启动第一动作"工具自检"时，**用当前平台实际工具名做自检**，缺失的工具按上表降级
- 任何模块文档里写的 `anthropic-skills:*` 都是 Claude Code 形态——其他平台执行时自动按上表映射，不是字面要找叫这个名字的工具
- 平台兜底不是"豁免"——质量纪律不降（识别等级 / 12 字段 / 边界自检 / 硬配额仍然适用）
