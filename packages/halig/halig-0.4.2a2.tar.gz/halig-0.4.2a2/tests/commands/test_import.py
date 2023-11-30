from pathlib import Path

import pytest

from halig.commands.import_unencrypted import ImportCommand
from halig.encryption import Encryptor


@pytest.fixture()
def command(settings) -> ImportCommand:
    return ImportCommand(settings)


def test_get_importables(unencrypted_notes: Path, command: ImportCommand):
    notes = list(command.get_importables())
    assert len(notes) == 15
    assert notes == list(unencrypted_notes.glob("**/*.md"))


def test_import(unencrypted_notes: Path, command: ImportCommand, encryptor: Encryptor):
    command.run()
    notes = command.get_importables()
    encrypted_notes = list(unencrypted_notes.glob("**/*.age"))
    assert len(encrypted_notes) == len(list(notes)) == 15
    for note in encrypted_notes:
        with note.open("rb") as f:
            encrypted_data = f.read()
        data = encryptor.decrypt(encrypted_data)
        if "inner" in str(note):
            assert (
                f'sub{note.name.replace(".age", "").replace("_"," ")}' == data.decode()
            )
        else:
            assert note.name.replace(".age", "").replace("_", " ") == data.decode()


def test_import_unlink(
    unencrypted_notes: Path,
    command: ImportCommand,
    encryptor: Encryptor,
):
    command.unlink = True
    command.run()
    notes = command.get_importables()
    encrypted_notes = list(unencrypted_notes.glob("**/*.age"))
    assert len(encrypted_notes) == 15
    assert len(list(unencrypted_notes.glob("**/*.md"))) == 0
