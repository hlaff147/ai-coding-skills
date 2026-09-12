#!/usr/bin/env python3
"""
scripts/audit_skills.py
Framework automatizado de auditoria de conformidade e custo de tokens para AI Coding Skills.
"""

import os
import re
import sys

REQUIRED_FILES = [
    "SKILL.md",
    ".cursorrules",
    "copilot-instructions.md",
    "README.md",
]

LINE_THRESHOLD_WARN = 120
DESC_WORD_THRESHOLD_WARN = 50


def audit_skill(skill_dir_path):
    skill_name = os.path.basename(skill_dir_path)
    report = {
        "name": skill_name,
        "files_present": [],
        "files_missing": [],
        "skill_md_lines": 0,
        "desc_words": 0,
        "body_tokens_est": 0,
        "warnings": [],
    }

    # Check files
    for req_file in REQUIRED_FILES:
        target_path = os.path.join(skill_dir_path, req_file)
        if os.path.exists(target_path):
            report["files_present"].append(req_file)
        else:
            report["files_missing"].append(req_file)

    # Analyze SKILL.md
    skill_md = os.path.join(skill_dir_path, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()
        report["skill_md_lines"] = len(lines)
        words = len(content.split())
        report["body_tokens_est"] = int(words * 1.3)

        # Extract description
        m = re.search(
            r"^description:\s*(?:>-\s*|\"|\|)?(.*?)(?=\n[a-z_]+:|\n---)",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if m:
            desc_clean = m.group(1).strip("\"'\n ")
            report["desc_words"] = len(desc_clean.split())

        # Warnings
        if report["desc_words"] > DESC_WORD_THRESHOLD_WARN:
            report["warnings"].append(
                f"Description longa ({report['desc_words']} palavras > {DESC_WORD_THRESHOLD_WARN})"
            )
        if report["skill_md_lines"] > LINE_THRESHOLD_WARN:
            report["warnings"].append(
                f"SKILL.md extenso ({report['skill_md_lines']} linhas > {LINE_THRESHOLD_WARN})"
            )

    if report["files_missing"]:
        report["warnings"].append(
            f"Faltam formatos: {', '.join(report['files_missing'])}"
        )

    return report


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    # Find skill directories
    skill_dirs = sorted(
        [
            os.path.join(repo_root, d)
            for d in os.listdir(repo_root)
            if os.path.isdir(os.path.join(repo_root, d))
            and len(d) > 2
            and d[:2].isdigit()
        ]
    )

    print("\n📊 RELATÓRIO DE AUDITORIA DE SKILLS (Conformidade & Custo)\n")
    print(
        f"| # | Skill | Formatos | Linhas SKILL.md | Palavras Desc | Tokens Est. | Status |"
    )
    print(
        f"|---|-------|:--------:|:---------------:|:-------------:|:-----------:|:------:|"
    )

    total_tokens = 0
    total_desc_words = 0
    total_warnings = 0

    for s_path in skill_dirs:
        data = audit_skill(s_path)
        num = data["name"][:2]
        slug = data["name"][3:]
        formats = f"{len(data['files_present'])}/4"

        status_badge = "✅ OK"
        if data["warnings"]:
            status_badge = "⚠️ " + "; ".join(data["warnings"])
            total_warnings += len(data["warnings"])

        total_tokens += data["body_tokens_est"]
        total_desc_words += data["desc_words"]

        print(
            f"| {num} | {slug} | {formats} | {data['skill_md_lines']} | {data['desc_words']} | ~{data['body_tokens_est']} | {status_badge} |"
        )

    print(
        f"\n📈 **Métricas Globais:** Total Skills: {len(skill_dirs)} | Total Tokens Est.: ~{total_tokens} | Média Palavras Desc: {total_desc_words // len(skill_dirs)} | Alertas: {total_warnings}\n"
    )


if __name__ == "__main__":
    main()
