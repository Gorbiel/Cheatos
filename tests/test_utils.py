import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from cheatos import utils
from datetime import datetime
from unittest import mock


@pytest.fixture
def temp_cheato_env(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("cheatos.utils.CHEATO_DIR", tmp_path)
        yield tmp_path


def test_get_cheato_path(temp_cheato_env):
    path = utils.get_cheato_path("demo")
    assert path.name == "demo.json"
    assert str(temp_cheato_env) in str(path)


def test_save_and_load_cheato(temp_cheato_env):
    name = "example"
    content = "some useful command"
    tags = ["cli"]
    utils.save_cheato(name, content, tags)

    loaded = utils.load_cheato(name)
    assert loaded["title"] == name
    assert loaded["content"] == content
    assert loaded["tags"] == tags
    # ISO timestamp ending in Z
    assert loaded["modified"].endswith("Z") is False  # now uses timezone-aware datetime
    assert "T" in loaded["modified"]


def test_load_nonexistent_cheato(temp_cheato_env):
    assert utils.load_cheato("notexist") is None


def test_open_editor_skip_first_line(monkeypatch):
    initial = "# Header"
    edited = "# Header\nactual content"
    with mock.patch("tempfile.NamedTemporaryFile") as mock_tmp:
        mock_file = mock.MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.name = "fake.tmp"
        mock_file.readlines.return_value = edited.splitlines(keepends=True)
        mock_tmp.return_value = mock_file
        monkeypatch.setattr("os.system", lambda _: 0)
        result = utils.open_editor(initial)
        assert result == "actual content"


def test_open_editor_preserve_all(monkeypatch):
    initial = "Start here"
    edited = "Not the same line"
    with mock.patch("tempfile.NamedTemporaryFile") as mock_tmp:
        mock_file = mock.MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.name = "fake.tmp"
        mock_file.readlines.return_value = [edited]
        mock_tmp.return_value = mock_file
        monkeypatch.setattr("os.system", lambda _: 0)
        result = utils.open_editor(initial)
        assert result == edited.strip()


def test_get_version_from_metadata(monkeypatch):
    monkeypatch.setattr("cheatos.utils.get_installed_version", lambda _: "2.0.0")
    assert utils.get_version() == "2.0.0"


def test_get_version_from_pyproject(tmp_path, monkeypatch):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("""
[project]
version = "3.1.4"
""")

    # Patch get_installed_version to fail
    monkeypatch.setattr("cheatos.utils.get_installed_version", lambda _: (_ for _ in ()).throw(Exception("fail")))

    # Patch Path(__file__).parent.parent / "pyproject.toml"
    def fake_path(*args, **kwargs):
        class FakePath(type(pyproject_path)):
            def __truediv__(self, key):
                return pyproject_path
        return FakePath(tmp_path)

    monkeypatch.setattr("cheatos.utils.Path", fake_path)

    assert utils.get_version() == "3.1.4"



def test_get_version_fallback(monkeypatch):
    monkeypatch.setattr("cheatos.utils.get_installed_version", lambda _: (_ for _ in ()).throw(Exception("fail")))
    monkeypatch.setattr("cheatos.utils.tomli.load", lambda _: (_ for _ in ()).throw(Exception("fail")))
    assert utils.get_version() == "unknown"
