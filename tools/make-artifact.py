#!/usr/bin/env python3
"""Builds the claude.ai Artifact version of index.html.

The artifact host supplies its own <head>, safe-area padding and runs without service workers,
so everything between the PWA-START / PWA-END markers is dropped, along with the document wrapper tags.

Usage: python3 tools/make-artifact.py [output-path]
"""
import base64
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")

src = re.sub(r"<!--PWA-START-->.*?<!--PWA-END-->", "", src, flags=re.S)
src = re.sub(r"/\*PWA-START\*/.*?/\*PWA-END\*/", "", src, flags=re.S)
src = re.sub(r"<!doctype html>\s*", "", src, flags=re.I)
src = re.sub(r"</?(html|head|body)[^>]*>\s*", "", src, flags=re.I)
src = re.sub(r"\n{3,}", "\n\n", src).strip() + "\n"

# Artifacts can't load sibling files, so the logo is inlined as a data: URI.
logo = base64.b64encode((root / "icons" / "logo.jpg").read_bytes()).decode("ascii")
src = src.replace("'icons/logo.jpg'", "'data:image/jpeg;base64," + logo + "'")

out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "artifact.html"
out.write_text(src, encoding="utf-8")
print(f"wrote {out}")
