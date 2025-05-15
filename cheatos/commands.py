from .utils import get_cheato_path, load_cheato, save_cheato, open_editor, CHEATO_DIR
import json


def add_cheato(name):
    """
    Create a new cheato with the given name.

    Opens the user's editor to enter the content and prompts for tags.
    Saves the cheato as a JSON file in the Cheatos data directory.
    """
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
    """
    Edit the content of an existing cheato using the user's editor.

    Preserves existing tags and updates the content and timestamp.
    """
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"Editing cheato '{name}'...")
    content = open_editor(data["content"])
    save_cheato(name, content, data.get("tags", []))
    print(f"Cheato '{name}' updated.")


def edit_tags(name):
    """
    Edit the tags of an existing cheato.

    Prompts the user for a new list of tags and saves them to the file.
    """
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
    """
    Delete a cheato by name.

    Removes the corresponding JSON file from the data directory.
    """
    path = get_cheato_path(name)
    if path.exists():
        path.unlink()
        print(f"Cheato '{name}' removed.")
    else:
        print(f"No cheato found for '{name}'")


def list_cheatos(tag_filter=None):
    """
    List all available cheatos, optionally filtered by a tag.

    Displays the names of matching cheatos in sorted order.
    """
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
    """
    Print all unique tags used across all cheatos.
    """
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
    """
    Display the contents and metadata of a single cheato.
    """
    data = load_cheato(name)
    if not data:
        print(f"No cheato found for '{name}'")
        return
    print(f"{data['title']}")
    print(data["content"])
    if data.get("tags"):
        print(f"\nTags: {', '.join(data['tags'])}")


def rename_cheato(old_name, new_name):
    """
    Rename a cheato by changing its filename and internal title.

    Prevents overwriting existing cheatos.
    """
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
