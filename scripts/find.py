#!/usr/bin/env python3
"""Find the module + key of an English UI string: npm run find -- "New Folder" [--missing]

Prints `module | key | English`; a leading ✓ means already translated (shown with its Bengali).
--missing lists only untranslated hits. The `&&` mnemonic marker is ignored when matching.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir
from nls import english, translations

args = [a for a in sys.argv[1:] if a != "--missing"]
only_missing = "--missing" in sys.argv[1:]
if not args:
    sys.exit('usage: find.py "<text>" [--missing]')
query, done = args[0].lower(), translations()
for mod, key, text in english():
    if query in text.replace("&&", "").lower():
        bn = done.get(mod, {}).get(key)
        if bn is None:
            print(f"  {mod} | {key} | {text!r}")
        elif not only_missing:
            print(f"✓ {mod} | {key} | {text!r} -> {bn!r}")
