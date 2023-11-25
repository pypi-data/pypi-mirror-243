from __future__ import annotations

from enum import auto as AutoEnum
from typing import TYPE_CHECKING

from .consts import MOD_NSMAP

if TYPE_CHECKING:
	from .type_annotations import Text

__all__ = (
	'ModTags',
	'ModAttrs',

	'AttrsNameEnum',
)

# TODO: Pydantic..
# TODO: DRY..


class AttrsNameEnum(type):
	def __new__(cls: type, name, bases, dct) -> type:
		# TODO: Annotations
		ins = type.__new__(cls, name, bases, dct)
		for key in ins.__annotations__:
			setattr(ins, key, key)

		return ins


# FIXME: Make it unmutable!
class ModAttrs(metaclass=AttrsNameEnum):  # TODO: ...
	name: str
	description: Text
	version: str
	link: str | None  # Alias url
	dependencies: list[str] | None
	repository: str  # Alias url
	issues: str | None
	tags: list[str] | None
	authors: list[str] | None


_fp = lambda s: f'{{%s}}{s}' % MOD_NSMAP  # noqa: E731


class ModTags(AutoEnum):
	name: str = _fp('Name')
	description: Text = _fp('Description')
	version: str = _fp('Version')
	link: str = _fp('Link')  # Alias url
	dependencies: str = _fp('Dependencies')
	repository: str = _fp('Repository')  # Alias url
	issues: str = _fp('Issues')
	tags: str = _fp('Tags')
	authors: str = _fp('Authors')
