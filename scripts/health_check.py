#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill health check —— 把反复踩过的坑固化成自动检查。

检查项：
  1. frontmatter name 是小写 kebab-case
  2. 仓库内部引用的文件真实存在（防悬空引用）
  3. 方法论文件无"本单位假设"泄漏（去本单位化纪律 · 排除 references/cases/）
  4. 无 PII 泄漏：作者行含中文真名 / 私人邮箱 / 本机路径 / 访问令牌
  5. README 含版本字符串（软检查）

设计原则：脚本只编码"规则"，不写入任何具体 PII（用正则模式检测，
不硬编码人名/邮箱）——否则脱敏脚本自己又成了泄漏源。

用法：
  python scripts/health_check.py                 # 默认检查脚本所在 skill
  python scripts/health_check.py --skill-dir X   # 指定 skill 目录
退出码：有 ✗（硬失败）→ 1，否则 0。
"""
import argparse
import re
import sys
from pathlib import Path

# Windows 控制台默认 GBK，强制 UTF-8 输出，避免中文/符号编码错误
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# 纯 ASCII 状态标记（不用 ✓✗ 与 ANSI 颜色，保证 Windows / cmd / git-bash 全兼容）
BOLD = RED = GREEN = YEL = RST = ""
OK = "[OK]"; FAIL = "[FAIL]"; WARN = "[WARN]"

# 本单位假设词表（方法论文件里不该出现；案例文件豁免）
ORG_TERMS = ["集团", "经研院", "央企", "党组", "均衡增长", "农村能源",
             "新型电力系统", "我司", "主业映射", "主业判断"]
# 仓库内部引用前缀（这些路径必须真实存在）
REF_DIRS = ("modules", "references", "subagents", "assets", "scripts", "agents")
TEXT_EXT = (".md", ".yaml", ".yml")
SKIP_DIRS = (".git",)


def iter_text_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT \
           and not any(part in SKIP_DIRS for part in p.parts):
            yield p


def check_frontmatter_name(root: Path, fails: list, warns: list):
    skill = root / "SKILL.md"
    if not skill.exists():
        fails.append("SKILL.md 不存在")
        return
    text = skill.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    if not m:
        fails.append("SKILL.md frontmatter 缺 name 字段")
        return
    name = m.group(1).strip()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        fails.append(f"frontmatter name 非小写 kebab-case：'{name}'")
    else:
        print(f"  {OK} frontmatter name = '{name}'")


def check_dangling_refs(root: Path, fails: list, warns: list):
    pat = re.compile(r"(?:" + "|".join(REF_DIRS) + r")/[\w./\-]+\.\w+")
    missing = {}
    for f in iter_text_files(root):
        for line_no, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for ref in pat.findall(line):
                ref_clean = ref.rstrip(").,;:")
                if not (root / ref_clean).exists():
                    missing.setdefault(ref_clean, []).append(f"{f.relative_to(root)}:{line_no}")
    if missing:
        for ref, locs in sorted(missing.items()):
            fails.append(f"悬空引用 '{ref}'  ← {locs[0]}" + (f" 等 {len(locs)} 处" if len(locs) > 1 else ""))
    else:
        print(f"  {OK} 仓库内部引用全部命中（无悬空引用）")


def check_org_leak(root: Path, fails: list, warns: list):
    hits = []
    for f in iter_text_files(root):
        # 只查模型当作研究指令加载的方法论内容；元文档（README/scripts）与案例豁免：
        # 案例是实战样例本该具体；README 变更日志 / scripts 文档会合法提及这些词
        if "cases" in f.parts or "scripts" in f.parts or f.name == "README.md":
            continue
        for line_no, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for term in ORG_TERMS:
                if term in line:
                    hits.append(f"{f.relative_to(root)}:{line_no}  含 '{term}'")
    if hits:
        for h in hits[:20]:
            fails.append(f"本单位假设泄漏：{h}")
        if len(hits) > 20:
            fails.append(f"……另有 {len(hits) - 20} 处")
    else:
        print(f"  {OK} 方法论文件无本单位假设泄漏")


def check_pii(root: Path, fails: list, warns: list):
    cjk = re.compile(r"[一-鿿]")
    email = re.compile(r"[\w.+\-]+@(?:gmail|163|qq|outlook|hotmail|foxmail|126|sina)\.com", re.I)
    local_path = re.compile(r"[A-Za-z]:[\\/]Users[\\/]|/Users/|[A-Za-z]:[\\/]工作")
    token = re.compile(r"\bghp_[A-Za-z0-9]{10,}")
    author = re.compile(r"作者[:：]\s*(.+)")
    found = []
    for f in iter_text_files(root):
        for line_no, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            am = author.search(line)
            if am and cjk.search(am.group(1)):
                found.append(f"{f.relative_to(root)}:{line_no}  作者行含中文真名")
            if email.search(line):
                found.append(f"{f.relative_to(root)}:{line_no}  私人邮箱")
            if local_path.search(line):
                found.append(f"{f.relative_to(root)}:{line_no}  本机路径")
            if token.search(line):
                found.append(f"{f.relative_to(root)}:{line_no}  访问令牌")
    if found:
        for h in found:
            fails.append(f"PII 泄漏：{h}")
    else:
        print(f"  {OK} 无 PII 泄漏（真名/私邮/本机路径/令牌）")


def check_hardstop(root: Path, fails: list, warns: list):
    # 六步法不变量：模块 01-06 必含 <硬停> 块，模块 07（最终交付）必不含。
    # 无 modules/ 结构的 skill（如 quick-research，设计上全程无硬停）自动跳过。
    mods_dir = root / "modules"
    mods = sorted(mods_dir.glob("0*.md")) if mods_dir.is_dir() else []
    if not mods:
        return
    bad = []
    for m in mods:
        mt = re.match(r"(\d+)", m.name)
        if not mt:
            continue
        num = int(mt.group(1))
        has = "<硬停>" in m.read_text(encoding="utf-8", errors="replace")
        if 1 <= num <= 6 and not has:
            bad.append(f"模块 {num:02d} 缺 <硬停> 块（停止协议适用模块）")
        if num == 7 and has:
            bad.append("模块 07 不应有 <硬停> 块（最终交付不受停止协议约束）")
    if bad:
        fails.extend(bad)
    else:
        print(f"  {OK} 硬停不变量正确（01-06 有、07 无）")


def check_version(root: Path, fails: list, warns: list):
    readme = root / "README.md"
    if readme.exists() and re.search(r"v\d+(\.\d+)*|版本", readme.read_text(encoding="utf-8", errors="replace")):
        print(f"  {OK} README 含版本字符串")
    else:
        warns.append("README 未发现版本字符串")


def main():
    ap = argparse.ArgumentParser(description="Skill health check")
    ap.add_argument("--skill-dir", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.skill_dir).resolve()

    print(f"\n{BOLD}Skill health check{RST}  ->  {root}\n")
    fails, warns = [], []
    for fn in (check_frontmatter_name, check_dangling_refs, check_org_leak, check_pii, check_hardstop, check_version):
        fn(root, fails, warns)

    print()
    for w in warns:
        print(f"  {WARN} {w}")
    for x in fails:
        print(f"  {FAIL} {x}")

    print()
    if fails:
        print(f"{RED}{BOLD}FAIL{RST} —— {len(fails)} 项硬失败，{len(warns)} 项警告\n")
        sys.exit(1)
    print(f"{GREEN}{BOLD}PASS{RST} —— 全部通过" + (f"，{len(warns)} 项警告" if warns else "") + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
