from pathlib import Path

import pendulum
import pytest as pytest

from halig import utils
from halig.commands.notebooks import NotebooksCommand
from halig.settings import Settings


@pytest.fixture()
def notes(notebooks_path: Path):
    personal = notebooks_path / "Personal"
    work = notebooks_path / "Work"
    personal.mkdir()
    work.mkdir()

    personal_todos = personal / "todos.age"
    personal_todos.touch()

    work_todos = work / "todos.age"
    work_todos.touch()

    dailies = work / "Dailies"
    dailies.mkdir()

    dt = pendulum.now()
    for day_offset in range(10):
        dt = dt.subtract(days=day_offset)
        (dailies / f"{dt.date()}.age").touch()


@pytest.fixture()
def unencrypted_notes(notebooks_path):
    unencrypted_root_path = notebooks_path / "unencrypted"
    unencrypted_root_path.mkdir()
    for i in range(5):
        note = unencrypted_root_path / f"note_{i}.md"
        note.touch()
        subnote_path = unencrypted_root_path / f"inner_{i}"
        subnote_path.mkdir()
        for j in range(2):
            subnote = subnote_path / f"note_{i}_{j}.md"
            subnote.touch()
            with subnote.open("w") as f:
                f.write(f"subnote {i} {j}")
        with note.open("w") as f:
            f.write(f"note {i}")
    return unencrypted_root_path


@pytest.fixture()
def notebooks_command(settings: Settings):
    return NotebooksCommand(max_depth=float("inf"), settings=settings)


@pytest.fixture()
def current_note(notes, settings, encryptor) -> Path:
    note_path = settings.notebooks_root_path / f"{utils.now().date()}.age"
    note_path.touch()
    data = encryptor.encrypt(b"foo")
    with note_path.open("wb") as f:
        f.write(data)
    return note_path


@pytest.fixture()
def current_daily(notes, settings, encryptor) -> Path:
    note_path = (
        settings.notebooks_root_path / "Work" / "Dailies" / f"{utils.now().date()}.age"
    )
    data = encryptor.encrypt(b"foo")
    with note_path.open("wb") as f:
        f.write(data)
    return note_path


@pytest.fixture()
def mock_edit(mocker):
    def edit(callargs: list):
        with open(callargs[1], "wb") as f:
            f.write(b"edited")

    mocker.patch("halig.commands.edit.subprocess.call", side_effect=edit)
