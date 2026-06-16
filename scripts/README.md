# scripts

本目录放 full-research 的维护脚本。纯 Python，能在 Windows / macOS / Linux 上跑。

## health_check.py

仓库结构与脱敏自检——把反复踩过的坑固化成自动检查，每次改完跑一遍。

```bash
python scripts/health_check.py
```

检查项：

1. **frontmatter name** 是小写 kebab-case
2. **悬空引用**：仓库内部引用（`modules/` `references/` `subagents/` `assets/` `scripts/` `agents/` 开头的路径）真实存在
3. **本单位假设泄漏**：方法论文件无 集团/经研院/央企/主业映射 等写死称谓（`references/cases/` 案例文件豁免）
4. **PII 泄漏**：作者行无中文真名、无私人邮箱、无本机路径、无访问令牌
5. **硬停不变量**：模块 01–06 必含 `<硬停>` 块、模块 07 必不含（无 `modules/` 的 skill 自动跳过）
6. **版本字符串**：README 含 version（软检查）

有硬失败退出码 1，否则 0。

设计原则：脚本只编码"规则"，不写入任何具体 PII（用正则模式检测，不硬编码人名/邮箱）——否则脱敏脚本自己又成了泄漏源。
