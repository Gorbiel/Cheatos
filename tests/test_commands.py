import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from cheatos import commands
from cheatos.utils import get_cheato_path


@pytest.fixture
def temp_cheato_env(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        monkeypatch.setattr("cheatos.utils.CHEATO_DIR", tmp_path)
        monkeypatch.setattr("cheatos.commands.CHEATO_DIR", tmp_path)
        yield tmp_path


def test_add_show_remove_cheato(monkeypatch, temp_cheato_env):
    monkeypatch.setattr(commands, "open_editor", lambda _: "echo hello")
    monkeypatch.setattr("builtins.input", lambda _: "test")

    name = "example"
    commands.add_cheato(name)
    path = get_cheato_path(name)
    assert path.exists()

    from io import StringIO
    import sys
    captured = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    commands.show_cheato(name)
    sys.stdout = sys_stdout

    output = captured.getvalue()
    assert "echo hello" in output
    assert "test" in output

    commands.remove_cheato(name)
    assert not path.exists()


def test_edit_cheato(monkeypatch, temp_cheato_env):
    name = "editme"
    monkeypatch.setattr(commands, "open_editor", lambda _: "new content")
    monkeypatch.setattr("builtins.input", lambda _: "default")
    commands.add_cheato(name)

    commands.edit_cheato(name)
    data = json.loads(Path(get_cheato_path(name)).read_text())
    assert data["content"] == "new content"


def test_edit_tags(monkeypatch, temp_cheato_env):
    name = "tagme"
    monkeypatch.setattr(commands, "open_editor", lambda _: "tag content")
    monkeypatch.setattr("builtins.input", lambda _: "default")
    commands.add_cheato(name)

    monkeypatch.setattr("builtins.input", lambda _: "python, testing")
    commands.edit_tags(name)
    data = json.loads(Path(get_cheato_path(name)).read_text())
    assert set(data["tags"]) == {"python", "testing"}


def test_rename_cheato(monkeypatch, temp_cheato_env):
    monkeypatch.setattr(commands, "open_editor", lambda _: "hello world")
    monkeypatch.setattr("builtins.input", lambda _: "notes")
    commands.add_cheato("oldname")
    commands.rename_cheato("oldname", "newname")
    assert not get_cheato_path("oldname").exists()
    assert get_cheato_path("newname").exists()


def test_list_cheatos(monkeypatch, temp_cheato_env, capsys):
    monkeypatch.setattr(commands, "open_editor", lambda _: "cmd one")
    monkeypatch.setattr("builtins.input", lambda _: "cli")
    commands.add_cheato("listme")
    commands.list_cheatos()
    out = capsys.readouterr().out
    assert "listme" in out


def test_list_all_tags(monkeypatch, temp_cheato_env, capsys):
    monkeypatch.setattr(commands, "open_editor", lambda _: "tag test")
    monkeypatch.setattr("builtins.input", lambda _: "cli,helper")
    commands.add_cheato("taglist")
    commands.list_all_tags()
    out = capsys.readouterr().out
    assert "cli" in out
    assert "helper" in out


