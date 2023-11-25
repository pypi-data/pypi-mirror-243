import logging

from rich.logging import RichHandler

from .api import HornAPI  # noqa: F401

__all__ = (
	'HornAPI',
)

logging.basicConfig(
	format='%(message)s',
	level=logging.INFO,
	handlers=(RichHandler(rich_tracebacks=True),),
)
