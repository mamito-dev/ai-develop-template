#!/usr/bin/env python3
"""
AI Documentation Validator
AI向けDocumentationの整合性を自動検証するツール

Usage:
    python scripts/ai-docs/validate.py
    python scripts/ai-docs/validate.py --json

Exit Codes:
    0 = PASS (ERROR なし。WARNING のみの場合も 0)
    1 = ERROR (1件以上の ERROR が検出された)
    2 = INVALID_CONFIGURATION (設定ファイルに問題がある)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# rules.py は同一ディレクトリに配置される
sys.path.insert(0, str(Path(__file__).parent))
import rules as R  # noqa: E402


# ──────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────

@dataclass
class Finding:
    level: str          # ERROR / WARNING / INFO
    rule: str           # AI001 ..
    file: str
    message: str
    detail: str = ""


@dataclass
class ValidationContext:
    repo_root: Path
    manifest: dict[str, Any] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    skill_dirs: list[Path] = field(default_factory=list)
    prompt_files: list[Path] = field(default_factory=list)
    instruction_files: list[Path] = field(default_factory=list)

    def add(self, level: str, rule: str, file: str, message: str, detail: str = "") -> None:
        self.findings.append(Finding(level, rule, file, message, detail))

    def error(self, rule: str, file: str, message: str, detail: str = "") -> None:
        self.add(R.LEVEL_ERROR, rule, file, message, detail)

    def warning(self, rule: str, file: str, message: str, detail: str = "") -> None:
        self.add(R.LEVEL_WARNING, rule, file, message, detail)

    def info(self, rule: str, file: str, message: str, detail: str = "") -> None:
        self.add(R.LEVEL_INFO, rule, file, message, detail)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == R.LEVEL_ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == R.LEVEL_WARNING]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.level == R.LEVEL_INFO]


# ──────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────

def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def parse_front_matter(content: str) -> tuple[dict[str, Any], str]:
    """YAML Front Matter をパースして (metadata, body) を返す。"""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    if not HAS_YAML:
        return {}, body
    try:
        meta = yaml.safe_load(fm_text) or {}
        return meta, body
    except yaml.YAMLError:
        return {}, body


def extract_headings(content: str) -> list[tuple[int, str]]:
    """Markdown の見出しを (level, text) のリストで返す。"""
    headings = []
    in_code_fence = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_fence = not in_code_fence
        if in_code_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
    return headings


def heading_to_anchor(text: str) -> str:
    """GitHub Markdown のアンカー生成規則に従う。"""
    anchor = text.lower()
    anchor = re.sub(r"[^\w\s\-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor.strip())
    return anchor


def is_placeholder_path(p: str) -> bool:
    for pattern in R.PATH_PLACEHOLDER_PATTERNS:
        if re.search(pattern, p):
            return True
    return False


def extract_markdown_links(content: str) -> list[tuple[str, str]]:
    """Markdown のリンク [(text, href)] を抽出する。外部URLは除外。"""
    in_code_fence = False
    links = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_fence = not in_code_fence
        if in_code_fence:
            continue
        for text, href in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", line):
            # 外部URL は対象外
            if href.startswith("http://") or href.startswith("https://"):
                continue
            # mailto も対象外
            if href.startswith("mailto:"):
                continue
            links.append((text, href))
    return links


def resolve_link(href: str, source_file: Path, repo_root: Path) -> tuple[Optional[Path], Optional[str]]:
    """リンクのパスとアンカーを解決する。存在する場合は (path, anchor)、なければ None 系。"""
    anchor = None
    if "#" in href:
        parts = href.split("#", 1)
        href = parts[0]
        anchor = parts[1]
    if not href:
        return source_file, anchor
    if href.startswith("/"):
        resolved = repo_root / href.lstrip("/")
    else:
        resolved = (source_file.parent / href).resolve()
    return resolved, anchor


# ──────────────────────────────────────────────────────────────
# Rule implementations
# ──────────────────────────────────────────────────────────────

def validate_manifest(ctx: ValidationContext) -> None:
    """AI013: ai-docs.yml の検証"""
    manifest_path = ctx.repo_root / ".github" / "ai-docs.yml"
    rel = relative(manifest_path, ctx.repo_root)

    if not manifest_path.exists():
        ctx.error(R.RULE_INVALID_MANIFEST, rel, "ai-docs.yml が存在しません")
        return

    if not HAS_YAML:
        ctx.warning(R.RULE_INVALID_MANIFEST, rel, "PyYAML が未インストールのため YAML 検証をスキップします")
        return

    content = read_text(manifest_path)
    if content is None:
        ctx.error(R.RULE_INVALID_MANIFEST, rel, "ai-docs.yml を読み込めません")
        return

    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        ctx.error(R.RULE_INVALID_MANIFEST, rel, f"YAML 構文エラー: {e}")
        return

    if "version" not in data:
        ctx.error(R.RULE_INVALID_MANIFEST, rel, "version フィールドが存在しません")

    ctx.manifest = data

    # required paths の存在確認
    for req_path in data.get("required", []):
        p = ctx.repo_root / req_path
        if not p.exists():
            ctx.error(R.RULE_REQUIRED_FILE_MISSING, req_path,
                      f"必須ファイルが存在しません: {req_path}")

    # source_of_truth paths の存在確認
    sot = data.get("source_of_truth", {})
    for domain, sot_path in sot.items():
        p = ctx.repo_root / sot_path
        if not p.exists():
            ctx.warning(R.RULE_INVALID_MANIFEST, sot_path,
                        f"source_of_truth のパスが存在しません: {sot_path} (domain: {domain})")


def validate_required_files(ctx: ValidationContext) -> None:
    """AI001: 必須ファイルの存在確認"""
    # Manifest で定義されていない場合でも最低限チェック
    hardcoded = [
        ".github/copilot-instructions.md",
        "AGENTS.md",
    ]
    already_checked = set(ctx.manifest.get("required", []))
    for req in hardcoded:
        if req not in already_checked:
            p = ctx.repo_root / req
            if not p.exists():
                ctx.error(R.RULE_REQUIRED_FILE_MISSING, req,
                          f"必須ファイルが存在しません: {req}")


def validate_change_safety_policy(ctx: ValidationContext) -> None:
    """AI015: .github/change-safety.yml の構造検証"""
    policy_path = ctx.repo_root / ".github" / "change-safety.yml"
    rel = relative(policy_path, ctx.repo_root)

    if not policy_path.exists():
        # 必須ファイル扱いは AI001 / Manifest 側で検証
        return

    if not HAS_YAML:
        ctx.warning(
            R.RULE_INVALID_CHANGE_SAFETY_POLICY,
            rel,
            "PyYAML が未インストールのため change-safety.yml 検証をスキップします",
        )
        return

    content = read_text(policy_path)
    if content is None:
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, "change-safety.yml を読み込めません")
        return

    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, f"YAML 構文エラー: {e}")
        return

    if not isinstance(data, dict):
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, "トップレベルは mapping である必要があります")
        return

    if "version" not in data:
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, "version フィールドが存在しません")

    changes = data.get("changes")
    if not isinstance(changes, dict):
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, "changes フィールドは mapping である必要があります")
        return

    supported_categories = {
        "code",
        "tests",
        "documentation",
        "dependency",
        "api",
        "database",
        "architecture",
        "configuration",
        "security",
        "ci_cd",
        "infrastructure",
        "generated",
        "git",
        "destructive",
        "history_rewrite",
        "secret_access",
        "unknown",
    }
    valid_values = {"allowed", "restricted", "forbidden"}

    categories = list(changes.keys())
    if len(categories) != len(set(categories)):
        ctx.error(R.RULE_INVALID_CHANGE_SAFETY_POLICY, rel, "changes に重複カテゴリがあります")

    unknown_categories = sorted(set(categories) - supported_categories)
    if unknown_categories:
        ctx.error(
            R.RULE_INVALID_CHANGE_SAFETY_POLICY,
            rel,
            f"未対応カテゴリが含まれています: {', '.join(unknown_categories)}",
        )

    missing_categories = sorted(supported_categories - set(categories))
    if missing_categories:
        ctx.error(
            R.RULE_INVALID_CHANGE_SAFETY_POLICY,
            rel,
            f"必須カテゴリが不足しています: {', '.join(missing_categories)}",
        )

    for category, value in changes.items():
        if value not in valid_values:
            ctx.error(
                R.RULE_INVALID_CHANGE_SAFETY_POLICY,
                rel,
                f"不正な Policy Value: {category}={value} "
                f"(許可値: {', '.join(sorted(valid_values))})",
            )


def validate_directory_structure(ctx: ValidationContext) -> None:
    """Directory Structure と Naming Convention の検証"""
    github_dir = ctx.repo_root / ".github"

    # Instructions
    instructions_dir = github_dir / "instructions"
    ctx.instruction_files = []
    if instructions_dir.exists():
        for f in instructions_dir.iterdir():
            if f.name == ".gitkeep":
                continue
            if f.is_file():
                if not re.match(R.INSTRUCTION_FILENAME_PATTERN, f.name):
                    ctx.warning(
                        R.RULE_INVALID_NAMING_CONVENTION,
                        relative(f, ctx.repo_root),
                        f"命名規則違反 (期待: *.instructions.md): {f.name}",
                    )
                else:
                    ctx.instruction_files.append(f)

    # Prompts
    prompts_dir = github_dir / "prompts"
    ctx.prompt_files = []
    if prompts_dir.exists():
        for f in prompts_dir.iterdir():
            if f.name == ".gitkeep":
                continue
            if f.is_file():
                if not re.match(R.PROMPT_FILENAME_PATTERN, f.name):
                    ctx.warning(
                        R.RULE_INVALID_NAMING_CONVENTION,
                        relative(f, ctx.repo_root),
                        f"命名規則違反 (期待: *.prompt.md): {f.name}",
                    )
                else:
                    ctx.prompt_files.append(f)

    # Skills
    skills_dir = github_dir / "skills"
    ctx.skill_dirs = []
    if skills_dir.exists():
        for entry in skills_dir.iterdir():
            if entry.name == ".gitkeep":
                continue
            if entry.is_dir():
                skill_md = entry / "SKILL.md"
                if not skill_md.exists():
                    ctx.warning(
                        R.RULE_INVALID_SKILL_STRUCTURE,
                        relative(entry, ctx.repo_root),
                        f"Skill ディレクトリに SKILL.md が存在しません: {entry.name}",
                    )
                else:
                    ctx.skill_dirs.append(entry)
            elif entry.is_file():
                ctx.warning(
                    R.RULE_INVALID_NAMING_CONVENTION,
                    relative(entry, ctx.repo_root),
                    f"skills/ 直下のファイルは許可されていません: {entry.name}",
                )

    ctx.info(
        R.RULE_INFO,
        ".github/",
        f"Instructions: {len(ctx.instruction_files)} 件, "
        f"Prompts: {len(ctx.prompt_files)} 件, "
        f"Skills: {len(ctx.skill_dirs)} 件",
    )


def _check_sections(content: str, required: list[Any], file_rel: str,
                    ctx: ValidationContext, rule: str) -> None:
    """
    必須セクションを確認する。
    required の各要素は str または (canonical, [aliases]) のタプル。
    """
    headings_text = [h for _, h in extract_headings(content)]

    for req in required:
        if isinstance(req, str):
            canonical = req
            aliases = [req]
        else:
            canonical, aliases = req

        found = any(h in aliases for h in headings_text)
        if not found:
            ctx.error(
                R.RULE_MISSING_REQUIRED_SECTION,
                file_rel,
                f"必須セクションがありません: {canonical}",
                detail=f"期待: ## {canonical}",
            )


def validate_skills(ctx: ValidationContext) -> None:
    """AI004 / AI007: Skill 構造と必須セクションの検証"""
    for skill_dir in ctx.skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        rel = relative(skill_md, ctx.repo_root)
        content = read_text(skill_md)
        if content is None:
            ctx.error(R.RULE_INVALID_SKILL_STRUCTURE, rel, "SKILL.md を読み込めません")
            continue

        meta, body = parse_front_matter(content)

        # 必須セクション確認
        _check_sections(body, R.SKILL_REQUIRED_SECTIONS, rel, ctx, R.RULE_MISSING_REQUIRED_SECTION)

        # メタデータ検証
        if meta:
            _validate_metadata(meta, rel, ctx)
            # AI009: Prompt 参照検証
            if "prompts" in meta:
                _validate_prompt_references(meta["prompts"], rel, ctx)


def validate_prompts(ctx: ValidationContext) -> None:
    """AI005 / AI007: Prompt 構造と必須セクションの検証"""
    for prompt_file in ctx.prompt_files:
        rel = relative(prompt_file, ctx.repo_root)
        content = read_text(prompt_file)
        if content is None:
            ctx.error(R.RULE_INVALID_PROMPT_STRUCTURE, rel, "Prompt ファイルを読み込めません")
            continue

        meta, body = parse_front_matter(content)

        _check_sections(body, R.PROMPT_REQUIRED_SECTIONS, rel, ctx, R.RULE_MISSING_REQUIRED_SECTION)

        # メタデータ検証
        if meta:
            _validate_metadata(meta, rel, ctx)

        # Skill 参照検証
        if meta and "skills" in meta:
            _validate_skill_references(meta["skills"], rel, ctx)


def validate_instructions(ctx: ValidationContext) -> None:
    """AI006 / AI007: Instruction 構造の検証"""
    for inst_file in ctx.instruction_files:
        rel = relative(inst_file, ctx.repo_root)
        content = read_text(inst_file)
        if content is None:
            ctx.error(R.RULE_INVALID_INSTRUCTION_STRUCTURE, rel, "Instruction ファイルを読み込めません")
            continue

        meta, body = parse_front_matter(content)
        _check_sections(body, R.INSTRUCTION_REQUIRED_SECTIONS, rel, ctx,
                        R.RULE_MISSING_REQUIRED_SECTION)


def _validate_skill_references(skill_list: list[str], prompt_rel: str,
                                ctx: ValidationContext) -> None:
    """AI008: Prompt から参照された Skill の存在確認"""
    existing_skills = {d.name for d in ctx.skill_dirs}

    for skill_name in skill_list:
        if skill_name not in existing_skills:
            ctx.error(
                R.RULE_MISSING_REFERENCED_SKILL,
                prompt_rel,
                f"参照された Skill が存在しません: {skill_name}",
                detail=f"期待: .github/skills/{skill_name}/SKILL.md",
            )


def _validate_prompt_references(prompt_list: list[str], skill_rel: str,
                                 ctx: ValidationContext) -> None:
    """AI009: Skill から参照された Prompt の存在確認"""
    existing_prompts = {f.stem.replace(".prompt", "") for f in ctx.prompt_files}
    # prompt ファイル名から拡張子を除いた名前のセット（例: implement-issue）
    existing_prompt_names = {
        re.sub(r"\.prompt$", "", f.stem) for f in ctx.prompt_files
    }

    for prompt_name in prompt_list:
        if prompt_name not in existing_prompt_names:
            ctx.error(
                R.RULE_MISSING_REFERENCED_PROMPT,
                skill_rel,
                f"参照された Prompt が存在しません: {prompt_name}",
                detail=f"期待: .github/prompts/{prompt_name}.prompt.md",
            )


def _validate_metadata(meta: dict, file_rel: str, ctx: ValidationContext) -> None:
    """AI012: メタデータの基本検証"""
    # type フィールドの値確認
    if "type" in meta:
        valid_types = {"prompt", "skill", "instruction", "documentation"}
        if meta["type"] not in valid_types:
            ctx.warning(
                R.RULE_INVALID_METADATA,
                file_rel,
                f"不正な type 値: {meta['type']} (期待: {', '.join(sorted(valid_types))})",
            )

    # status フィールドの値確認
    if "status" in meta:
        valid_statuses = {"active", "draft", "deprecated", "archived"}
        if meta["status"] not in valid_statuses:
            ctx.warning(
                R.RULE_INVALID_METADATA,
                file_rel,
                f"不正な status 値: {meta['status']} "
                f"(期待: {', '.join(sorted(valid_statuses))})",
            )

    # deprecated の場合 replacement を確認
    if meta.get("status") == "deprecated":
        if "replacement" not in meta:
            ctx.warning(
                R.RULE_DEPRECATED_DOC_REFERENCE,
                file_rel,
                "status: deprecated のファイルに replacement が指定されていません",
            )
        else:
            replacement_path = ctx.repo_root / meta["replacement"]
            if not replacement_path.exists():
                ctx.warning(
                    R.RULE_DEPRECATED_DOC_REFERENCE,
                    file_rel,
                    f"replacement のパスが存在しません: {meta['replacement']}",
                )


def validate_markdown_links(ctx: ValidationContext) -> None:
    """AI002: 内部リンクの検証"""
    # 検証対象ファイル収集
    target_files: list[Path] = []
    patterns = [
        ctx.repo_root / ".github" / "copilot-instructions.md",
        ctx.repo_root / "AGENTS.md",
    ]
    for p in patterns:
        if p.exists():
            target_files.append(p)

    for d in [
        ctx.repo_root / ".github" / "instructions",
        ctx.repo_root / ".github" / "prompts",
    ]:
        if d.exists():
            target_files.extend(f for f in d.glob("*.md") if f.name != ".gitkeep")

    for skill_dir in ctx.skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            target_files.append(skill_md)

    for doc_file in (ctx.repo_root / "docs").rglob("*.md"):
        if doc_file.name != ".gitkeep":
            target_files.append(doc_file)

    for source_file in target_files:
        content = read_text(source_file)
        if content is None:
            continue
        rel = relative(source_file, ctx.repo_root)
        _, body = parse_front_matter(content)
        links = extract_markdown_links(body)

        for text, href in links:
            resolved, anchor = resolve_link(href, source_file, ctx.repo_root)
            if resolved is None:
                continue

            # ファイル存在確認
            if not resolved.exists():
                ctx.error(
                    R.RULE_BROKEN_INTERNAL_LINK,
                    rel,
                    f"存在しないファイルへのリンク: {href}",
                    detail=f"リンクテキスト: [{text}]",
                )
                continue

            # アンカー確認（可能な範囲で）
            if anchor:
                linked_content = read_text(resolved)
                if linked_content is not None:
                    _, linked_body = parse_front_matter(linked_content)
                    headings = extract_headings(linked_body)
                    anchors = {heading_to_anchor(h) for _, h in headings}
                    if anchor not in anchors:
                        ctx.warning(
                            R.RULE_BROKEN_INTERNAL_LINK,
                            rel,
                            f"アンカーが見つかりません: #{anchor} ({href})",
                        )


def validate_referenced_paths(ctx: ValidationContext) -> None:
    """AI003: Markdown 本文中の Path 参照の存在確認"""
    # コードブロック内やリスト内に書かれた相対パスを検出
    # 対象: .github/instructions, .github/prompts, skills, docs 内のファイル
    target_files: list[Path] = []
    for glob_pattern in [
        ".github/instructions/*.instructions.md",
        ".github/prompts/*.prompt.md",
        ".github/policies/*.md",
        ".github/skills/*/SKILL.md",
        "docs/**/*.md",
        ".github/copilot-instructions.md",
        "AGENTS.md",
    ]:
        target_files.extend(ctx.repo_root.glob(glob_pattern))

    # path-like なトークンを検出する正規表現
    # docs/ や .github/ で始まるパスのみを対象とする（誤検知軽減）
    PATH_PATTERN = re.compile(
        r"(?<![`\w/])"
        r"((?:\.github|docs|src|scripts)/[\w/.\-]+\.\w+)"
        r"(?![`\w])"
    )

    for source_file in target_files:
        content = read_text(source_file)
        if content is None:
            continue
        rel = relative(source_file, ctx.repo_root)
        _, body = parse_front_matter(content)

        # コードフェンス内は対象外
        clean_body = re.sub(r"```[\s\S]*?```", "", body)
        clean_body = re.sub(r"~~~[\s\S]*?~~~", "", clean_body)

        for m in PATH_PATTERN.finditer(clean_body):
            candidate = m.group(1)
            if is_placeholder_path(candidate):
                continue
            p = ctx.repo_root / candidate
            if not p.exists():
                ctx.error(
                    R.RULE_INVALID_PATH_REFERENCE,
                    rel,
                    f"参照されたパスが存在しません: {candidate}",
                )


def validate_deprecated_references(ctx: ValidationContext) -> None:
    """AI010: Deprecated Document への参照検出"""
    # 全 Markdown ファイルを1回のパスで収集し、deprecated ファイルと参照元を同時に処理
    all_files: dict[str, tuple[Optional[str], str]] = {}  # rel_path -> (metadata_status, content)
    for md_file in ctx.repo_root.rglob("*.md"):
        content = read_text(md_file)
        if content is None:
            continue
        meta, body = parse_front_matter(content)
        rel = relative(md_file, ctx.repo_root)
        all_files[rel] = (meta.get("status"), body)

    # deprecated なファイルを特定
    deprecated_files: dict[str, str] = {}  # rel_path -> replacement
    for rel, (status, _) in all_files.items():
        if status == "deprecated":
            md_file = ctx.repo_root / rel
            content = read_text(md_file)
            if content:
                meta, _ = parse_front_matter(content)
                deprecated_files[rel] = meta.get("replacement", "")

    if not deprecated_files:
        return

    # 各ファイルのリンクから deprecated を参照しているか確認
    for rel, (_, body) in all_files.items():
        source_file = ctx.repo_root / rel
        links = extract_markdown_links(body)
        for text, href in links:
            resolved, _ = resolve_link(href, source_file, ctx.repo_root)
            if resolved is None:
                continue
            resolved_rel = relative(resolved, ctx.repo_root)
            if resolved_rel in deprecated_files:
                replacement = deprecated_files[resolved_rel]
                ctx.warning(
                    R.RULE_DEPRECATED_DOC_REFERENCE,
                    rel,
                    f"Deprecated なドキュメントへの参照: {resolved_rel}",
                    detail=f"Replacement: {replacement}" if replacement else "",
                )


def validate_source_of_truth(ctx: ValidationContext) -> None:
    """Source of Truth 定義の検証"""
    sot = ctx.manifest.get("source_of_truth", {})
    for domain, sot_path in sot.items():
        p = ctx.repo_root / sot_path
        ctx.info(
            R.RULE_SOURCE_OF_TRUTH_CONFLICT,
            sot_path,
            f"Source of Truth: {domain} → {sot_path} "
            f"({'存在' if p.exists() else '不在'})",
        )


# ──────────────────────────────────────────────────────────────
# Reporting
# ──────────────────────────────────────────────────────────────

def _color(text: str, code: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def print_results(ctx: ValidationContext, json_output: bool = False) -> None:
    if json_output:
        result = {
            "status": "fail" if ctx.errors else "pass",
            "errors": len(ctx.errors),
            "warnings": len(ctx.warnings),
            "results": [
                {
                    "level": f.level,
                    "rule": f.rule,
                    "file": f.file,
                    "message": f.message,
                    **({"detail": f.detail} if f.detail else {}),
                }
                for f in ctx.findings
                if f.level in (R.LEVEL_ERROR, R.LEVEL_WARNING)
            ],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print()
    print("=" * 60)
    print("  AI Documentation Validation")
    print("=" * 60)

    categories = [
        ("Required files",        R.RULE_REQUIRED_FILE_MISSING),
        ("Manifest",              R.RULE_INVALID_MANIFEST),
        ("Change safety policy",  R.RULE_INVALID_CHANGE_SAFETY_POLICY),
        ("Directory structure",   R.RULE_INVALID_NAMING_CONVENTION),
        ("Markdown links",        R.RULE_BROKEN_INTERNAL_LINK),
        ("Referenced paths",      R.RULE_INVALID_PATH_REFERENCE),
        ("Skills",                R.RULE_INVALID_SKILL_STRUCTURE),
        ("Prompts",               R.RULE_INVALID_PROMPT_STRUCTURE),
        ("Instructions",          R.RULE_INVALID_INSTRUCTION_STRUCTURE),
        ("Required sections",     R.RULE_MISSING_REQUIRED_SECTION),
        ("Skill references",      R.RULE_MISSING_REFERENCED_SKILL),
        ("Metadata",              R.RULE_INVALID_METADATA),
        ("Deprecated references", R.RULE_DEPRECATED_DOC_REFERENCE),
    ]

    for label, rule_id in categories:
        related = [f for f in ctx.findings if f.rule == rule_id and f.level == R.LEVEL_ERROR]
        if related:
            print(f"[{_color('FAIL', '31')}] {label}")
        else:
            print(f"[{_color('PASS', '32')}] {label}")

    # Errors
    if ctx.errors:
        print()
        print(_color("Errors:", "31"))
        for f in ctx.errors:
            print()
            print(f"  [{f.rule}] {f.file}")
            print(f"  {f.message}")
            if f.detail:
                print(f"  {f.detail}")

    # Warnings
    if ctx.warnings:
        print()
        print(_color("Warnings:", "33"))
        for f in ctx.warnings:
            print()
            print(f"  [{f.rule}] {f.file}")
            print(f"  {f.message}")
            if f.detail:
                print(f"  {f.detail}")

    # Summary
    print()
    print("-" * 60)
    print(f"  INFO: {len(ctx.infos)} 件")
    print(f"  WARNING: {len(ctx.warnings)} 件")
    print(f"  ERROR: {len(ctx.errors)} 件")
    print("-" * 60)
    print()
    if ctx.errors:
        print(f"Result: {_color('FAIL', '31')}")
    else:
        print(f"Result: {_color('PASS', '32')}")
    print()


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def run(repo_root: Path, json_output: bool = False) -> int:
    ctx = ValidationContext(repo_root=repo_root)

    # 1. Manifest
    validate_manifest(ctx)

    # 2. Required files
    validate_required_files(ctx)

    # 3. Change Safety Policy
    validate_change_safety_policy(ctx)

    # 4. Directory structure & naming
    validate_directory_structure(ctx)

    # 5. Skills
    validate_skills(ctx)

    # 6. Prompts
    validate_prompts(ctx)

    # 7. Instructions
    validate_instructions(ctx)

    # 8. Internal links
    validate_markdown_links(ctx)

    # 9. Referenced paths
    validate_referenced_paths(ctx)

    # 10. Deprecated references
    validate_deprecated_references(ctx)

    # 11. Source of truth (INFO)
    validate_source_of_truth(ctx)

    # Report
    print_results(ctx, json_output=json_output)

    if ctx.errors:
        return R.EXIT_ERROR
    return R.EXIT_PASS


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Documentation Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="リポジトリルートのパス (デフォルト: スクリプトの2階層上)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 形式で出力する",
    )
    args = parser.parse_args()

    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        # scripts/ai-docs/validate.py → scripts/ai-docs → scripts → repo_root
        repo_root = Path(__file__).resolve().parent.parent.parent

    if not repo_root.exists():
        print(f"ERROR: repo_root が存在しません: {repo_root}", file=sys.stderr)
        sys.exit(R.EXIT_INVALID_CONFIGURATION)

    sys.exit(run(repo_root, json_output=args.json))


if __name__ == "__main__":
    main()
