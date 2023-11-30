from functools import lru_cache
from pathlib import Path
from typing import Any

import hishel
import httpx
import platformdirs
import yaml
from pydantic import DirectoryPath, Field, FilePath, HttpUrl, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings model. It mainly stores paths that are interesting to the project.
     All the path-attributes described below have a validity check upon instantiation,
     meaning that they should exist and be readable and/or writable

    Attributes:
        notebooks_root_path (DirectoryPath): a *valid* path to a directory that
            may contain notes or other notebooks
        identity_paths (list[FilePath]): a list of *valid* paths of private keys.
            Defaults to `[~/.ssh/id_ed25519]`
        recipient_paths (list[FilePath|HttpUrl]): a list *valid* paths of public keys,
            which usually is understood as a public key. Defaults to
            `[~/.ssh/id_ed25519.pub]`
        cache_path (DirectoryPath): a *valid* path used to cache some stuff,
            particularly remote public keys. Defaults to $XDG_CACHE_HOME/halig
        remote_public_keys_timeout (float): time after which the retrieval of external public keys
            (e.g. github ssh keys) should be interrupted. Defaults to 0.5.
    """

    notebooks_root_path: DirectoryPath
    identity_paths: list[FilePath] = Field(
        default=[Path("~/.ssh/id_ed25519").expanduser()],
    )
    recipient_paths: list[FilePath | HttpUrl] = Field(
        default=[
            Path("~/.ssh/id_ed25519.pub").expanduser(),
        ],
    )
    cache_path: DirectoryPath = Field(
        default_factory=lambda: platformdirs.user_cache_path(
            "halig",
            ensure_exists=True,
        ),
    )
    remote_public_keys_timeout: float = 0.5

    @field_validator("identity_paths", "recipient_paths", mode="before")
    @classmethod
    def validate_paths(cls, v: Any):
        if not isinstance(v, list):
            v = [v]
        new_v = []
        for path in v:
            new_path = path
            if isinstance(path, str) and not path.startswith("http"):
                new_path = Path(path)
            new_v.append(
                new_path.expanduser() if isinstance(new_path, Path) else new_path,
            )
        return new_v

    @field_validator("notebooks_root_path", mode="before")
    @classmethod
    def validate_notebooks_path(cls, v: Any):
        if isinstance(v, str):
            return Path(v).expanduser()
        if isinstance(v, Path):
            return v.expanduser()
        return v

    def load_private_keys(self) -> set[str]:
        keys = set()
        for path in self.identity_paths:
            with path.open("r") as f:
                keys.add(f.read())
        return keys

    def load_public_keys(self) -> set[str]:
        keys = set()
        for path in self.recipient_paths:
            if isinstance(path, Url):
                with hishel.CacheClient(
                    storage=hishel.FileStorage(base_path=self.cache_path / "hishel"),
                ) as client:
                    response = client.get(
                        str(path),
                        timeout=self.remote_public_keys_timeout,
                    )
                if response.status_code == httpx.codes.OK:
                    for line in response.content.decode().split("\n"):
                        if line:
                            keys.add(line)
            elif isinstance(path, Path):
                with path.open("r") as f:
                    keys.add(f.read())
        return keys

    model_config = SettingsConfigDict(env_prefix="halig_")


@lru_cache
def load_from_file(file_path: Path | None = None) -> Settings:
    if file_path is None:
        halig_config_home = platformdirs.user_config_path("halig", ensure_exists=True)
        file_path = halig_config_home / "halig.yml"
        file_path.touch(exist_ok=True)
    elif not file_path.exists():
        err = f"File {file_path} does not exist"
        raise FileNotFoundError(err)

    with file_path.open("r") as f:
        data = yaml.safe_load(f)
    if not data:
        err = f"File {file_path} is empty"
        raise ValueError(err)
    return Settings(**data)
