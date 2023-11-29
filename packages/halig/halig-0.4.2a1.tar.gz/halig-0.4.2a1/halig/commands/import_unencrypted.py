from collections.abc import Generator
from pathlib import Path

from halig.commands.base import BaseCommand
from halig.encryption import Encryptor
from halig.settings import Settings


class ImportCommand(BaseCommand):
    def __init__(self, settings: Settings, unlink: bool = False):
        super().__init__(settings)
        self.encryptor = Encryptor(self.settings)
        self.unlink = unlink

    def get_importables(self) -> Generator[Path, None, None]:
        """Get all markdown files under self.settings.notebooks_root_path

        Yields:
            a list of Path objects matching any markdown files under
            the notebooks root path
        """
        return self.settings.notebooks_root_path.glob("**/*.md")

    def run(self):
        """For every importable file, encrypt its contents inside
        `filename.age`. If `self.unlink` is `True`, unlink the original
        file
        """

        for file_path in self.get_importables():
            with file_path.open("rb") as f:
                contents = f.read()

            encrypted_contents = self.encryptor.encrypt(contents)
            encrypted_file_path = file_path.with_suffix("").with_suffix(".age")
            encrypted_file_path.touch()
            with encrypted_file_path.open("wb") as f:
                f.write(encrypted_contents)

            if self.unlink:
                file_path.unlink()
