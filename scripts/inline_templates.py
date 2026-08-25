#!/usr/bin/env python3
"""Sostituisce i riferimenti alle cartelle template con il contenuto inline.

Un riferimento non risolto verrebbe spedito così com'è dentro l'adapter,
lasciando al modello l'istruzione di leggere una cartella a cui non ha
accesso: in quel caso il build deve fallire, non proseguire in silenzio.
"""
import pathlib
import re
import sys

RIFERIMENTO = re.compile(r"Usa i template in `([^`]+)`\.")

target = pathlib.Path(sys.argv[1])
body = target.read_text(encoding="utf-8")

espansi = 0


def expand(match):
    global espansi
    folder = pathlib.Path(match.group(1))
    if not folder.is_dir():
        raise SystemExit(f"errore: cartella template inesistente: {folder}")
    paths = sorted(folder.glob("*.md"))
    if not paths:
        raise SystemExit(f"errore: nessun template in {folder}")
    blocks = []
    for path in paths:
        content = path.read_text(encoding="utf-8").rstrip()
        blocks.append(f"### {path.stem}\n\n```\n{content}\n```")
    espansi += 1
    return "\n\n".join(blocks)


body = RIFERIMENTO.sub(expand, body)

if not espansi:
    raise SystemExit(f"errore: nessun riferimento a template trovato in {target}")

target.write_text(body, encoding="utf-8")
