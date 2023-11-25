from __future__ import annotations

import logging
import re
import zipfile
from abc import ABC, abstractmethod
from hashlib import md5
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import filetype  # Not the best, but well..
import requests
from lxml.etree import XMLSchema as etree_schema  # noqa: N813
from lxml.etree import parse as etree_parse

from .consts import (
	API_DATA,
	API_LINKS,
	MOD_LINKS,
	PACKAGES_CACHE,
	ROOT_REPO_DIR,
	ROOT_REPO_SOURCES_URL,
	SCHEMA_API_LINKS,
	SCHEMA_MOD_LINKS,
)
from .enums import ModAttrs, ModTags
from .models import Mod

if TYPE_CHECKING:
	from collections.abc import ItemsView, Iterable
	from re import Pattern
	from typing import Any

	from lxml.etree import Element, ElementTree, XMLSchema

	from .type_annotations import FilePath, ModField, Status, true

__all__ = (
	'logger',

	'HornyParserABC',
	'HornyParser',
	'HornAPI',
)

# TODO: LRU results..
# TODO: Multiversion & compatibility
# TODO: i18n

# TODO: More handle `Path.mkdir` with `parents=True` arg..

# TODO: More parsers support


logger = logging.getLogger(__name__)  ##


class DownloadError(Exception):
	...


class HornyParserABC(ABC):
	mod_repo_data_root: Element
	mod_repo_data_tree: Element

	api_data_root: Element
	api_data_tree: Element


	@staticmethod
	@abstractmethod
	def mod_element2obj(element: Element) -> Mod:
		raise NotImplementedError


class HornyParser(HornyParserABC):
	"""XML parser for mods repo.

	=)
	"""

	def __init__(
		self: HornyParser,
		schema_mod_links: FilePath = SCHEMA_MOD_LINKS,
		mod_links: FilePath = MOD_LINKS,

		schema_api_links: FilePath = SCHEMA_API_LINKS,
		api_links: FilePath = API_LINKS,

		*,
		autovalidate: bool = True,
	) -> None:
		# TODO: Property/unmutable this stuff..
		# TODO: ValidationError exception..
		# TODO: Dynamically construct dataclasses from schemes..

		# Mods data from repo
		self.schema_mod: XMLSchema = etree_schema(file=schema_mod_links)
		self.mod_repo_data_tree: ElementTree = etree_parse(mod_links)
		self.mod_repo_data_root: Element = self.mod_repo_data_tree.getroot()

		# Modding API
		self.schema_api: XMLSchema = etree_schema(file=schema_api_links)
		self.api_data: ElementTree = etree_parse(api_links)
		self.api_data_root: Element = self.api_data.getroot()

		if autovalidate:
			# TODO: raise Error..
			self._api_validate()
			self._mod_repo_validate()


	def _api_validate(self: HornyParser) -> bool:
		return self.schema_api.validate(self.api_data)


	def _mod_repo_validate(self: HornyParser) -> bool:
		return self.schema_api.validate(self.mod_repo_data_tree)


	@staticmethod
	def get_element_text(element: Element | None) -> str:
		text = getattr(element, 'text', None) or ''
		return text.strip()


	@staticmethod
	def get_elements_list(element: Element | None) -> list[str] | None:
		if element is None:
			return None
		return [e.text for e in element]


	@staticmethod
	def mod_element2obj(element: Element) -> Mod:
		# TODO: Handle errors..
		return Mod(
			name=HornyParser.get_element_text(element.find(ModTags.name)),
			description=HornyParser.get_element_text(element.find(ModTags.description)),
			version=HornyParser.get_element_text(element.find(ModTags.version)),
			link=HornyParser.get_element_text(element.find(ModTags.link)) or None,
			dependencies=HornyParser.get_elements_list(element.find(ModTags.dependencies)) or None,
			repository=HornyParser.get_element_text(element.find(ModTags.repository)),
			issues=HornyParser.get_element_text(element.find(ModTags.issues)) or None,
			tags=HornyParser.get_elements_list(element.find(getattr(ModTags, 'tags', ''))) or None,
			authors=HornyParser.get_elements_list(element.find(ModTags.authors)) or None,
		)


	def iter_mods(self: HornyParser) -> Iterable[Mod]:
		for mod in self.mod_repo_data_root:
			yield self.mod_element2obj(mod)


class HornAPI:
	def __init__(self: HornAPI, parser: type[HornyParser] = HornyParser, **kwargs: Any) -> None:
		self.parser: HornyParser = parser(**kwargs)


	# TODO: Count mods..


	@staticmethod
	def unpack_archive(
		*,
		filepath: str | Path,
		path: str | Path,
	) -> true:
		with zipfile.ZipFile(filepath, 'r') as zip_ref:
			zip_ref.extractall(path)

		return True


	@staticmethod
	def download_file(url: str, save_path: str | Path) -> true:
		# TODO: Async downloader!!!
		# TODO: Progressbar..
		# TODO: Retry & catch exceptions..
		# TODO: Overwrite optional..
		# FIXME: More test(s)..
		save_path = Path(save_path)
		with requests.get(url) as r, save_path.open('wb') as f:
			r.raise_for_status()  ##
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)

		return True


	@staticmethod
	def update_repo(*, overwrite: bool = False) -> true:
		# TODO: Mb make dirs startup..??
		API_DATA.mkdir(parents=True, exist_ok=True)
		# TODO: More checks..
		# TODO: Catch & warnings..
		# TODO: On repo data missing warning..|/- ....
		if not overwrite and ROOT_REPO_DIR.exists():
			return True

		repo_zipfile = Path(API_DATA, HornAPI.get_filename_from(url=ROOT_REPO_SOURCES_URL))
		# TODO: Do something with `self`-like in static..
		# TODO: Move to consts..?

		logger.info(
			'[cyan]Updating repo..',
			extra={'markup': True},
		)

		HornAPI.download_file(url=ROOT_REPO_SOURCES_URL, save_path=repo_zipfile)
		HornAPI.unpack_archive(filepath=repo_zipfile, path=API_DATA)

		# FIXME: Crutch~
		Path(API_DATA, 'modlinks-main').rename(ROOT_REPO_DIR)

		return True


	def _validate_fields(self: HornAPI, fields: dict[ModField, str]) -> None:
		for field in fields:
			if not field:
				msg = 'Field must have something!'
				raise ValueError(msg)

			if field not in Mod.__dataclass_fields__:
				msg = f'Incorrect field name `{field}`'
				raise ValueError(msg)


	def filter_mod_fields(
		self: HornAPI,
		mod: Mod, fsi: ItemsView[ModField, str | Pattern],
	) -> Mod | None:
		for field, ptrn in fsi:
			if not re.search(re.compile(ptrn), getattr(mod, field)):  # FIXME: ptrn types..
				return None

			logger.debug('[r"%s"] Regex result: `%s`', ptrn, getattr(mod, field))

		return mod


	# TODO: Use iterator..
	def find_mod_by(
		self: HornAPI,
		*,
		fields: ModField | tuple[ModField] | dict[ModField, str | Pattern],
		ptrn: str | Pattern | None = None,
		stop: int = -1,
	) -> list[Mod] | Mod | None:
		# TODO: raise errors..
		# FIXME: ptrn type..
		# TODO: Regex..
		# TODO: FuzzyWuzzy..

		# TODO: Do something with `stop=0`.. & mb `stop=False|None|all|not..' - lol..

		is_single_field = isinstance(fields, str)
		is_multi_field = isinstance(fields, dict)
		is_union_field = isinstance(fields, tuple)
		if is_multi_field:
			if ptrn:
				msg = 'Please use tuple with field names if you search union..'
				raise ValueError(msg)
		elif is_single_field:  # FIXME: Hints..
			fields = {
				fields: ptrn,
			}
		elif is_union_field:
			fields = {field: ptrn for field in fields}
		else:
			msg = f"Expected type `str | tuple[str] | dict[str, str]`, got '{type(fields)}'"
			raise ValueError(msg)

		fields_: dict[ModField, str] = fields
		self._validate_fields(fields_)

		# TODO: ...
		if ModAttrs.version in fields_:
			if fields_[ModAttrs.version] not in ('*',):
				fields_[ModAttrs.version] = f'^{fields_[ModAttrs.version]}$'
			else:
				del fields_[ModAttrs.version]

		# TODO: Make it rich..
		logger.info(
			'Searching field(s) ptrn(s) [yellow]`%s`[/]',
			str(fields_),
			extra={'markup': True},
		)

		result: list[Mod] = []
		cnt = 0
		# FIXME: Precompile..
		fsi: ItemsView[ModField, str | Pattern] = fields_.items()
		for mod in self.parser.iter_mods():
			if cnt == stop:
				break

			res: Mod | None = self.filter_mod_fields(mod=mod, fsi=fsi)
			if not res:
				continue

			cnt += 1
			result.append(res)

		if not result:
			return None

		ret: list[Mod] | Mod = result if len(result) > 1 else result[0]  # TODO: Make it optional..
		del result
		return ret


	@staticmethod
	def check_is_path_exists(path: str | Path) -> None:
		path = Path(path).expanduser()
		if not path.is_dir():
			msg = f"Directory '{path}' does not exist"
			raise OSError(msg)


	@staticmethod
	def get_filename_from(
		*,
		url: str,  # Alias url
	) -> str:
		# TODO: Manage priority..
		# Get filename from request headers
		response = requests.head(url, timeout=3)  # TODO: More manage this..
		filename = response.headers.get('Content-Disposition', '').split('filename=')[-1]
		del response

		# Get filename from url
		if not filename:
			filename = Path(urlparse(url).path).name
			# TODO: Add md5 hash between file suffix and prefix/name (undersuffix)..

		# At least make filename from url md5 hash..
		if not filename:
			filename = md5(url.encode()).hexdigest()  # noqa: S324
			# filetype.guess_extension

		return filename


	# TODO: Make it async!
	@staticmethod
	def download_package(
		*,
		url: str,  # Alias url
	) -> Path:

		# TODO: Install if package in cache..
		PACKAGES_CACHE.mkdir(parents=True, exist_ok=True)

		file_name = HornAPI.get_filename_from(url=url)

		# Download using grequests
		save_file_path = Path(PACKAGES_CACHE, file_name)
		if save_file_path.exists():
			logger.info(
				'File exists in cache [yellow]`%s`[/]',
				save_file_path,
				extra={'markup': True},
			)
			return save_file_path

		logger.info(
			'Downloading [yellow]`%s`[/] to path [yellow]`%s`[/]',
			url, save_file_path,
			extra={'markup': True},
		)
		HornAPI.download_file(url, save_file_path)

		return save_file_path


	# TODO: Make it async!
	@staticmethod
	def unpack_package(
		*,
		filepath: str | Path,
		path: str | Path,
	) -> Status:
		# TODO: More archive types.. & Type classes...
		path = Path(path).expanduser()

		HornAPI.check_is_path_exists(path)

		logger.info(
			'Unpacking `[blue]%s[/]` to path `[cyan]%s[/]`',  # TODO/FIXME: Fix colors..
			filepath, path,
			extra={'markup': True},
		)
		# Unpack using zip/tar & etc.
		return HornAPI.unpack_archive(filepath=filepath, path=path)


	def install(
		self: HornAPI, *,
		name: str, version: str = '*',
		path: str | Path,  # TODO: .. Replace os's `~`..
	) -> Status:
		path = Path(path).expanduser()
		# TODO: (Optional) Hide in logs home dir..
		# TODO: Change colors..
		if version not in ('*',):
			logger.info(
				"Searching package [violet]`'%s'==%s`[/]",
				name, version,
				extra={'markup': True},
			)
		else:
			logger.info(
				"Searching package [violet]'%s'[/]",
				name,
				extra={'markup': True},
			)
		mod: Mod = self.find_mod_by(  # type: ignore
			fields={ModAttrs.name: f'^{name}$', ModAttrs.version: version},
			stop=1,
		)

		# TODO: Update logic..
		if not mod:
			# FIXME: Duplications..
			if version not in ('*',):
				logger.info(
					"Package [violet]`'%s'==%s`[/] not found..", name, version,
					extra={'markup': True},
				)
			else:
				# TODO: Change color..
				logger.info(
					"Package [violet]'%s'[/] not found",
					name,
					extra={'markup': True},
				)
			return False

		if not mod.link:
			msg = "No download link & git download isn't implemented yet.."
			raise DownloadError(msg)

		logger.info(
			"[yellow]Installing package[/] [violet]`'%s'==%s`[/]",
			mod.name, mod.version,
			extra={'markup': True},  # FIXME: Duplication.. .. ..
		)
		pkg_filepath: Path = self.download_package(url=mod.link)
		install_path: Path = Path(path, mod.name)

		# TODO: Handle if installed.. (mb optional reinstall/skip or etc.)
		install_path.mkdir(parents=True)

		self.unpack_package(filepath=pkg_filepath, path=install_path)
		logger.info(
			"[green]Installation of package[/] [violet]`'%s'==%s`[/] [green]complete!",
			mod.name, mod.version,
			extra={'markup': True},
		)

		return True
