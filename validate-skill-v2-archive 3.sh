#!/usr/bin/env bash
# validate-skill.sh — Comprehensive Skill Validator
# Version: 2.0 (Expanded with yamllint + advanced checks)
# Source: Temporary Grok account (skill-creator session)
# Date: May 2026
# Status: ARCHIVAL — preserved as-found, unedited
#
# Usage:
#   validate-skill.sh <skill-directory>
#   validate-skill.sh --all                    # Validate all skills in .grok/skills/
#
# Features:
#   - YAML frontmatter structure validation
#   - yamllint integration (style + syntax)
#   - Name format, description quality, length checks
#   - Typographic dash detection
#   - Line count warnings
#   - Colored output + summary

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

die() {
    echo -e "${RED}FAIL:${NC} $*" >&2
    exit 1
}

warn() {
    echo -e "${YELLOW}WARN:${NC} $*"
}

info() {
    echo -e "${BLUE}INFO:${NC} $*"
}

success() {
    echo -e "${GREEN}OK:${NC} $*"
}

# --- Main Validation Function ---
validate_skill() {
    local SKILL_DIR="$1"
    local SKILL_MD="$SKILL_DIR/SKILL.md"

    [[ -d "$SKILL_DIR" ]] || die "Directory does not exist: $SKILL_DIR"
    [[ -f "$SKILL_MD" ]]  || die "SKILL.md not found in $SKILL_DIR"

    echo -e "\n${BLUE}=== Validating skill: $(basename "$SKILL_DIR") ===${NC}"

    CONTENT=$(<"$SKILL_MD")

    # 1. Check for proper frontmatter delimiters
    if [[ "$CONTENT" != ---* ]]; then
        FIRST3=$(echo "$CONTENT" | head -c 12)
        if echo "$FIRST3" | LC_ALL=C grep -qP '[\x{2010}-\x{2015}\x{FE58}\x{FE63}\x{FF0D}]' 2>/dev/null; then
            die "SKILL.md starts with typographic dashes. Use plain ASCII --- (U+002D)"
        fi
        die "SKILL.md must start with --- (YAML frontmatter)"
    fi

    # 2. Extract frontmatter and body
    FRONTMATTER=$(echo "$CONTENT" | awk '/^---$/{n++; next} n==1')
    [[ -n "$FRONTMATTER" ]] || die "Empty or malformed frontmatter"

    BODY=$(echo "$CONTENT" | awk '/^---$/{n++; next} n>=2')
    BODY_TRIMMED=$(echo "$BODY" | sed '/^[[:space:]]*$/d')
    [[ -n "$BODY_TRIMMED" ]] || die "SKILL.md body is empty after frontmatter"

    # 3. Extract and validate name
    NAME=$(echo "$FRONTMATTER" | grep -m1 '^name:' | sed 's/^name:[[:space:]]*//')
    [[ -n "$NAME" ]] || die "Missing 'name' in frontmatter"
    [[ ${#NAME} -ge 2 ]] || die "Name too short (min 2 chars)"
    [[ ${#NAME} -le 64 ]] || die "Name too long (max 64 chars)"
    if ! echo "$NAME" | grep -qE '^[a-z0-9][a-z0-9-]*[a-z0-9]$'; then
        die "Name must be kebab-case (lowercase letters, digits, hyphens only)"
    fi

    # 4. Extract and validate description
    DESC_LINE=$(echo "$FRONTMATTER" | grep -m1 '^description:')
    [[ -n "$DESC_LINE" ]] || die "Missing 'description' in frontmatter"

    DESCRIPTION=$(echo "$DESC_LINE" | sed 's/^description:[[:space:]]*//')
    if [[ "$DESCRIPTION" =~ ^\"(.*)\"$ ]] || [[ "$DESCRIPTION" =~ ^\'(.*)\'$ ]]; then
        DESCRIPTION="${BASH_REMATCH[1]}"
    fi
    [[ -n "$DESCRIPTION" ]] || die "Description cannot be empty"

    # Check for unquoted colons
    RAW_VALUE=$(echo "$DESC_LINE" | sed 's/^description:[[:space:]]*//')
    if echo "$RAW_VALUE" | grep -q ': ' && [[ ! "$RAW_VALUE" =~ ^\" ]] && [[ ! "$RAW_VALUE" =~ ^\' ]]; then
        die "Description contains unquoted ': ' — wrap in quotes"
    fi

    # Check for TODO
    if echo "$DESCRIPTION" | grep -qi 'TODO'; then
        die "Description still contains TODO placeholder"
    fi

    # Check length
    DESC_LEN=${#DESCRIPTION}
    if [[ "$DESC_LEN" -gt 1024 ]]; then
        die "Description too long ($DESC_LEN chars, max 1024)"
    fi

    # 5. Run yamllint (if available)
    if command -v yamllint >/dev/null 2>&1; then
        if [[ -f ".yamllint" ]]; then
            if ! yamllint -c .yamllint "$SKILL_MD" >/dev/null 2>&1; then
                warn "yamllint found style issues in $SKILL_MD"
                yamllint -c .yamllint "$SKILL_MD" || true
            else
                success "yamllint passed"
            fi
        else
            warn "No .yamllint config found — using default rules"
            yamllint "$SKILL_MD" || true
        fi
    else
        warn "yamllint not installed. Install with: pip install yamllint"
    fi

    # 6. Line count warning
    LINE_COUNT=$(echo "$CONTENT" | wc -l | tr -d ' ')
    if [[ "$LINE_COUNT" -gt 500 ]]; then
        warn "SKILL.md is $LINE_COUNT lines (recommended ≤500). Consider splitting into references/"
    fi

    success "Skill '$NAME' is valid ($LINE_COUNT lines, description: $DESC_LEN chars)"
}

# --- Main Entry Point ---
if [[ "${1:-}" == "--all" ]]; then
    SKILLS_DIR="/home/workdir/.grok/skills"
    [[ -d "$SKILLS_DIR" ]] || die "Skills directory not found: $SKILLS_DIR"

    echo -e "${BLUE}Validating all skills in $SKILLS_DIR...${NC}\n"
    for dir in "$SKILLS_DIR"/*/; do
        [[ -d "$dir" ]] && validate_skill "${dir%/}"
    done
    echo -e "\n${GREEN}All skills validated.${NC}"
else
    [[ $# -ne 1 ]] && die "Usage: validate-skill.sh <skill-directory>  or  --all"
    validate_skill "$1"
fi
