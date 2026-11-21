#!/usr/bin/env python3
"""Controlla le regole meccaniche dei testi prodotti dalle skill.

Il modello conta male i caratteri e dimentica le regole tipografiche: questo
script verifica ciò che si può misurare, non lo stile.

Uso:
    python3 scripts/verifica_testo.py FILE [FILE ...]
    python3 scripts/verifica_testo.py -          (legge da standard input)
    python3 scripts/verifica_testo.py --canale threads FILE

Il testo viene diviso in sezioni dalle intestazioni (righe che iniziano con
`#` o interamente in grassetto, come `**Instagram**` o `### Threads 1/2`).
Il canale di ogni sezione si ricava dall'intestazione; senza intestazioni il
testo è un post base, o un articolo se contiene la scheda SEO. Con --canale tutto il testo è trattato come quel canale.

Esce con 1 se trova errori; gli avvisi non cambiano l'esito.
"""
import argparse
import re
import sys
import unicodedata

LIMITE_SEO = 191
LIMITE_THREADS = 500
LIMITE_ANTEPRIMA_IG = 125
LIMITE_ALT = 125
EMOJI_MIN, EMOJI_MAX = 5, 10

CANALI = ("base", "instagram", "story", "threads", "seo", "slug", "alt",
          "hashtag", "articolo", "altro")

INTESTAZIONE = re.compile(r"^\s*(#{1,6}\s+.+|\*\*[^*]+\*\*[^a-zà-ù]*(\(.*\))?\s*:?\s*)$")
# Righe "**Campo:** valore" della scheda SEO.
CAMPO = re.compile(r"^\s*\*\*(Slug|Testo alternativo[^*:]*|Frase SEO[^*:]*)\s*:?\s*\*\*\s*:?\s*(.*)$",
                   re.IGNORECASE)
ALTRO_CAMPO = re.compile(r"^\s*\*\*[^*]+:\s*\*\*|^\s*\*\*[^*]+\*\*\s*:\s*\S")
HASHTAG = re.compile(r"(?<![\w&/#])#[^\W\d_][\w]*", re.UNICODE)
LINK = re.compile(r"https?://\S+|www\.\S+")

# Una emoji: un simbolo pittografico con eventuali selettori, toni della pelle
# e sequenze ZWJ, oppure una coppia di indicatori regionali (bandiera).
_PITTO = (r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿"
          r"←-⇿〰〽㊗㊙©®‼⁉]")
EMOJI = re.compile(
    r"[\U0001F1E6-\U0001F1FF]{2}"
    rf"|{_PITTO}[️\U0001F3FB-\U0001F3FF]*(?:‍{_PITTO}[️\U0001F3FB-\U0001F3FF]*)*"
)


# Costruzioni tipiche dei testi generati (sezione "Scrittura naturale" delle
# regole comuni). Sono indizi, non certezze: producono avvisi, non errori.
CANALI_DI_TESTO = ("base", "instagram", "story", "threads", "articolo")
TIC = (
    ("contrapposizione a effetto",
     re.compile(r"\b[Nn]on (?:è|e'|sono|era|erano|sarà|saranno) solo\b[^.!?\n]{0,60}?"
                r"[,;:]\s*(?:ma\s+)?(?:è|e'|sono|era|erano|sarà|saranno)\b")),
    ("domanda con risposta immediata",
     re.compile(r"(?:^|(?<=[.!…]\s))(?:[^\s?.!]+[ \t]+){0,3}[^\s?.!]+\?[ \t]+"
                r"(?=[A-ZÀÈÉÌÒÙ0-9])", re.M)),
    ("domanda al pubblico", re.compile(r"\bE voi\b[^?\n]{0,80}\?")),
    ("frase fatta",
     re.compile(r"\bda incorniciare\b|\bnuova pagina\b|\btestimonianza d[i'ea]",
                re.IGNORECASE)),
)


def conta_emoji(testo):
    return len(EMOJI.findall(testo))


def canale_da_intestazione(riga, predefinito):
    t = riga.lower()
    if "hashtag" in t:
        return "hashtag"
    if "story" in t or "storia" in t:
        return "story"
    if "threads" in t or "corta" in t:
        return "threads"
    if "instagram" in t or "media" in t:
        return "instagram"
    if "frase seo" in t:
        return "seo"
    if "slug" in t:
        return "slug"
    if "testo alternativo" in t:
        return "alt"
    if "scheda seo" in t:
        return "altro"
    if any(k in t for k in ("post base", "lunga", "facebook", "whatsapp")):
        return "base"
    return predefinito


def sezioni(testo, canale_forzato=None, predefinito="base"):
    """Restituisce (titolo, canale, righe) per ogni sezione."""
    if canale_forzato:
        return [("(intero testo)", canale_forzato, testo.splitlines())]
    out = []
    titolo, canale, righe = "(inizio)", predefinito, []

    def chiudi():
        if any(r.strip() for r in righe):
            out.append((titolo, canale, list(righe)))

    for riga in testo.splitlines():
        campo = CAMPO.match(riga)
        if campo:
            chiudi()
            nome = campo.group(1).lower()
            c = "slug" if "slug" in nome else "alt" if "alternativo" in nome else "seo"
            # "(max 191 caratteri):" dopo il nome del campo non fa parte del testo.
            valore = re.sub(r"^\(.*?\)\s*:?\s*", "", campo.group(2))
            titolo, canale, righe = campo.group(1).strip(), c, [valore] if valore else []
            continue
        if ALTRO_CAMPO.match(riga):
            # Un campo della scheda che lo script non controlla (Categorie,
            # Link interno): chiude la sezione precedente.
            chiudi()
            titolo, canale, righe = riga.strip(), "altro", []
            continue
        if INTESTAZIONE.match(riga):
            chiudi()
            titolo, canale, righe = riga.strip(), canale_da_intestazione(riga, predefinito), []
            continue
        if riga.strip() == "---" or riga.lstrip().startswith(">"):
            continue
        righe.append(riga)
    chiudi()
    return out


def testo_pubblicabile(righe):
    """Il testo come verrebbe pubblicato: senza righe vuote ai bordi."""
    return "\n".join(righe).strip()


def controlla(titolo, canale, righe):
    errori, avvisi = [], []
    testo = testo_pubblicabile(righe)
    if not testo or canale == "altro":
        return errori, avvisi

    # Regole valide per tutti i canali.
    if canale != "hashtag":
        tag = HASHTAG.findall(testo)
        if tag:
            errori.append(f"hashtag nel testo ({' '.join(tag)}): vanno nel blocco "
                          "'Hashtag consigliati'")
    if re.search(r"Progetto Ciclismo\s*[–—]\s*Rodengo", testo):
        errori.append("denominazione con trattino lungo: usa "
                      "'A.S.D. Progetto Ciclismo - Rodengo Saiano'")
    elif re.search(r"[–—]", testo):
        avvisi.append("trattino lungo (– o —): nella comunicazione si usa il trattino breve")
    for m in re.finditer(r"\b\d+°\s+(posizione|piazza|batteria|tappa|prova|edizione)\b"
                         r"|\(\d+°\s+nelle\b|\b\d+°\s+nelle\b|\b\d+°\s+tra\s+le\b", testo):
        avvisi.append(f"'{m.group(0)}': con un nome o una categoria femminile serve ª")
    for m in re.finditer(r"\b\d+ª\s+nei\b|\b\d+ª\s+(posto|classificato)\b", testo):
        avvisi.append(f"'{m.group(0)}': con un nome o una categoria maschile serve °")
    if canale in CANALI_DI_TESTO:
        for nome, schema in TIC:
            for m in schema.finditer(testo):
                avvisi.append(f"{nome}: '{' '.join(m.group(0).split())}' "
                              "(vedi 'Scrittura naturale')")

    if canale == "hashtag":
        tag = HASHTAG.findall(testo)
        if not 3 <= len(tag) <= 5:
            avvisi.append(f"{len(tag)} hashtag consigliati: ne servono da 3 a 5")
        for t in tag:
            if any(unicodedata.combining(c) for c in unicodedata.normalize("NFD", t)):
                errori.append(f"hashtag con accento: {t}")

    elif canale == "seo":
        # Una riga spezzata a capo nel Markdown resta un solo paragrafo.
        paragrafi = [" ".join(p.split()) for p in re.split(r"\n\s*\n", testo) if p.strip()]
        if len(paragrafi) > 1:
            errori.append("la frase SEO deve stare su una sola riga")
        n = len(paragrafi[0]) if paragrafi else 0
        if n > LIMITE_SEO:
            errori.append(f"frase SEO di {n} caratteri: il limite è {LIMITE_SEO}")

    elif canale == "slug":
        slug = testo.strip().strip("`")
        if slug.startswith("[") or not slug:
            return errori, avvisi
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            errori.append(f"slug non valido '{slug}': solo minuscole, cifre e trattini, "
                          "senza accenti")
        if re.search(r"-\d$", slug) and not re.search(r"-(19|20)\d\d$", slug):
            avvisi.append(f"slug '{slug}' finisce con un suffisso numerico: "
                          "è un doppione di WordPress?")

    elif canale == "alt":
        if testo.startswith("["):
            return errori, avvisi
        if len(testo) > LIMITE_ALT:
            avvisi.append(f"testo alternativo di {len(testo)} caratteri: "
                          f"tienilo entro {LIMITE_ALT}")
        if re.match(r"(?i)(immagine|foto)\s+di\b", testo):
            avvisi.append("testo alternativo che inizia con 'Immagine di' o 'Foto di'")

    elif canale == "threads":
        n = len(testo)
        if n > LIMITE_THREADS:
            errori.append(f"{n} caratteri: Threads accetta al massimo "
                          f"{LIMITE_THREADS} caratteri per post")

    elif canale == "instagram":
        if LINK.search(testo) or "[link]" in testo:
            errori.append("link nella didascalia Instagram: va sostituito dal "
                          "rimando alle storie")
        prima = testo.splitlines()[0]
        if len(prima) > LIMITE_ANTEPRIMA_IG:
            avvisi.append(f"prima riga di {len(prima)} caratteri: su Instagram se ne "
                          f"vedono circa {LIMITE_ANTEPRIMA_IG} prima di 'altro'")

    if canale in ("base", "instagram"):
        n = conta_emoji(testo)
        if not EMOJI_MIN <= n <= EMOJI_MAX:
            avvisi.append(f"{n} emoji: nei post la norma è {EMOJI_MIN}-{EMOJI_MAX} "
                          "(3-4 nei flash e nei post brevi)")
        if canale == "base" and len(testo) > LIMITE_THREADS:
            avvisi.append(f"{len(testo)} caratteri: per Threads serve una versione "
                          "condensata o un piccolo thread")

    return errori, avvisi


def main():
    for flusso in (sys.stdin, sys.stdout, sys.stderr):
        try:
            flusso.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", nargs="+", help="file da controllare, o - per lo standard input")
    ap.add_argument("--canale", choices=CANALI,
                    help="tratta tutto il testo come questo canale")
    ap.add_argument("--tipo", choices=("auto", "social", "articolo"), default="auto",
                    help="canale delle sezioni senza intestazione riconoscibile: "
                         "post base (social) o articolo per il sito; auto lo "
                         "ricava dalla presenza della scheda SEO")
    args = ap.parse_args()

    totale_errori = 0
    for nome in args.file:
        testo = sys.stdin.read() if nome == "-" else open(nome, encoding="utf-8").read()
        print(f"== {nome}")
        tipo = args.tipo
        if tipo == "auto":
            articolo = re.search(r"\*\*(Frase SEO|Slug)|^# Risultati Cat\.", testo, re.M)
            tipo = "articolo" if articolo else "social"
        predefinito = "articolo" if tipo == "articolo" else "base"
        for titolo, canale, righe in sezioni(testo, args.canale, predefinito):
            errori, avvisi = controlla(titolo, canale, righe)
            for e in errori:
                print(f"  ERRORE  [{canale}] {titolo}: {e}")
            for a in avvisi:
                print(f"  avviso  [{canale}] {titolo}: {a}")
            totale_errori += len(errori)
    print(f"{totale_errori} errori")
    return 1 if totale_errori else 0


if __name__ == "__main__":
    sys.exit(main())
