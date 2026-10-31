"""Shared loaders for the scripts: VS Code's English NLS data and our translations."""
import json, os

OUT = os.environ.get("VSCODE_OUT", "/Applications/Visual Studio Code.app/Contents/Resources/app/out/")
TRANSLATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "translations", "main.i18n.json")


def english():
    """Ordered list of (module, key, English text) for every VS Code UI string."""
    keys = json.load(open(os.path.join(OUT, "nls.keys.json"), encoding="utf-8"))
    msgs = json.load(open(os.path.join(OUT, "nls.messages.json"), encoding="utf-8"))
    rows, i = [], 0
    for mod, ks in keys:
        for k in ks:
            rows.append((mod, k, msgs[i]))
            i += 1
    return rows


def translations():
    """{module: {key: Bengali text}}"""
    return json.load(open(TRANSLATIONS, encoding="utf-8"))["contents"]
