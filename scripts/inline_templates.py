#!/usr/bin/env python3
"""Sostituisce i riferimenti alle cartelle template con il contenuto inline."""
import pathlib
import re
import sys

target = pathlib.Path(sys.argv[1])
body = target.read_text(encoding="utf-8")


def expand(match):
    folder = pathlib.Path(match.group(1))
    if not folder.is_dir():
        return match.group(0)
    blocks = []
    for path in sorted(folder.glob("*.md")):
        content = path.read_text(encoding="utf-8").rstrip()
        blocks.append(f"### {path.stem}\n\n```\n{content}\n```")
    return "\n\n".join(blocks)


body = re.sub(r"Usa i template in `([^`]+)`\.", expand, body)
target.write_text(body, encoding="utf-8")
