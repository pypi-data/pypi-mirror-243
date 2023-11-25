from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from rich import print as rp

from hk_horn import HornAPI
from hk_horn.enums import ModAttrs
from hk_horn.models import Mod

if TYPE_CHECKING:
	from typing import Any, Iterable


CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}


def get_version_from_pyproject_toml(fp: str | Path = Path('pyproject.toml')) -> str:
	fp = Path(fp)
	if not fp.exists():
		return '-'

	with open(fp, 'r') as ppt:
		for line in ppt.readlines():
			if 'version = ' in line:
				sv = line.split()[-1]
				if '"' in sv:
					sv = sv[1:-1]
				return sv

	return '--'


horn: HornAPI = HornAPI  # type: ignore


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=get_version_from_pyproject_toml())
def cli():
	global horn
	# TODO: Handle update command(s) before init..
	horn.update_repo()
	horn = horn()

# TODO: List command (installed, repo & etc.)

# TODO: (Auto) Check & Update modlinks repo
# TODO: ...
# TODO: Mod/Package remove command..
# TODO: Mod/Package disable command..
# TODO: Command to manage & install HKMA..
# TODO: Command to set/download/manage repo list
# TODO: Configs..


def parse_opts(
	opts: dict[str, Any],
	*,
	name_equal: bool = True,
) -> None:
	_re_eq = lambda s: f'^{s}$'  # noqa: E731
	if ModAttrs.name in opts:
		# FIXME: Blah
		if 'case' in opts:
			if opts['case'] and opts.get(ModAttrs.name):
				opts[ModAttrs.name] = f'(?i){opts[ModAttrs.name]}'
			del opts['case']

		if opts[ModAttrs.name] and name_equal:  # TODO: More things..
			opts[ModAttrs.name] = _re_eq(opts[ModAttrs.name])

	# Clean no args:
	# TODO: Mb search click's option for it..
	for k, v in opts.copy().items():  # FIXME: ~Crutchy (mb use pycapi fork with PyDict_Next..)
		if not v:
			del opts[k]


# TODO: Union search value to avoid things like: `horn --name HK --description HK ...`
# TODO: Mb make print patterns in conf..
@cli.command()
@click.option('--name', help='Mod name')
@click.option('--display', default='description', help='Set tags search for..')  # TODO: More flexible..
@click.option('--case', is_flag=True, default=True, help="Don't ignore case on search")
@click.option('--version', default='*', help='Set version search for..')
@click.option('--description', help='Set description search for..')
@click.option('--link', help='Set link search for..')
@click.option('--repository', help='Set link search for..')
@click.option('--tags', help='Set tags search for..')  # TODO: ...
@click.option('--authors', help='Set tags search for..')  # TODO: ...
def find(**options: Any) -> None:
	# TODO: Flex versions search..
	parse_opts(options, name_equal=False)
	display_info = options.pop('display')
	if display_info in ('no', 'nothing', 'False', 'name', 'version'):  # version with name lol..
		display_info = None
	mods = horn.find_mod_by(fields=options)
	if not mods:  # FIXME: Duplicate..
		rp('No results found..')
		return

	if isinstance(mods, Mod):  # FIXME: Duplicate..
		mods: tuple[Mod] = (mods,)

	# TODO: Colors customization..

	# TODO: Blah..
	_rp_p = '{}'
	_rp_sq = "'{}'"
	if display_info:
		rich_print_mods(
			(_rp_sq, ModAttrs.name),
			(_rp_p, ModAttrs.version),
			(f'[white]-[/] [yellow]{_rp_p}[/]', display_info),

			mods=mods,
		)
	else:
		rich_print_mods(
			(_rp_sq, ModAttrs.name),
			(_rp_p, ModAttrs.version),

			mods=mods,
		)


def rich_print_mods(
	*args: tuple[str, str],  # Mod pattern <- key
	mods: Iterable[Mod],
) -> None:
	# TODO: Display length limit..
	for mod in mods:
		rp(*(fmt.format(getattr(mod, arg)) for fmt, arg in args))


@cli.command()
@click.argument('name')
@click.option('--version', default='*', help='Set version info about..')
def info(*, name: str, version: str) -> None:
	# TODO: Flex versions search..

	fields = {ModAttrs.name: name, ModAttrs.version: version}

	parse_opts(fields)

	mod = horn.find_mod_by(
		fields=fields,
		stop=1,  # TODO: raise/print/log Error or etc. handling here on more results..
	)
	if not mod:  # FIXME: Duplicate..
		rp('No results found..')
		return

	# if isinstance(mods, Mod):  # FIXME: Duplicate..
	# 	mods = (mods,)

	# TODO: Better format info..
	rp(mod)


# TODO: Game paths groups with config..
@cli.command()
@click.argument('names')
@click.option('--path', help='Path to install mod', required=True)
@click.option('--version', default='*', help='Set version install for..')
def install(*, names: str, version: str, path: str) -> None:
	# TODO: Install multiple packages.
	# TODO: Async & parallel installation XD
	# TODO: Flex versions search..

	for pkg in names.split(','):

		status = horn.install(
			name=pkg,
			version=version,
			path=Path(path),
		)
		if not status:
			rp('Status: ', '[red]Fail')
			return

		# if isinstance(mods, Mod):  # FIXME: Duplicate..
		# 	mods = (mods,)

		# TODO: Better format info..
		rp('Status: ', '[green]OK')


if __name__ == '__main__':
	cli()
