# YAML Linting Tools — Research Snapshot
# Source: Temporary Grok account (skill-creator session)
# Date: May 2026
# Status: ARCHIVAL — preserved as-found, unedited
# Context: Extracted before account access loss
# Relevance: Governance toolchain for SKILL.md frontmatter validation
#            Pairs with init-skill-archive.sh + validate-skill-archive.sh

---

## 1. yamllint — The Clear Winner for Most Projects

Repository: adrienverge/yamllint (https://github.com/adrienverge/yamllint)
Latest version: v1.38.0 (released January 13, 2026)
Stars: ~3.4k+ | Actively maintained

Why it's the most recommended:
- Checks syntax + style/cosmetic issues (not just "is it valid YAML?")
- Highly configurable with a .yamllint file
- Supports inline disable comments (# yamllint disable-line)
- Excellent for CI/CD, pre-commit hooks, and scripts
- Listed on the official yaml.org/tools page

Key rules it checks:
- indentation, line-length, trailing-spaces
- key-duplicates (repeated keys)
- colons, brackets, truthy (e.g. True vs true)
- Comments, empty values, and more

Installation (Linux):

  # Ubuntu / Debian
  sudo apt install yamllint

  # Fedora / RHEL / Rocky
  sudo dnf install yamllint

  # pip (always gets the latest)
  pip install --user yamllint

Basic usage:

  yamllint file.yaml
  yamllint .
  yamllint -c .yamllint myfile.yaml

Example .yamllint config:

  extends: default

  rules:
    line-length:
      max: 120
    key-duplicates: disable          # useful for some Docker Compose files
    indentation:
      spaces: 2
      indent-sequences: consistent

---

## 2. Best IDE Experience: Red Hat YAML (VS Code)

Extension: "YAML" by Red Hat
- Real-time linting + schema validation (Kubernetes, OpenAPI, GitHub Actions, etc.)
- Autocompletion, hover documentation, formatting
- Powers most professional YAML workflows in 2026

Highly recommended alongside yamllint for local development.

---

## 3. Complementary Formatters (Auto-fix style issues)

Tool          | Language | Best For                  | Auto-fix yamllint issues? | Notes
yamlfix       | Python   | Fixing yamllint problems  | Excellent                 | Converts True→true, removes unnecessary quotes, adds --- header
Google yamlfmt| Go       | Fast, opinionated format  | Good                      | Very fast, preserves anchors well
Prettier      | Node.js  | Multi-language projects   | Good                      | Use if already using Prettier for JS/TS/Markdown

---

## 4. Other Strong Options

Tool                        | Type                  | Best Use Case                        | Notes
yq (mikefarah/yq)           | CLI processor+valid.  | Validation + transformation          | Extremely powerful (like jq for YAML)
yamale                      | Schema validator      | Strict contracts / data pipelines    | Validates against a schema file
Mega-Linter / Super-Linter  | CI/CD aggregator      | Full linting suite in GitHub Actions | Runs yamllint + many others
Spectral                    | OpenAPI/AsyncAPI      | API specs                            | Excellent for OpenAPI YAML

---

## Recommendation for Skill Creator Workflow

Since SKILL.md files have YAML frontmatter, recommended stack:

1. PRIMARY:  yamllint (robust style + syntax checking)
2. AUTO-FIX: yamlfix (run before committing)
3. IDE:      VS Code + Red Hat YAML extension

---

## Pending (not yet extracted from temp account)

- Updated validate-skill.sh with yamllint integration
- .yamllint config optimized for skill files
- Pre-commit hook example
- yamllint + yamlfix combined command

---
# END ARCHIVAL SNAPSHOT
