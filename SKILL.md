---
name: full-research
description: Use when the user asks for 综合研究, 行业研究, 政策研究, 软科学研究, 课题研究, 趋势/影响分析, 判断命题是否成立, 研究报告, 成熟报告体例, 成稿, 证据矩阵, 反方审稿, 研究假设, or 分层建议, especially when the model must form an evidence-backed judgment under uncertainty. For a fast one-shot demo report instead (一键出报告 / 5 分钟简报 / 演示用), use quick-research.
---

# 综合研究六步法

> **本文件是导航页。** 只放路由 + 核心纪律 + 指针。执行细节按需加载对应模块 / reference——不要一次性把所有内容读进上下文。

## 概述

本技能把宽泛研究题目收敛为有判断、有证据、有边界的研究产出。核心规则：AI 负责展开、整理、对比、起草、批评，研究员负责最终判断、证据采纳、建议强度。

面向"判断导向"的研究，不做综述。只要事实性说明 → 按普通对话答。要判断某事是否为真/重要/可行/风险/值得做 → 用本技能。

## 请求路由

按用户输入选最轻路径。

| 用户输入 | 模式 | 加载什么 |
|---|---|---|
| 宽题目、新任务、"帮我研究一下 X" | 完整研究流程 | 每次只加载一个模块，从 `modules/01_problem_definition.md` 开始 |
| "先给我完整草稿"、"一次性走完"、或时间紧 | 一次性草稿模式 | 六步走完，假定项显式标"待研究员审核" |
| 单项请求：证据矩阵 / 反方审稿 / 假设清单 / 建议分层 | 单模块 | 只加载对应模块 |
| 现有报告 + 证据 | 复查 / 优化 | 通常加载 `modules/05_red_team_review.md`，需要建议时再加 `modules/06_recommendation_layering.md` |
| 已有过程稿 / 方法论稿 / 研究笔记，要转成读者面向的成熟报告 | 报告成稿 | 加载 `modules/07_report_assembly.md` + `references/report_style_guide.md` + `assets/mature_report_template.md`。除非草稿缺核心判断或证据，否则跳过 01–06 |
| "出报告"、"成稿"、"成熟报告体例"、或六步法完成后的最终交付 | 报告成稿 | 同上 |

完整研究默认走"分阶段交互"——每模块结束后展示阶段产出，请研究员逐条确认判断点，才进下一模块。**不要**一次性把所有模块读进上下文。

## 七大模块

| 步 | 模块 | 目的 | 产出 | 配套文件 |
|---|---|---|---|---|
| 1 | `modules/01_problem_definition.md` | 把宽题收敛为 1-3 个判断问题；登记本地资料 | 主问题、边界声明、本地资料登记表 | 案例参考；`references/local_materials_protocol.md`（若有本地资料） |
| 2 | `modules/02_framework_convergence.md` | 把主问题拆为可验证子判断 | 判断框架 | `references/judgment_framework_patterns.md`；可选 `references/consulting_frameworks_cheatsheet.md` |
| 3 | `modules/03_hypothesis_generation.md` | 生成正/反假设 + 证伪条件 | 假设清单 | —— |
| 4 | `modules/04_evidence_matrix.md` | 把证据映射到假设并标证据边界 | 证据矩阵（12 字段）+ 待复核清单 + 缺口清单 | `references/evidence_sourcing_protocol.md` + `references/local_materials_protocol.md`（均必读）；`subagents/fact-checker-prompt.md` + `references/subagent_dispatch.md`（并行调度） |
| 5 | `modules/05_red_team_review.md` | 找无证据陈述、过头结论、口径不一致 | 风险与改稿清单 | `subagents/reviewer-prompt.md` + `references/subagent_dispatch.md` |
| 6 | `modules/06_recommendation_layering.md` | 把结论转成观察/研究/行动三层建议 | 分层建议草稿 | —— |
| 7 | `modules/07_report_assembly.md` | 把研究过程产出转成成熟报告 + 完整交付包 | 最终报告 + 待复核清单 + 跨模块待研究员补汇总 | `references/report_style_guide.md`；`assets/mature_report_template.md` |

战略/行业框架类工作，仅当模块 2 需要更多候选框架时才读 `references/consulting_frameworks_cheatsheet.md`。案例只读 `references/cases/` 中最贴近的那一个。最终报告阶段不要停在模块 6——永远加载模块 7，并把六步法脚手架从读者面向报告里隐去。

## 子代理模式（隔离上下文消除确认偏差）

核心审视动作（事实核查、反方审稿）派子代理在无主会话历史的环境执行——消除确认偏差，研究员不切对话。

| 模块 | 调度模式 | 子代理角色 | 提示词模板 |
|---|---|---|---|
| 04 证据采集 | ✅ **并行多子代理** | 事实核查员（每子判断 1 个） | `subagents/fact-checker-prompt.md` |
| 05 反方审稿 | ✅ **单子代理** | 反方审稿员 | `subagents/reviewer-prompt.md` |
| 01 / 07 | ❌ 不用（需对话 / 需完整上下文） | —— | —— |
| 02 / 03 / 06 | （未来扩展） | —— | —— |

**怎么派、调用规约、兜底、硬配额、本地豁免** → 读 `references/subagent_dispatch.md`（派子代理前必读）。
**非 Claude Code 平台的工具名映射** → 读 `references/platform_adaptation.md`。

## 模块停止协议（最易违反 · 适用模块 01–06）

分阶段模式下每模块以硬停结束：①输出阶段产出 → ②输出"待研究员逐条确认的判断点"（对应模块"AI 不替你做的"每条）→ ③停下等回应。各模块末尾的"硬停"块是权威全文。

- **反惯性**：研究员简短确认（"好""继续""OK""下一步""嗯""go"）**不构成**跳过授权。简短/含糊回复 → 重述未确认项，要求逐条回应。
- **部分确认**：只回应部分判断点 → 对未覆盖项继续追问，不默认其余已通过。
- **唯一例外**：用户明确"先给我完整草稿"/"一次性走完"/时间极紧 → 六步一次走完，假定项标"假定 X · 待研究员审核"。
- 模块 07 是最终交付，其内部中间确认由研究员自主，不受本协议约束。

## 本地资料处理（铁律）

```
LOCAL FIRST-HAND BEFORE WEB SEARCH
本地一手 > 联网一手 > 联网二手 > AI 既有知识
```

本地资料没消化完之前，不启动联网搜索。任何本地资料引用为证据必须标**识别等级**（完整识别 / 部分识别 / 仅文字识别 / 摘要识别 / 未识别）——**仅"完整识别"可进证据矩阵正文**，其余进待复核。登记时点、5 档定义、工具链调用规范全文 → `references/local_materials_protocol.md`。

## 交付包结构（铁律）

```
NO DELIVERY WITHOUT VERIFICATION CHECKLIST
```

模块 07 成稿 = 单一报告 + 多附件，分三层（对外 / 对内 / 归档）。**必须配套生成"待复核清单"**——汇总模块 04/05/06 所有需人工核对位置（识别等级非完整 / 边界待确认 / 单一信源 / 必改风险 / ▢ 未填）。无待复核清单不算完整交付。全文 → `modules/07_report_assembly.md` "交付包结构" 小节。

## 工作纪律

- 每加载一个模块，把该模块"AI 不替你做的"显式展示给研究员——这些是判断关口
- **模块 04 必须遵循两份协议**：`evidence_sourcing_protocol.md`（联网）+ `local_materials_protocol.md`（本地），均为唯一权威。采集顺序：消化本地 → 边界自检 → 联网补缺 → 填 12 字段。违反协议的证据行无效
- 任何用到证据处，"能支撑什么 / 不能支撑什么"必须并列写
- 每条关键假设、薄弱证据、未验证来源都**显式标注**，不要打磨掉
- 反方审稿先批评，不润色（除非用户要）
- 建议除非证据 + 决策语境足够，否则标"框架性候选 · 待研究员审核"
- 优先"正向、有边界"的论点，避免结论强度超出证据等级
- 最终报告用成熟体例（`report_style_guide.md`），不把"问题定义/证据矩阵/反方审稿/建议分层"作为报告章节标题暴露

## 输出文件夹约定

用户需要文件时，分阶段产出放在同一课题文件夹：

```text
<课题名>/
01_问题定义.md  02_判断框架.md  03_假设清单.md  04_证据矩阵.xlsx
05_反方审稿.md  06_分层建议.md  07_成熟报告.md
```

assets 模板当起点，不从零重写其结构。

## 维护

仓库结构 / 脱敏 / 引用完整性自检 → 运行 `scripts/health_check.py`（详见 `scripts/README.md`）。

## 常见错误

- 把任务做成叙述性文献综述，而不是给判断
- 一次性加载所有模块和参考资料，浪费上下文
- 让 AI 编造当下事实而不做信源核查
- 跳过证伪条件，导致证据搜索变成自我确认
- 证据只够"观察/研究"层却写成"行动"建议
- 把 AI 摘要当一手证据；关键数据必须回原文核对
- 把六步法过程笔记当最终报告交付，而不是跑报告成稿
