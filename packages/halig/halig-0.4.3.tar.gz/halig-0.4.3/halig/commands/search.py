import hashlib
import re
import sqlite3
from pathlib import Path

from rich.console import Console

from halig.commands.base import BaseCommand
from halig.encryption import Encryptor
from halig.settings import Settings


class SearchCommand(BaseCommand):
    def __init__(self, term: str, index: bool, settings: Settings, *args, **kwargs):
        super().__init__(settings, *args, **kwargs)
        self.encryptor = Encryptor(settings)
        self.term = term
        self.index = index
        self.db_path = self.settings.cache_path / "halig.db"
        self.db_conn = sqlite3.connect(self.db_path)

    def _create_schema(self):
        with self.db_conn:
            self.db_conn.execute(
                """CREATE VIRTUAL TABLE IF NOT EXISTS notes
                USING fts5(name, last_timestamp, hash, filepath, body);""",
            )

    def _search_note_in_db_by_path(self, path: Path) -> tuple[str | None, str | None]:
        with self.db_conn:
            cursor = self.db_conn.execute(
                "SELECT hash, last_timestamp FROM notes where filepath = ?",
                (str(path),),
            )
            results = cursor.fetchall()
            if not results:
                return None, None
            return results[0]  # type: ignore[no-any-return]

    def _index_note(
        self,
        updated_at: float,
        body_hash: str,
        note_path: Path,
        body: str,
    ):
        with self.db_conn:
            self.db_conn.execute(
                """INSERT INTO notes (name, last_timestamp, hash, filepath, body)
                VALUES (?, ?, ?, ?, ?);""",
                (note_path.name, updated_at, body_hash, str(note_path), body),
            )

    def _update_index_note(
        self,
        updated_at: float,
        body_hash: str,
        note_path: Path,
        body: str,
    ):
        with self.db_conn:
            self.db_conn.execute(
                """UPDATE notes SET
                    last_timestamp = (?),
                    hash = (?),
                    body = (?)
                WHERE
                    filepath = (?);
                """,
                (updated_at, body_hash, body, str(note_path)),
            )

    def _index_notebooks(self):
        for note_path in self.traverse():
            updated_at = note_path.stat().st_mtime
            with note_path.open("rb") as f:
                body = self.encryptor.decrypt(f.read())
            body_hash = hashlib.sha512(body).hexdigest()
            original_hash, last_timestamp = self._search_note_in_db_by_path(note_path)
            if not original_hash:
                self._index_note(updated_at, body_hash, note_path, body.decode())
                continue

            if hash != original_hash:
                self._update_index_note(updated_at, body_hash, note_path, body.decode())

    def _search(self):
        with self.db_conn:
            cursor = self.db_conn.execute(
                "SELECT filepath, body FROM notes WHERE body MATCH ? ORDER BY rank;",
                (f"{self.term}*",),
            )
            results = cursor.fetchall()
        console = Console()
        search_regex = re.compile(re.escape(self.term), re.IGNORECASE)
        for result in results:
            filepath, body = result
            lines = body.split("\n")

            for lineno, line in enumerate(lines, start=1):
                match = search_regex.search(line)
                if match:
                    content_line = search_regex.sub("[bold red]\\g<0>[/bold red]", line)
                    console.print(f"{filepath}:{lineno}: {content_line}")

    def run(self):
        self._create_schema()
        if self.index:
            self._index_notebooks()
        self._search()
        self.db_conn.close()
