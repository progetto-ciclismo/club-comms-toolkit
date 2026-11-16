#!/usr/bin/env bash
# Assembla gli adapter di piattaforma per le due skill (social ed editorial)
# a partire dai moduli in core/ e templates/.
# Modifica SEMPRE core/ e templates/, mai gli adapter generati.
#
# Uso:
#   ./build.sh           rigenera gli adapter in adapters/
#   ./build.sh --check    verifica che gli adapter siano allineati al sorgente
#                         senza modificarli; esce con 1 se sono disallineati
set -euo pipefail

# Il build usa percorsi relativi: lavora sempre dalla radice del repository.
cd "$(dirname "${BASH_SOURCE[0]}")"

CHECK=0
case "${1:-}" in
  --check) CHECK=1 ;;
  "")      ;;
  *)       echo "Uso: $0 [--check]" >&2; exit 2 ;;
esac

SHARED=(core/shared/00-identity.md core/shared/01-shared-rules.md)
SOCIAL=(core/social/10-role.md core/social/11-triggers.md core/social/12-style.md core/social/13-content-rules.md core/social/14-platforms.md core/social/19-templates.md)
EDITORIAL=(core/editorial/20-role.md core/editorial/21-article-format.md core/editorial/22-seo.md core/editorial/23-content-types.md core/editorial/24-lexicon.md)

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

assemble() {
  local out="$1"; shift
  : > "$out"
  for f in "$@"; do
    cat "$f" >> "$out"
    echo "" >> "$out"
  done
}

# Il ruolo va per primo, poi identità e regole comuni, poi le regole specifiche.
# Nella skill social la tabella "cosa produrre" segue subito il ruolo: il modello
# sa quale output gli serve prima di leggere le regole di dettaglio.
assemble "$WORK/social.md" "${SOCIAL[0]}" "${SOCIAL[1]}" "${SHARED[@]}" "${SOCIAL[@]:2}"
python3 scripts/inline_templates.py "$WORK/social.md"

assemble "$WORK/editorial.md" "${EDITORIAL[0]}" "${SHARED[@]}" "${EDITORIAL[@]:1}"
python3 scripts/inline_templates.py "$WORK/editorial.md"

# In modalità --check si scrive su una copia usa e getta, così adapters/ resta
# intatto e alla fine si confronta il generato con il committato.
if [ "$CHECK" -eq 1 ]; then
  DEST="$WORK/adapters"
  cp -r adapters "$DEST"
else
  DEST="adapters"
fi

mkdir -p "$DEST/claude-skill/social-progetto-ciclismo"
mkdir -p "$DEST/claude-skill/editorial-progetto-ciclismo"
mkdir -p "$DEST/gemini-gem" "$DEST/openai-gpt" "$DEST/generic"

# --- Claude Skills: frontmatter + corpo ---
cat adapters/claude-skill/social-frontmatter.yaml "$WORK/social.md" \
  > "$DEST/claude-skill/social-progetto-ciclismo/SKILL.md"
cat adapters/claude-skill/editorial-frontmatter.yaml "$WORK/editorial.md" \
  > "$DEST/claude-skill/editorial-progetto-ciclismo/SKILL.md"

# --- Gemini Gems ---
{ echo "<!-- Incolla nel campo Instructions della Gem. -->"; echo ""; cat "$WORK/social.md"; } \
  > "$DEST/gemini-gem/social-instructions.md"
{ echo "<!-- Incolla nel campo Instructions della Gem. -->"; echo ""; cat "$WORK/editorial.md"; } \
  > "$DEST/gemini-gem/editorial-instructions.md"

# --- OpenAI GPTs ---
{ echo "<!-- Incolla nel campo Instructions del GPT. -->"; echo ""; cat "$WORK/social.md"; } \
  > "$DEST/openai-gpt/social-instructions.md"
{ echo "<!-- Incolla nel campo Instructions del GPT. -->"; echo ""; cat "$WORK/editorial.md"; } \
  > "$DEST/openai-gpt/editorial-instructions.md"

# --- System prompt generici ---
cp "$WORK/social.md" "$DEST/generic/social-system-prompt.md"
cp "$WORK/editorial.md" "$DEST/generic/editorial-system-prompt.md"

if [ "$CHECK" -eq 1 ]; then
  if diff -ru adapters "$DEST"; then
    echo "Adapter allineati al sorgente."
  else
    echo "" >&2
    echo "Adapter DISALLINEATI dal sorgente." >&2
    echo "Esegui ./build.sh e committa il risultato." >&2
    exit 1
  fi
  exit 0
fi

echo "Build completata:"
find adapters -name "*.md" | sort | sed 's/^/  /'
