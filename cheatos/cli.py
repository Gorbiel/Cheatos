import argparse
import argcomplete
import os
import json
import tempfile
import subprocess
# import shutil
from pathlib import Path
from appdirs import user_data_dir
from datetime import datetime

APP_NAME = "cheatos"
APP_AUTHOR = "gorbiel"
CHEATO_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


def ensure_cheato_dir():
    CHEATO_DIR.mkdir(parents=True, exist_ok=True)


def cheato_name_completer(**kwargs):
    return [f.stem for f in CHEATO_DIR.glob("*.json")]


def tag_name_completer(**kwargs):
    tags = set()
    for path in CHEATO_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
            tags.update(data.get("tags", []))
    return sorted(tags)


def check_first_time():
    marker_file = CHEATO_DIR / ".initialized"
    if marker_file.exists():
        return

    print("👋 Welcome to Cheatos!")
    print("To enable shell auto-completion, you can set it up now.")
    choice = input("Would you like to enable it? [y/N]: ").strip().lower()

    if choice == "y":
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            rc_file = Path.home() / ".bashrc"
        elif "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            print("❌ Unsupported shell for auto-setup.")
            marker_file.touch()
            return

        try:
            result = subprocess.run(
                ["register-python-argcomplete", "cheatos"],
                capture_output=True, text=True, check=True
            )
            completion_script = f"\n# Enable cheatos completion\n{result.stdout}\n"
            with open(rc_file, "a") as f:
                f.write(completion_script)
            print(f"✅ Completion added to {rc_file}. Restart your shell or run: source {rc_file}")
        except Exception as e:
            print(f"⚠️ Could not set up completion: {e}")
    else:
        print("ℹ️ You can manually enable it later with:")
        print('   eval "$(register-python-argcomplete cheatos)"')

    marker_file.touch()
    return


def get_cheato_path(name):
    return CHEATO_DIR / f"{name}.json"


def load_cheato(name):
    path = get_cheato_path(name)
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def save_cheato(name, content, tags):
    path = get_cheato_path(name)
    data = {
        "title": name,
        "content": content.strip(),
        "tags": tags,
        "modified": datetime.now().isoformat() + "Z"
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def open_editor(initial_content=""):
    editor = os.environ.get("EDITOR", "nano")
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False, mode="w+") as tf:
        tf.write(initial_content)
        tf.flush()
        os.system(f"{editor} {tf.name}")
        tf.seek(0)
        content = tf.read()
    os.unlink(tf.name)
    return content.strip()


def add_cheato(name):
    if get_cheato_path(name).exists():
        print(f"Cheato '{name}' already exists.")
        return
    print(f"Creating new cheato '{name}' using your editor...")
    content = open_editor("# Write your cheato content here")
    tags_input = input("Tags (comma separated): ")
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] or ["default"]
    save_cheato(name, content, tags)
    print(f"Cheato '{name}' added.")


def edit_cheato(name):
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"Editing cheato '{name}'...")
    content = open_editor(data["content"])
    save_cheato(name, content, data.get("tags", []))
    print(f"Cheato '{name}' updated.")


def edit_tags(name):
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"Current tags: {', '.join(data.get('tags', []))}")
    tags_input = input("New tags (comma separated): ")
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] or ["default"]
    save_cheato(name, data["content"], tags)
    print(f"Tags for '{name}' updated.")


def remove_cheato(name):
    path = get_cheato_path(name)
    if path.exists():
        path.unlink()
        print(f"Cheato '{name}' removed.")
    else:
        print(f"No cheato found for '{name}'")


def list_cheatos(tag_filter=None):
    cheatos = []
    for path in CHEATO_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
            tags = data.get("tags", [])
            if tag_filter is None or tag_filter in tags:
                cheatos.append(data["title"])
    if tag_filter:
        print(f"Cheatos with tag '{tag_filter}':")
    else:
        print("Available cheatos:")
    for name in sorted(cheatos):
        print(f"  {name}")


def list_all_tags():
    tags = set()
    for path in CHEATO_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
            tags.update(data.get("tags", []))
    if tags:
        print("Available tags:")
        for tag in sorted(tags):
            print(f"  {tag}")
    else:
        print("No tags found.")


def show_cheato(name):
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"# {data['title']}")
    print(data["content"])
    if data.get("tags"):
        print(f"\nTags: {', '.join(data['tags'])}")


def rename_cheato(old_name, new_name):
    old_path = get_cheato_path(old_name)
    new_path = get_cheato_path(new_name)

    if not old_path.exists():
        print(f"Cheato '{old_name}' does not exist.")
        return
    if new_path.exists():
        print(f"A cheato named '{new_name}' already exists.")
        return

    with open(old_path, "r") as f:
        data = json.load(f)
    data["title"] = new_name

    with open(new_path, "w") as f:
        json.dump(data, f, indent=2)

    old_path.unlink()
    print(f"Renamed cheato '{old_name}' to '{new_name}'.")


def main():
    ensure_cheato_dir()
    check_first_time()

    parser = argparse.ArgumentParser(description="Cheatos: Your terminal post-it notes manager")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="<command>",
        title="Available commands"
    )

    # cheatos list [--tag TAG] — list all cheatos or filter by tag
    list_parser = subparsers.add_parser("list", help="List all cheatos")
    tag_arg = list_parser.add_argument("--tag", help="Filter by tag")
    tag_arg.completer = tag_name_completer

    # cheatos show NAME — display a single cheato
    show_parser = subparsers.add_parser("show", help="Show a cheato")
    name_arg = show_parser.add_argument("name")
    name_arg.completer = cheato_name_completer

    # cheatos add NAME — create a new cheato using $EDITOR
    add_parser = subparsers.add_parser("add", help="Add a new cheato")
    add_parser.add_argument("name")

    # cheatos edit NAME [--tags] — edit content or tags of a cheato
    edit_parser = subparsers.add_parser("edit", help="Edit a cheato")
    edit_parser.add_argument("name")
    edit_parser.completer = cheato_name_completer
    edit_parser.add_argument("--tags", action="store_true", help="Edit tags of a cheato")

    # cheatos remove NAME — delete a cheato
    rm_parser = subparsers.add_parser("remove", help="Remove a cheato")
    rm_parser.add_argument("name")
    rm_parser.completer = cheato_name_completer

    # cheatos rename OLD_NAME NEW_NAME
    rename_parser = subparsers.add_parser("rename", help="Rename a cheato")
    old_arg = rename_parser.add_argument("old_name")
    old_arg.completer = cheato_name_completer
    rename_parser.add_argument("new_name")

    # cheatos tags — list all unique tags
    tags_parser = subparsers.add_parser("tags", help="List all unique tags")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.command == "list":
        list_cheatos(args.tag)
    elif args.command == "show":
        show_cheato(args.name)
    elif args.command == "add":
        add_cheato(args.name)
    elif args.command == "edit":
        if args.tags:
            edit_tags(args.name)
        else:
            edit_cheato(args.name)
    elif args.command == "remove":
        remove_cheato(args.name)
    elif args.command == "tags":
        list_all_tags()
    elif args.command == "rename":
        rename_cheato(args.old_name, args.new_name)
