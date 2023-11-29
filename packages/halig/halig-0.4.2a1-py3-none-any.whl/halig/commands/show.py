from pathlib import Path

from rich import print
from rich.console import Console
from rich.markdown import Markdown

from halig import utils
from halig.commands.base import BaseCommand
from halig.encryption import Encryptor
from halig.settings import Settings


class ShowCommand(BaseCommand):
    def __init__(self, note_path: Path, settings: Settings, plain: bool = False):
        super().__init__(settings)

        self.note_path = self.settings.notebooks_root_path / note_path
        self.encryptor = Encryptor(self.settings)
        self.plain = plain
        self.console = Console()
        if self.note_path.is_dir():
            self.note_path /= f"{utils.now().date()}.age"

        if not self.note_path.exists():
            err = f"File {self.note_path.name} does not exist"
            raise ValueError(err)

        if not self.note_path.name.endswith(".age"):
            err = f"File {self.note_path.name} is not a valid AGE file"
            raise ValueError(err)

    def decrypt(self) -> str:
        with self.note_path.open("rb") as f:
            data = f.read()
        return self.encryptor.decrypt(data).decode()

    def run(self):  # pragma: no cover
        contents = self.decrypt()
        if self.plain:
            print(contents)
            return
        md_contents = Markdown(contents)
        self.console.print(md_contents)
