# Bengali Language Pack for VS Code

Translates the VS Code UI into Bengali (বাংলা). Untranslated strings fall back to English.

## Translation file format

`translations/main.i18n.json` maps VS Code source modules to string keys:

```json
{
	"version": "1.0.0",
	"contents": {
		"vs/workbench/contrib/files/browser/explorerViewlet": {
			"explore": "এক্সপ্লোরার"
		}
	}
}
```

Module paths and keys must match VS Code exactly. Get them from an official pack, e.g.
[vscode-language-pack-fr/translations/main.i18n.json](https://github.com/microsoft/vscode-loc/blob/main/i18n/vscode-language-pack-fr/translations/main.i18n.json).
Keep `&&` (menu mnemonic) and `{0}` placeholders as in the source.

Built-in extensions (git, markdown, ...) use separate files under `translations/extensions/<id>.i18n.json`,
each listed in `package.json` `contributes.localizations[0].translations`.

## Test locally

F5 (Extension Development Host) does not work for language packs: VS Code only lists installed packs
in `Configure Display Language`. Test with an installed `.vsix` in an isolated profile instead:

```sh
npm run try    # package, install into /tmp/vscode-bn, open VS Code in bn
npm run open   # open the test instance again (no install)
npm run clean  # remove /tmp/vscode-bn and the .vsix
```

After every `try`: quit the test window (Cmd+Q), then `npm run open`. VS Code registers a
CLI-installed pack in `languagepacks.json` only after startup, so the first launch after an
install shows English (or stale) menus; the second launch uses the new translations.

Your normal VS Code profile is not touched. Close the test window before re-running `try`,
otherwise the open window keeps the old translations.

## Package

```sh
npm run package
```

Install the `.vsix` into your main VS Code: Extensions view, `...` menu, `Install from VSIX...`.

## Maintenance

VS Code ships monthly. On each release bump `engines.vscode` and `version`, then translate new keys.
Terms: see `GLOSSARY.md` (repo only, not shipped in the package).
