#!/usr/bin/env bash
# Assembla gli adapter di piattaforma per le due skill (social ed editorial)
# a partire dai moduli in core/ e templates/.
# Modifica SEMPRE core/ e templates/, mai gli adapter generati.
set -euo pipefail

SHARED=(core/shared/00-identity.md core/shared/01-shared-rules.md)
SOCIAL=(core/social/10-role.md core/social/11-style.md core/social/12-content-rules.md core/social/13-triggers.md)
EDITORIAL=(core/editorial/20-role.md core/editorial/21-article-format.md core/editorial/22-seo.md core/editorial/23-content-types.md core/editorial/24-lexicon.md)

assemble() {
  local out="$1"; shift
  : > "$out"
  for f in "$@"; do
    cat "$f" >> "$out"
    echo "" >> "$out"
  done
}

# Il ruolo va per primo, poi identità e regole comuni, poi le regole specifiche.
build_social() {
  assemble /tmp/_social.md "${SOCIAL[0]}" "${SHARED[@]}" "${SOCIAL[@]:1}"
  python3 scripts/inline_templates.py /tmp/_social.md
}

build_editorial() {
  assemble /tmp/_editorial.md "${EDITORIAL[0]}" "${SHARED[@]}" "${EDITORIAL[@]:1}"
  python3 scripts/inline_templates.py /tmp/_editorial.md
}

build_social
build_editorial

mkdir -p adapters/claude-skill/social-progetto-ciclismo
mkdir -p adapters/claude-skill/editorial-progetto-ciclismo
mkdir -p adapters/gemini-gem adapters/openai-gpt adapters/generic

# --- Claude Skills: frontmatter + corpo ---
cat adapters/claude-skill/social-frontmatter.yaml /tmp/_social.md \
  > adapters/claude-skill/social-progetto-ciclismo/SKILL.md
cat adapters/claude-skill/editorial-frontmatter.yaml /tmp/_editorial.md \
  > adapters/claude-skill/editorial-progetto-ciclismo/SKILL.md

# --- Gemini Gems ---
{ echo "<!-- Incolla nel campo Instructions della Gem. -->"; echo ""; cat /tmp/_social.md; } \
  > adapters/gemini-gem/social-instructions.md
{ echo "<!-- Incolla nel campo Instructions della Gem. -->"; echo ""; cat /tmp/_editorial.md; } \
  > adapters/gemini-gem/editorial-instructions.md

# --- OpenAI GPTs ---
{ echo "<!-- Incolla nel campo Instructions del GPT. -->"; echo ""; cat /tmp/_social.md; } \
  > adapters/openai-gpt/social-instructions.md
{ echo "<!-- Incolla nel campo Instructions del GPT. -->"; echo ""; cat /tmp/_editorial.md; } \
  > adapters/openai-gpt/editorial-instructions.md

# --- System prompt generici ---
cp /tmp/_social.md adapters/generic/social-system-prompt.md
cp /tmp/_editorial.md adapters/generic/editorial-system-prompt.md

rm -f /tmp/_social.md /tmp/_editorial.md

echo "Build completata:"
find adapters -name "*.md" | sort | sed 's/^/  /'
