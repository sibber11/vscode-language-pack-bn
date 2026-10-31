# Bengali (bn) VS Code Language Pack

## Adding translations

All strings live in `translations/main.i18n.json` as `contents[<module path>][<key>] = <Bengali text>`.
Wrong module paths or keys fail silently (string stays English), so never hand-type them.

### 1. Find module + key for an English string

Source of truth: the installed VS Code's NLS files (`nls.keys.json` = `[module, [keys]]` flattened in order,
index-aligned with the `nls.messages.json` array).

```sh
python3 -I - "New Folder" <<'EOF'
import json,sys
b="/Applications/Visual Studio Code.app/Contents/Resources/app/out/"
keys=json.load(open(b+"nls.keys.json")); msgs=json.load(open(b+"nls.messages.json")); i=0
q=sys.argv[1].lower()
for mod,ks in keys:
    for k in ks:
        if q in msgs[i].replace("&&","").lower(): print(f"{mod} | {k} | {msgs[i]!r}")
        i+=1
EOF
```

Each line is one UI place. Menu items usually have `mi*` keys.

### 2. Add to `translations/main.i18n.json`

```json
"vs/workbench/contrib/files/browser/fileActions": {
	"newFolder": "নতুন ফোল্ডার"
}
```

- Existing module: add the key inside it. New module: add a block.
- `&&` count must equal the English; put it at the start of the Bengali text.
- Keep `{0}` `{1}` placeholders, trailing `...`, product names (VS Code, Git) unchanged.
- Terms: follow `GLOSSARY.md`; add new recurring terms there first.
  Decided: File = নথি (ফাইলের→নথির, ফাইলে→নথিতে; Profile stays প্রোফাইল), Settings = সেটিংস (not সরঞ্জাম),
  Revert = পরিবর্তন বাতিল করুন (never same as Undo), Quit/Exit = প্রস্থান.
- Write JSON with tab indent and unescaped Bengali (`ensure_ascii=False`).

### 3. Check

- `npm run package` must end with `DONE` (valid JSON only).
- It does NOT catch wrong keys or `&&` / `{0}` mismatches. Validate every entry: (module, key) exists in the
  VS Code mapping above (and ideally in the official French pack from microsoft/vscode-loc), placeholder set
  and `&&` count identical to English.

### 4. Test

`npm run try` → quit test window (Cmd+Q) → `npm run open`, then look at the string in the UI.
The first launch after an install shows English/stale menus (pack registered in `languagepacks.json`
only after startup); the second launch is correct. F5 / Extension Development Host cannot test language packs.

### 5. Commit

`feat(bn): translate <area>`. Single-line conventional commit, no body, no attribution lines.

## Pending idea (not built)

`scripts/` with `npm run find "<text>"` (lookup above), `npm run check` (key/placeholder/`&&` validation),
`npm run missing` (untranslated keys per module), so nothing depends on `/tmp`.
