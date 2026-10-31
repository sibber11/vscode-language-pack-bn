#!/usr/bin/env python3
"""Validate translations/main.i18n.json against the installed VS Code NLS files.

Errors (exit 1): unknown module/key, {n} placeholder mismatch, && count mismatch,
newline count mismatch, empty value, non-string value.
Warnings: text identical to English, glossary violation (ফাইল instead of নথি).

Override the VS Code location with VSCODE_OUT=/path/to/app/out/.
"""
import json, os, re, sys

OUT = os.environ.get("VSCODE_OUT", "/Applications/Visual Studio Code.app/Contents/Resources/app/out/")
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "translations", "main.i18n.json")

keys = json.load(open(os.path.join(OUT, "nls.keys.json"), encoding="utf-8"))
msgs = json.load(open(os.path.join(OUT, "nls.messages.json"), encoding="utf-8"))
english, i = {}, 0
for mod, ks in keys:
    for k in ks:
        english[(mod, k)] = msgs[i]
        i += 1

placeholders = lambda s: sorted(re.findall(r"\{\d+\}", s))
errors, warnings, count = [], [], 0
for mod, entries in json.load(open(FILE, encoding="utf-8"))["contents"].items():
    for key, text in entries.items():
        count += 1
        where = f"{mod} | {key}"
        en = english.get((mod, key))
        if en is None:
            errors.append(f"{where}: unknown module/key")
        elif not isinstance(text, str) or not text.strip():
            errors.append(f"{where}: empty or non-string value")
        else:
            if placeholders(en) != placeholders(text):
                errors.append(f"{where}: placeholders {placeholders(en)} != {placeholders(text)}")
            if en.count("&&") != text.count("&&"):
                errors.append(f"{where}: '&&' count {en.count('&&')} != {text.count('&&')}")
            if en.count("\n") != text.count("\n"):
                errors.append(f"{where}: newline count differs")
            if text == en and re.search(r"[a-z]{4,}", en):
                warnings.append(f"{where}: identical to English")
            if re.search(r"(?<!প্রো)ফাইল", text):  # প্রোফাইল (Profile) is allowed
                warnings.append(f"{where}: uses ফাইল, glossary says নথি")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{count} entries, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
