import argparse
import os
import json
import tempfile
from pathlib import Path
from appdirs import user_data_dir
from datetime import datetime

APP_NAME = "cheatos"
APP_AUTHOR = "gorbiel"
CHEATO_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

def ensure_cheato_dir():
    CHEATO_DIR.mkdir(parents=True, exist_ok=True)

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


def show_cheato(name):
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"# {data['title']}")
    print(data["content"])
    if data.get("tags"):
        print(f"\nTags: {', '.join(data['tags'])}")

def main():
    ensure_cheato_dir()
    parser = argparse.ArgumentParser(description="Cheatos: Your terminal post-it notes")
    parser.add_argument("topic", nargs="?", help="Cheato to display")
    parser.add_argument("--list", action="store_true", help="List all cheatos")
    parser.add_argument("--add", metavar="TOPIC", help="Add a new cheato")
    parser.add_argument("--remove", metavar="TOPIC", help="Remove a cheato")
    parser.add_argument("--edit", metavar="TOPIC", help="Edit an existing cheato")
    parser.add_argument("--edit-tags", metavar="TOPIC", help="Edit tags for a cheato")
    parser.add_argument("--tag", metavar="TAG", help="Filter --list by tag")
    args = parser.parse_args()

    if args.list:
        list_cheatos(args.tag)
    elif args.add:
        add_cheato(args.add)
    elif args.remove:
        remove_cheato(args.remove)
    elif args.edit:
        edit_cheato(args.edit)
    elif args.edit_tags:
        edit_tags(args.edit_tags)
    elif args.topic:
        show_cheato(args.topic)
    else:
        parser.print_help()
