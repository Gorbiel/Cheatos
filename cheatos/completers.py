import json
from cheatos.utils import CHEATO_DIR


def cheato_name_completer(**kwargs):
    """
    Autocomplete function for cheato names.

    Returns a list of cheato file stems (without .json extension) in the data directory.
    """
    return [f.stem for f in CHEATO_DIR.glob("*.json")]


def tag_name_completer(**kwargs):
    """
    Autocomplete function for tag names.

    Scans all cheatos and returns a sorted list of unique tags.
    """
    tags = set()
    for path in CHEATO_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
            tags.update(data.get("tags", []))
    return sorted(tags)
