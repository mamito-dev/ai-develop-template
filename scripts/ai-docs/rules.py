"""
AI Documentation Validation Rules
AI向けDocumentationの検証ルール定義
"""

# ──────────────────────────────────────────────────────────────
# Rule IDs
# ──────────────────────────────────────────────────────────────
RULE_REQUIRED_FILE_MISSING      = "AI001"
RULE_BROKEN_INTERNAL_LINK       = "AI002"
RULE_INVALID_PATH_REFERENCE     = "AI003"
RULE_INVALID_SKILL_STRUCTURE    = "AI004"
RULE_INVALID_PROMPT_STRUCTURE   = "AI005"
RULE_INVALID_INSTRUCTION_STRUCTURE = "AI006"
RULE_MISSING_REQUIRED_SECTION   = "AI007"
RULE_MISSING_REFERENCED_SKILL   = "AI008"
RULE_MISSING_REFERENCED_PROMPT  = "AI009"
RULE_DEPRECATED_DOC_REFERENCE   = "AI010"
RULE_SOURCE_OF_TRUTH_CONFLICT   = "AI011"
RULE_INVALID_METADATA           = "AI012"
RULE_INVALID_MANIFEST           = "AI013"
RULE_INVALID_NAMING_CONVENTION  = "AI014"
# 汎用 INFO ルール（統計情報・サマリー出力用）
RULE_INFO                       = "AI000"

# ──────────────────────────────────────────────────────────────
# Severity Levels
# ──────────────────────────────────────────────────────────────
LEVEL_ERROR   = "ERROR"
LEVEL_WARNING = "WARNING"
LEVEL_INFO    = "INFO"

# ──────────────────────────────────────────────────────────────
# Exit Codes
# ──────────────────────────────────────────────────────────────
EXIT_PASS                = 0
EXIT_ERROR               = 1
EXIT_INVALID_CONFIGURATION = 2

# ──────────────────────────────────────────────────────────────
# Skill Required Sections
# Issue Section 13 の定義に基づく
# ──────────────────────────────────────────────────────────────
SKILL_REQUIRED_SECTIONS = [
    "Purpose",
    "When to Use",
    "Workflow",
    "Rules",
    "Validation",
    "Completion Criteria",
    "Output",
]

# ──────────────────────────────────────────────────────────────
# Prompt Required Sections
# 既存Promptが Objective / Completion Report を使用するため、
# それぞれの別名も許容する。
# Issue Section 12 の定義に基づく。
# ──────────────────────────────────────────────────────────────
PROMPT_REQUIRED_SECTIONS = [
    # (canonical_name, [acceptable_aliases])
    ("Objective",          ["Objective", "Purpose"]),
    ("Completion Report",  ["Completion Report", "Output"]),
]

# ──────────────────────────────────────────────────────────────
# Instruction Required Sections
# Issue Section 14: 種類によって構造が異なるため最低限のみ必須。
# 既存 Instructions が日本語セクション名を使用しているため、
# 各種の別名を許容する。
# ──────────────────────────────────────────────────────────────
INSTRUCTION_REQUIRED_SECTIONS = [
    # (canonical_name, [acceptable_aliases])
    (
        "Rules",
        [
            "Rules",
            "基本ルール",
            "ルール",
            # architecture.instructions.md
            "Architectureの基本原則",
            # testing.instructions.md
            "基本方針",
            # api.instructions.md では "禁止事項" をルール定義として扱う
            "禁止事項",
            "Prohibited Actions",
        ],
    ),
]

# ──────────────────────────────────────────────────────────────
# Naming Convention Patterns
# ──────────────────────────────────────────────────────────────
INSTRUCTION_FILENAME_PATTERN = r"^[a-z][a-z0-9\-]*\.instructions\.md$"
PROMPT_FILENAME_PATTERN       = r"^[a-z][a-z0-9\-]*\.prompt\.md$"
SKILL_FILENAME_PATTERN        = r"^SKILL\.md$"

# ──────────────────────────────────────────────────────────────
# Placeholder path patterns to skip in referenced path checks
# ──────────────────────────────────────────────────────────────
PATH_PLACEHOLDER_PATTERNS = [
    r"^example/",
    r"^<",
    r"^\$\{",
    r"^/path/to/",
    r"^your/",
    r"^\.\.\.",
    r"<project-root>",
    r"<skill-name>",
]

# ──────────────────────────────────────────────────────────────
# Rule descriptions (for reporting)
# ──────────────────────────────────────────────────────────────
RULE_DESCRIPTIONS = {
    RULE_INFO:                          "Information / summary",
    RULE_REQUIRED_FILE_MISSING:         "Required file does not exist",
    RULE_BROKEN_INTERNAL_LINK:          "Broken internal link",
    RULE_INVALID_PATH_REFERENCE:        "Referenced path does not exist",
    RULE_INVALID_SKILL_STRUCTURE:       "Invalid Skill structure",
    RULE_INVALID_PROMPT_STRUCTURE:      "Invalid Prompt structure",
    RULE_INVALID_INSTRUCTION_STRUCTURE: "Invalid Instruction structure",
    RULE_MISSING_REQUIRED_SECTION:      "Missing required section",
    RULE_MISSING_REFERENCED_SKILL:      "Prompt references missing Skill",
    RULE_MISSING_REFERENCED_PROMPT:     "Missing referenced Prompt",
    RULE_DEPRECATED_DOC_REFERENCE:      "Deprecated document is referenced",
    RULE_SOURCE_OF_TRUTH_CONFLICT:      "Source of Truth conflict",
    RULE_INVALID_METADATA:              "Invalid metadata",
    RULE_INVALID_MANIFEST:              "Invalid manifest",
    RULE_INVALID_NAMING_CONVENTION:     "Invalid naming convention",
}
