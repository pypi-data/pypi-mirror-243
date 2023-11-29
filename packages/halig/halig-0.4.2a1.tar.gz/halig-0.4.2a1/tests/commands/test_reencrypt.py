import pytest

from halig.commands.reencrypt import ReencryptCommand


@pytest.fixture()
def reencrypt_command(settings):
    return ReencryptCommand(settings)


@pytest.mark.usefixtures("notes")
def test_reencrypt(reencrypt_command):
    reencrypt_command.run()
    for note_path in reencrypt_command.traverse():
        with note_path.open("rb") as f:
            assert reencrypt_command.encryptor.decrypt(f.read()) == b""
