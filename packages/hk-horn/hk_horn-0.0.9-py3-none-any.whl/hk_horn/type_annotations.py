from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from pathlib import Path
	from typing import Literal, Union

	FilePath = Union[str, Path]

	ModField = str  # Literal some of Mod dataclass fields..

	Status = bool
	true = Literal[True]

	__all__ = (
		'FilePath',
		'ModField',
		'Status',
		'true',
	)
