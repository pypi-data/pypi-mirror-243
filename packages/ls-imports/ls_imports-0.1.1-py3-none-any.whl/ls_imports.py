import ast
import pathlib
import sys
from collections import defaultdict
from typing import Iterable

import click

__all__ = ["parse_file", "parse_source"]
__version__ = "0.1.1"


def parse_file(path: str | pathlib.Path):
    """Open a Python source file and return the modules it imports."""
    with open(path) as f:
        return parse_source(f.read(), path)


def parse_source(source: str, filename: str = "<unknown>"):
    """Parse a given Python source string and return a list of imported
    modules.

    Parameters
    ----------
    source : str
        Source to parse.
    filename : str, optional
        Filename associated with `source`. Only used in error messages.
        (default: "<unknown>")

    Raises
    ------
    SyntaxError
        If `source` is not valid Python source code.
    ValueError
        If `source` contains null bytes.
    """
    imports = set()
    tree = ast.parse(source, filename)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                imports.add("." * node.level)
            else:
                imports.add("." * node.level + node.module)
    return list(imports)


def filter_modules(modules: Iterable[str], ignore: Iterable[str]):
    """Filter a set of modules based on top-level imports."""
    return {module for module in modules if module.partition(".")[0] not in set(ignore)}


def _cli_parse_file(path: pathlib.Path, files: dict[str, list]):
    try:
        modules = parse_file(path)
    except Exception as exc:
        click.secho(
            f"Could not parse {click.format_filename(path)}: {exc}",
            fg="yellow",
            err=True,
        )
        return 1
    for module in modules:
        files[module].append(path)
    return 0


def _cli_parse_dir(path: pathlib.Path, files: dict[str, list]):
    num_errors = 0
    for p in pathlib.Path(path).rglob("*.py"):
        if p.is_file():
            num_errors += _cli_parse_file(p, files)
    return num_errors


@click.command()
@click.argument(
    "paths",
    type=click.Path(exists=True, path_type=pathlib.Path),
    nargs=-1,
    required=False,
)
@click.option(
    "--ignore",
    "-i",
    metavar="MODULE",
    multiple=True,
    help=(
        "Ignore a module and all its submodules."
        " This option may be given multiple times."
    ),
)
@click.option(
    "--ignore-relative/--no-ignore-relative",
    "-R/ ",
    help="Ignore relative imports.",
)
@click.option(
    "--ignore-stdlib/--no-ignore-stdlib",
    "-S/ ",
    help="Ignore standard library modules.",
)
@click.option(
    "--show-files/--no-show-files",
    "-f/ ",
    help="For each import, list the files that import it.",
)
@click.version_option(__version__, message="%(version)s")
def _cli(
    paths: list[pathlib.Path],
    ignore: list[str],
    ignore_relative: bool,
    ignore_stdlib: bool,
    show_files: bool,
):
    """Search Python source file(s) in PATHS for imported modules.

    Directories specified by PATHS are searched recursively for *.py files.
    """
    files = defaultdict(list)
    num_errors = 0
    for path in paths:
        if path.is_dir():
            num_errors += _cli_parse_dir(path, files)
        else:
            num_errors += _cli_parse_file(path, files)

    files = dict(files)
    imports = files.keys()

    ignore_modules = set(ignore)
    if ignore_stdlib:
        ignore_modules.update(sys.stdlib_module_names)
    if ignore_modules:
        imports = filter_modules(imports, ignore_modules)
    if ignore_relative:
        imports = {imp for imp in imports if not imp.startswith(".")}

    if imports:
        if show_files:
            for module in sorted(imports):
                lines = [
                    module,
                    *(
                        click.format_filename(filename)
                        for filename in sorted(files[module])
                    ),
                ]
                click.echo("\n\t".join(lines))
        else:
            click.echo("\n".join(sorted(imports)))

    if num_errors:
        raise click.ClickException(f"{num_errors} files could not be parsed.")


if __name__ == "__main__":
    _cli()
