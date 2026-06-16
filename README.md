# full-research

> AI 辅助综合研究方法论 · Claude Code 技能 · 六步法 + 工程化协议

把宽泛研究题目收敛为有判断、有证据、有边界的研究产出。设计原则：**AI 参与每一步，研究员承担最终判断**。

## 是什么

这是一个 [Claude Code 技能](https://docs.claude.com/en/docs/claude-code/skills)，把综合研究的工作流封装成可复用的协议体系。包含：

- **六步法工作流**：问题定义 → 框架收敛 → 假设生成 → 证据矩阵 → 反方审稿 → 建议分层
- **第七步报告组装**：把研究过程产出转成成熟报告 + 完整交付包
- **多轮停止协议**：每模块结束硬停下，等研究员逐条确认
- **子代理隔离机制**：事实核查员 / 审稿员派出独立子代理，消除确认偏差
- **证据采集协议**：12 字段强制信源溯源 + 识别等级标注
- **本地资料处理协议**：PDF / Word / Excel / 图片的 anthropic-skills 工具链调用规范
- **研究主体声明**：4 字段开放式，让研究员自己定义输出范围与禁区

## 安装

### 单设备首次安装

```bash
cd ~/.claude/skills
git clone https://github.com/ymb023/full-research-public.git
```

或直接 clone 到 skills 目录：

```bash
git clone https://github.com/ymb023/full-research-public.git ~/.claude/skills/full-research
```

### 多设备同步

每台设备首次：`git clone` 到 `~/.claude/skills/full-research/`

后续更新：

```bash
cd ~/.claude/skills/full-research
git pull
```

## 使用

新开 Claude Code 会话，输入：

```
/full-research
```

或直接说"做个综合研究 / 研究 X / 出研究报告 / 做证据矩阵 / 做反方审稿"等触发词，Claude 会自动调用本技能。

## 目录结构

```
full-research/
├── SKILL.md                              # 技能入口 + 路由 + 工作纪律
├── modules/                              # 六步法 + 报告成稿（7 个模块）
│   ├── 01_problem_definition.md
│   ├── 02_framework_convergence.md
│   ├── 03_hypothesis_generation.md
│   ├── 04_evidence_matrix.md
│   ├── 05_red_team_review.md
│   ├── 06_recommendation_layering.md
│   └── 07_report_assembly.md
├── references/                           # 协议与参考资料
│   ├── evidence_sourcing_protocol.md     # 联网证据采集协议
│   ├── local_materials_protocol.md       # 本地资料处理协议
│   ├── subagent_dispatch.md              # 子代理调度详情（派子代理前必读）
│   ├── platform_adaptation.md            # 非 Claude Code 平台的工具映射
│   ├── consulting_frameworks_cheatsheet.md
│   ├── judgment_framework_patterns.md
│   ├── report_style_guide.md
│   └── cases/case_token_outbound.md      # 经典案例
├── subagents/                            # 隔离上下文的子代理提示词
│   ├── fact-checker-prompt.md            # 模块 04 默认推荐
│   └── reviewer-prompt.md                # 模块 05 强烈推荐
├── assets/                               # 模板
│   └── mature_report_template.md
├── scripts/                              # 维护脚本
│   ├── health_check.py                   # 结构 / 脱敏 / 引用完整性自检
│   └── README.md
└── agents/                               # 多平台适配
    └── openai.yaml                       # Codex / Cowork
```

## 设计哲学

- **判断导向，不是综述导向**：研究最终要回答有边界的判断，不做"是什么 + 现状 + 趋势"的发散综述
- **证据可追溯**：每条事实必须有信源机构 + 发布日期 + URL + 访问日期 + 原文摘录 + 识别等级
- **隔离消除偏见**：核心审视动作（事实核查、反方审稿）派子代理在无主会话历史的环境执行
- **研究员主权**：AI 做不了的事（最终判断、政治分寸、组织数据、领域常识）显式归还研究员

## 版本

当前 v7.4（2026-06）

历史版本要点：
- v7：模块 04 默认改为并行多子代理调度
- v7.1：事实核查员加 6 项硬配额（解决"一两轮就放弃"）
- v7.2：删悬空引用 + 加平台适配小节 + 审稿员 9 维统一 + 本地资料豁免规则
- v7.3：去本单位化——主业映射链泛化为落地映射链（目标取自研究主体声明、可跳过），清除集团/央企/经研院等写死假设，报告体例降为可替换示例
- v7.4：SKILL.md 瘦回导航页（细节移入 references）+ 加 `scripts/health_check.py` 自检脚本 + 配额数字归一权威 + 加 LICENSE

## License

本作品采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hans)（署名-非商业性使用）许可。详见 [LICENSE](LICENSE)。

---

作者：ymb023
