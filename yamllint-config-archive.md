# yamllint Configuration — Archival Snapshot
# Source: Temporary Grok account (skill-creator session)
# Date: May 2026
# Status: ARCHIVAL — preserved as-found, unedited
# Context: Extracted before account access loss
# Relevance: YAML governance layer for SKILL.md frontmatter
#            Pairs with init-skill-archive.sh + validate-skill-archive.sh

---

## FILE 1: .yamllint
## Place in project root alongside your skill directories

# .yamllint - Optimized for YAML frontmatter (SKILL.md, Jekyll, Hugo, etc.)
extends: default

rules:
  # --- Core Style ---
  indentation:
    spaces: 2
    indent-sequences: consistent
    check-multi-line-strings: true

  line-length:
    max: 120                    # Relaxed for long descriptions
    level: warning              # Change to 'error' if you want strict enforcement

  trailing-spaces: enable
  new-line-at-end-of-file: enable

  # --- Frontmatter Best Practices ---
  key-duplicates: enable        # Prevent duplicate keys in frontmatter
  truthy: enable                # Enforce lowercase true/false/null
  colons: enable                # Proper spacing around colons

  # --- Comments (very common in frontmatter) ---
  comments:
    require-starting-space: true
    min-spaces-from-content: 2

  # --- Document Structure ---
  document-start:
    present: true               # Require opening ---
    level: warning

  # --- Relaxations for Frontmatter + Markdown ---
  empty-values: disable         # Allow empty values in frontmatter if needed
  quoted-strings:
    quote-type: any             # Allow both single and double quotes

---

## FILE 2: validate-skill.sh ADDITION
## Add this section inside validate-skill.sh after existing checks

# --- YAML Frontmatter Linting with yamllint ---
if command -v yamllint >/dev/null 2>&1; then
    echo "Running yamllint on frontmatter..."
    if ! yamllint -c .yamllint "$SKILL_MD" 2>&1; then
        die "yamllint found issues in $SKILL_MD"
    fi
    echo "OK: yamllint passed"
else
    echo "WARN: yamllint not installed. Run: pip install yamllint"
fi

---

## USAGE

# Lint a single file
yamllint -c .yamllint SKILL.md

# Lint all Markdown files with frontmatter
yamllint -c .yamllint **/*.md

# Lint with parsable output (great for CI)
yamllint -f parsable -c .yamllint .

---

## QUICK SETUP

# Install yamllint
pip install --user yamllint

# Create the config file
cat > .yamllint << 'EOF'
extends: default

rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
    indent-sequences: consistent
  key-duplicates: enable
  truthy: enable
  trailing-spaces: enable
  new-line-at-end-of-file: enable
  document-start:
    present: true
    level: warning
EOF

---

## STRICT VERSION (for team projects)

extends: default

rules:
  line-length:
    max: 100
    level: error
  key-duplicates: enable
  truthy: enable
  document-start:
    present: true
    level: error
  comments:
    require-starting-space: true

---

## PENDING (not yet extracted)
# - Full validate-skill.sh rewrite with yamllint fully integrated
# - Frontmatter-only linting version (ignores Markdown body)
# - Pre-commit hook example
# - yamllint + yamlfix combined command

---
# END ARCHIVAL SNAPSHOT
