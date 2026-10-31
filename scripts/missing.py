#!/usr/bin/env python3
"""Untranslated keys per module: npm run missing [-- <module-substring>] [--max-len N]

No args: top 40 modules by untranslated count. With a substring: list that module's
untranslated strings (skips icon/colour/*Description keys and strings longer than --max-len, default 90).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir
from collections import Counter
from nls import english, translations

argv = sys.argv[1:]
max_len = 90
if "--max-len" in argv:
    i = argv.index("--max-len")
    max_len = int(argv[i + 1])
    del argv[i:i + 2]
done = translations()
todo = [(m, k, t) for m, k, t in english() if k not in done.get(m, {})]
if not argv:
    for mod, n in Counter(m for m, _, _ in todo).most_common(40):
        print(f"{n:5d}  {mod}")
    print(f"{len(todo)} untranslated of {len(english())}")
else:
    for mod, key, text in todo:
        low = key.lower()
        if argv[0] in mod and "icon" not in low and "description" not in low and len(text) <= max_len:
            print(f"{mod.split('/')[-1]} | {key} | {text!r}")
