import argparse
from pathlib import Path
from appdirs import user_data_dir

APP_NAME = "cheatos"
APP_AUTHOR = "gorbiel"
CHEATO_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

def ensure_cheato_dir():
    CHEATO_DIR.mkdir(parents=True, exist_ok=True)

def list_cheatos():
    cheatos = [f.stem for f in CHEATO_DIR.glob("*.txt")]
    print("Available cheatos:")
    for cheato in sorted(cheatos):
        print(f"  {cheato}")

def show_cheato(topic):
    file_path = CHEATO_DIR / f"{topic}.txt"
    if file_path.exists():
        print(file_path.read_text())
    else:
        print(f"No cheato found for '{topic}'")

def add_cheato(topic):
    file_path = CHEATO_DIR / f"{topic}.txt"
    if file_path.exists():
        print(f"Cheato '{topic}' already exists.")
        return
    print("Enter the cheato content (Ctrl+D to finish):")
    try:
        content = input()
        content += "\n" + "\n".join(iter(input, ""))
    except EOFError:
        pass
    with open(file_path, "w") as f:
        f.write(content + "\n")
    print(f"Cheato '{topic}' added.")

def remove_cheato(topic):
    file_path = CHEATO_DIR / f"{topic}.txt"
    if file_path.exists():
        file_path.unlink()
        print(f"Cheato '{topic}' removed.")
    else:
        print(f"No cheato found for '{topic}'")

def main():
    ensure_cheato_dir()
    parser = argparse.ArgumentParser(description="Cheatos: Your terminal post-it notes")
    parser.add_argument("topic", nargs="?", help="Cheato to display")
    parser.add_argument("--list", action="store_true", help="List all cheatos")
    parser.add_argument("--add", metavar="TOPIC", help="Add a new cheato")
    parser.add_argument("--remove", metavar="TOPIC", help="Remove a cheato")
    args = parser.parse_args()

    if args.list:
        list_cheatos()
    elif args.add:
        add_cheato(args.add)
    elif args.remove:
        remove_cheato(args.remove)
    elif args.topic:
        show_cheato(args.topic)
    else:
        parser.print_help()