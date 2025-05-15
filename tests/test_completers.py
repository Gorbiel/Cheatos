import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from cheatos import completers


@pytest.fixture
def temp_cheatos(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("cheatos.utils.CHEATO_DIR", tmp_path)
        monkeypatch.setattr("cheatos.completers.CHEATO_DIR", tmp_path)

        # Create sample cheatos
        sample_data = [
            {"title": "alpha", "content": "A", "tags": ["sys"]},
            {"title": "beta", "content": "B", "tags": ["dev", "sys"]},
        ]
        for entry in sample_data:
            path = tmp_path / f"{entry['title']}.json"
            with open(path, "w") as f:
                json.dump(entry, f)

        yield tmp_path


def test_cheato_name_completer(temp_cheatos):
    result = completers.cheato_name_completer()
    assert sorted(result) == ["alpha", "beta"]


def test_tag_name_completer(temp_cheatos):
    result = completers.tag_name_completer()
    assert sorted(result) == ["dev", "sys"]
