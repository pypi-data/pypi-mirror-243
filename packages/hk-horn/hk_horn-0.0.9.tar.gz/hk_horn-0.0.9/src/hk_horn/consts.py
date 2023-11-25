from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from platformdirs import user_cache_dir, user_data_dir

if TYPE_CHECKING:
	from typing import Final

__all__ = (
	'ROOT_REPO',
	'SCHEMAS_DIRNAME',
	'API_FILENAME',
	'MOD_FILENAME',

	'ROOT_REPO_SOURCES_URL',

	'MOD_NSMAP',

	'PACKAGES_CACHE',
	'API_DATA',
	'ROOT_REPO_DIR',

	'SCHEMAS_DIR',
	'SCHEMA_API_LINKS',
	'SCHEMA_MOD_LINKS',
	'API_LINKS',
	'MOD_LINKS',
)


ROOT_REPO: Final[str] = 'modlinks'
SCHEMAS_DIRNAME: Final[str] = 'Schemas'

API_FILENAME: Final[str] = 'ApiLinks.xml'
MOD_FILENAME: Final[str] = 'ModLinks.xml'


# TODO: ...
# TODO: Rename..
ROOT_REPO_SOURCES_URL = 'https://github.com/hk-modding/modlinks/archive/refs/heads/master.zip'
# TODO: ...
MOD_NSMAP: Final[str] = 'https://github.com/HollowKnight-Modding/HollowKnight.ModLinks/HollowKnight.ModManager'


# TODO: ...
# TODO: Move app name to const..
# TODO: ...
PACKAGES_CACHE: Final[Path] = Path(user_cache_dir('horn'), 'pkg')
# FIXME: Lazy..
API_DATA: Final[Path] = Path(user_data_dir('horn'))  # DB-like
ROOT_REPO_DIR: Final[Path] = Path(API_DATA, ROOT_REPO)


# TODO: Refact(or)..
SCHEMAS_DIR: Final[Path] = Path(API_DATA, ROOT_REPO, SCHEMAS_DIRNAME)

SCHEMA_API_LINKS: Final[Path] = Path(API_DATA, SCHEMAS_DIR, API_FILENAME)
SCHEMA_MOD_LINKS: Final[Path] = Path(API_DATA, SCHEMAS_DIR, MOD_FILENAME)

API_LINKS: Final[Path] = Path(API_DATA, ROOT_REPO, API_FILENAME)
MOD_LINKS: Final[Path] = Path(API_DATA, ROOT_REPO, MOD_FILENAME)
