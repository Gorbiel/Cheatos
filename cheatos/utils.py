from pathlib import Path
import os
import json
import tempfile
import tomli
from datetime import datetime, UTC
from appdirs import user_data_dir

try:
    from importlib.metadata import version as get_installed_version
except ImportError:
    from importlib_metadata import version as get_installed_version  # For Python <3.8

APP_NAME = "cheatos"
APP_AUTHOR = "gorbiel"
CHEATO_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


def get_version():
    """
    Import cheatos from a JSON or BSON file.

    Skips existing cheatos unless --force is specified.
    """
    try:
        return get_installed_version("cheatos")
    except Exception:
        try:
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                data = tomli.load(f)
            return data["project"]["version"]
        except Exception:
            return "unknown"


def ensure_cheato_dir():
    """
    Ensure the Cheatos data directory exists, creating it if needed.
    """
    CHEATO_DIR.mkdir(parents=True, exist_ok=True)


def get_cheato_path(name):
    """
    Return the full path to a cheato file given its name.
    """
    return CHEATO_DIR / f"{name}.json"


def load_cheato(name):
    """
    Load and return a cheato's JSON data as a dictionary.

    Returns None if the file does not exist.
    """
    path = get_cheato_path(name)
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def save_cheato(name, content, tags):
    """
    Save cheato content and metadata to a JSON file.
    """
    path = get_cheato_path(name)
    data = {
        "title": name,
        "content": content.strip(),
        "tags": tags,
        "modified": datetime.now(UTC).isoformat()
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def open_editor(initial_content=""):
    """
    Open the user's default editor to input or edit text.

    If the first line remains unchanged after editing, it is excluded from the result.
    Returns the resulting content as a stripped string.
    """
    editor = os.environ.get("EDITOR", "nano")
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True, mode="w+") as tf:
        tf.write(initial_content)
        tf.flush()
        os.system(f"{editor} {tf.name}")
        tf.seek(0)
        lines = tf.readlines()

    if lines and lines[0].strip() == initial_content.strip():
        lines = lines[1:]

    return "".join(lines).strip()
