# Bengali (bn) VS Code Language Pack

## Adding translations

All strings live in `translations/main.i18n.json` as `contents[<module path>][<key>] = <Bengali text>`.
Wrong module paths or keys fail silently (string stays English), so never hand-type them.

### 1. Find module + key for an English string

`npm run find -- "New Folder"` (add `--missing` for untranslated hits only) does the lookup below.
`npm run missing` lists untranslated keys per module; `npm run missing -- <module-substring>` lists one module's strings.
The raw version, if the scripts are unavailable:

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
- `npm run check` validates every entry against the installed VS Code: (module, key) exists, placeholder set,
  `&&` and newline count identical to English; warns on untranslated text and ফাইল (glossary says নথি).
  Must report 0 errors. Ideally also compare keys with the official French pack from microsoft/vscode-loc.

### 4. Test

`npm run try` → quit test window (Cmd+Q) → `npm run open`, then look at the string in the UI.
The first launch after an install shows English/stale menus (pack registered in `languagepacks.json`
only after startup); the second launch is correct. F5 / Extension Development Host cannot test language packs.

### 5. Commit

`feat(bn): translate <area>`. Single-line conventional commit, no body, no attribution lines.
