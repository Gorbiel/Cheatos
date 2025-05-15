import json
from pathlib import Path
from bson import encode as bson_encode, decode_all as bson_decode_all
from .utils import get_cheato_path, CHEATO_DIR




def check_first_time():
    """
    Display a welcome message and optionally set up shell autocompletion.

    This function is only triggered once, storing a marker file in the cheato directory.
    """
    import subprocess
    import os

    marker_file = CHEATO_DIR / ".initialized"
    if marker_file.exists():
        return

    print("\U0001F44B Welcome to Cheatos!")
    print("To enable shell auto-completion, you can set it up now.")
    choice = input("Would you like to enable it? [y/n]: ").strip().lower()

    if choice == "y":
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            rc_file = Path.home() / ".bashrc"
        elif "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            print("\u274C Unsupported shell for auto-setup.")
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
            print(f"\u2705 Completion added to {rc_file}. Restart your shell or run: source {rc_file}")
        except Exception as e:
            print(f"\u26A0\uFE0F Could not set up completion: {e}")
    else:
        print("\u2139\uFE0F You can manually enable it later with:")
        print('   eval "$(register-python-argcomplete cheatos)"')

    marker_file.touch()
    return


def export_cheatos(file_path):
    """
    Export all cheatos to a JSON or BSON file.

    The format is determined by the file extension (.json or .bson).
    """
    export_path = Path(file_path)
    cheatos = []
    for path in CHEATO_DIR.glob("*.json"):
        with open(path) as f:
            cheatos.append(json.load(f))

    if export_path.suffix == ".bson":
        with open(export_path, "wb") as f:
            f.write(bson_encode({"cheatos": cheatos}))
        print(f"✅ Exported {len(cheatos)} cheatos to {export_path} (BSON)")
    else:
        with open(export_path, "w") as f:
            json.dump(cheatos, f, indent=2)
        print(f"✅ Exported {len(cheatos)} cheatos to {export_path} (JSON)")


def import_cheatos(file_path, force=False):
    """
    Import cheatos from a JSON or BSON file.

    Skips existing cheatos unless --force is specified.
    """
    import_path = Path(file_path)
    if not import_path.exists():
        print(f"❌ File not found: {import_path}")
        return

    if import_path.suffix == ".bson":
        with open(import_path, "rb") as f:
            data = bson_decode_all(f.read())
        cheatos = data[0].get("cheatos", [])
    else:
        with open(import_path, "r") as f:
            cheatos = json.load(f)

    count = 0
    for cheato in cheatos:
        title = cheato["title"]
        path = get_cheato_path(title)
        if path.exists() and not force:
            print(f"⚠️ Skipping existing cheato '{title}'")
            continue
        with open(path, "w") as f:
            json.dump(cheato, f, indent=2)
        count += 1

    print(f"✅ Imported {count} cheatos.")
