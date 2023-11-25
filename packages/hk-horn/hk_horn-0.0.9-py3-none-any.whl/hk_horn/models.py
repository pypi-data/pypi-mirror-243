from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .typing import Text

__all__ = (
	'Mod',
)


# TODO: Auto optimize dataclass looking by Python's version..
# TODO: Pydantic..


@dataclass
class Mod:
	name: str
	description: Text
	version: str
	link: str | None  # Alias url
	dependencies: list[str] | None
	repository: str  # Alias url
	issues: str | None
	tags: list[str] | None
	authors: list[str] | None
