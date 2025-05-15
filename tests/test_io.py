import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from bson import decode_all

from cheatos import io
from cheatos.utils import get_cheato_path


@pytest.fixture
def temp_cheato_env(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("cheatos.utils.CHEATO_DIR", tmp_path)
        monkeypatch.setattr("cheatos.io.CHEATO_DIR", tmp_path)
        yield tmp_path


def create_sample_cheato(name, content, tags, tmp_path):
    path = get_cheato_path(name)
    data = {
        "title": name,
        "content": content,
        "tags": tags,
        "modified": "2024-01-01T00:00:00Z"
    }
    with open(path, "w") as f:
        json.dump(data, f)
    return path


def test_export_json(tmp_path, temp_cheato_env):
    create_sample_cheato("test1", "abc", ["x"], tmp_path)
    create_sample_cheato("test2", "def", ["y"], tmp_path)
    export_path = tmp_path / "export.json"
    io.export_cheatos(export_path)

    assert export_path.exists()
    with open(export_path) as f:
        exported = json.load(f)
    assert len(exported) == 2
    assert any(c["title"] == "test1" for c in exported)


def test_export_bson(tmp_path, temp_cheato_env):
    create_sample_cheato("bson1", "abc", ["x"], tmp_path)
    export_path = tmp_path / "export.bson"
    io.export_cheatos(export_path)
    assert export_path.exists()

    # ✅ Decode and validate the content
    with open(export_path, "rb") as f:
        decoded = decode_all(f.read())
    assert isinstance(decoded, list)
    assert "cheatos" in decoded[0]
    assert decoded[0]["cheatos"][0]["title"] == "bson1"


def test_import_json(tmp_path, temp_cheato_env):
    data = [
        {"title": "imp1", "content": "a", "tags": ["z"], "modified": "now"},
        {"title": "imp2", "content": "b", "tags": ["z"], "modified": "now"}
    ]
    file = tmp_path / "data.json"
    with open(file, "w") as f:
        json.dump(data, f)

    io.import_cheatos(file)
    assert get_cheato_path("imp1").exists()
    assert get_cheato_path("imp2").exists()


def test_import_overwrite(tmp_path, temp_cheato_env):
    create_sample_cheato("dup", "old", ["x"], tmp_path)

    data = [{"title": "dup", "content": "new", "tags": ["y"], "modified": "later"}]
    file = tmp_path / "overwrite.json"
    with open(file, "w") as f:
        json.dump(data, f)

    io.import_cheatos(file, force=False)
    with open(get_cheato_path("dup")) as f:
        assert json.load(f)["content"] == "old"

    io.import_cheatos(file, force=True)
    with open(get_cheato_path("dup")) as f:
        assert json.load(f)["content"] == "new"
