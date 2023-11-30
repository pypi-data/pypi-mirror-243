import pyrage
from rich import print

from halig.commands.base import BaseCommand
from halig.encryption import Encryptor
from halig.settings import Settings


class ReencryptCommand(BaseCommand):
    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__(settings, *args, **kwargs)
        self.encryptor = Encryptor(settings)

    def run(self):
        for note_path in self.traverse():
            try:
                with note_path.open("rb") as fr:
                    orig_data = self.encryptor.decrypt(fr.read())
                new_data = self.encryptor.encrypt(orig_data)
                with note_path.open("wb") as fw:
                    fw.write(new_data)
            except pyrage.DecryptError:  # type: ignore[reportGeneralTypeIssues]
                print(
                    f"[yellow] Could not reencrypt {note_path} because no matching keys"
                    f" were found, skipping ...",
                )
