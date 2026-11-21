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
CLAUDE_ONLY=(core/claude/90-verifica.md)
EDITORIAL=(core/editorial/20-role.md core/editorial/21-article-format.md core/editorial/22-seo.md core/editorial/23-content-types.md core/editorial/24-lexicon.md)

# claude.ai rifiuta una skill con la descrizione oltre i 1024 caratteri: meglio
# accorgersene qui che al momento del caricamento.
python3 - adapters/claude-skill/*-frontmatter.yaml <<'PY'
import re, sys
sys.stderr.reconfigure(encoding="utf-8")
errori = 0
for nome in sys.argv[1:]:
    testo = open(nome, encoding="utf-8").read()
    m = re.search(r"^description: (.*)$", testo, re.M)
    n = len(m.group(1)) if m else 0
    if not m or n > 1024:
        print(f"errore: {nome}: description di {n} caratteri, il limite è 1024",
              file=sys.stderr)
        errori += 1
    elif n > 950:
        print(f"attenzione: {nome}: description di {n} caratteri su 1024", file=sys.stderr)
sys.exit(1 if errori else 0)
PY

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

# --- Claude Skills: frontmatter + corpo + modulo solo Claude + script ---
# Solo le skill di Claude possono eseguire codice: ricevono lo script di
# verifica e le istruzioni per usarlo. Gli altri adapter restano testo unico.
for skill in social editorial; do
  dir="$DEST/claude-skill/$skill-progetto-ciclismo"
  { cat "adapters/claude-skill/$skill-frontmatter.yaml" "$WORK/$skill.md"
    for f in "${CLAUDE_ONLY[@]}"; do cat "$f"; echo ""; done
  } > "$dir/SKILL.md"
  mkdir -p "$dir/scripts"
  cp scripts/verifica_testo.py "$dir/scripts/verifica_testo.py"
done

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
