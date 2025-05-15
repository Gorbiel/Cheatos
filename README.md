# Cheatos

> Inspired by the need to stop forgetting one-liners for tools like `tar`, `ffmpeg`, or `git rebase`.

**Cheatos** is a terminal post-it notes manager — lightweight CLI tool for storing cheat sheets called "cheatos", that you access, edit, and tag right from your shell.

---

## ✨ Features

- ✅ Create, edit, and delete short snippets of command-line knowledge
- 🏷️ Organize with tags
- 🖊️ Uses `$EDITOR` for clean editing flow
- 🔍 Fuzzy search (soon!)
- 📦 Export/import in JSON or BSON format
- 🧠 Shell autocompletion for subcommands, cheato names, and tags

---

## 🚀 Installation

```bash
pipx install cheatos
```

Make sure to have `pipx` and Python 3.7+ installed. `pipx` is preferred over `pip` for global installations to avoid dependency conflicts and not breaking your OS' Python installation.

---

## 🛠️ First Time Use

When you run Cheatos for the first time, it will prompt to enable shell autocompletion for Bash/Zsh automatically.

---

## 🧪 Usage

### Create a new cheato

```bash
cheatos add archive
```

Your `$EDITOR` opens. Write your note. Example:
```
To archive a directory:
tar czf archive.tar.gz folder/
```

You'll then be prompted to enter tags like:

```
archive, tar, linux
```

### Show a cheato

```bash
cheatos show archive
```

### List all cheatos (optionally by tag)

```bash
cheatos list
cheatos list --tag linux
```

### Edit content or tags

```bash
cheatos edit archive
cheatos edit archive --tags
```

### Delete a cheato

```bash
cheatos remove archive
```

### Rename a cheato

```bash
cheatos rename oldname newname
```

---

## 🔁 Export / Import

### Export all cheatos to a backup:

```bash
cheatos export backup.json
cheatos export backup.bson
```

### Import cheatos from backup:

```bash
cheatos import backup.json
cheatos import backup.bson
```

Use `--force` to overwrite existing ones.

---

## 🧩 Autocompletion

If you skip setup on first run, you can manually enable shell autocompletion:

```bash
eval "$(register-python-argcomplete cheatos)"
```

Add this to your `.bashrc` or `.zshrc`.

(I plan to add a command to re-prompt for autocompletion setup.)

---

## ✅ Coming Soon

- `cheatos search` with fuzzy matching
- `cheatos config` command to tweak behavior
- More export formats (e.g. Markdown)

---

## 📄 License

MIT © 2025 Gorbiel