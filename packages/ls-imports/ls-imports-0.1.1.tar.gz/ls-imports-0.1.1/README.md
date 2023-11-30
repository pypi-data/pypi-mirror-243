## Installation & Usage

``` sh
$ pip install ls-imports
$ python -m ls_imports ...
```

Or use the CLI through [`pipx`](https://pypa.github.io/pipx/):

```
$ pipx run ls-imports --help
Usage: ls-imports [OPTIONS] [PATHS]...

  Search Python source file(s) in PATHS for imported modules.

  Directories specified by PATHS are searched recursively for *.py files.

Options:
  -i, --ignore MODULE             Ignore a module and all its submodules. This
                                  option may be given multiple times.
  -R, --ignore-relative / --no-ignore-relative
                                  Ignore relative imports.
  -S, --ignore-stdlib / --no-ignore-stdlib
                                  Ignore standard library modules.
  -f, --show-files / --no-show-files
                                  For each import, list the files that import
                                  it.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

## Examples

### Library

Setup:

``` pycon
>>> source = """
... import ast
... import click
... from .base import pkgfunc
... 
... def lazy_import():
...     import math
...     return math.sin(20.0)
... """
>>> with open('file.py', 'w') as f:
...     f.write(source)
```

Parse imports from a file:

``` pycon
>>> import ls_imports
>>> ls_imports.parse_file('file.py')
['math', 'ast', 'click', '.base']
```

Parse imports from a string:

``` pycon
>>> ls_imports.parse_source(source)
['math', 'ast', 'click', '.base']
```

### Command-line interface

Exclude standard library modules:

``` sh
$ python -m ls_imports --ignore-stdlib file.py
click
```

Exclude relative imports:

``` sh
$ python -m ls_imports --ignore-relative file.py
ast
click
math
```

Search a directory recursively:

``` sh
$ python -m ls_imports dir/
```

Search a large package for all third-party imports, and show which files
import them:

``` sh
$ git clone https://github.com/denavit/libdenavit-py
$ python -m ls_imports -RSf --ignore libdenavit libdenavit-py/src
matplotlib.pyplot
        libdenavit-py/src/libdenavit/OpenSees/get_fiber_data.py
        libdenavit-py/src/libdenavit/OpenSees/plotting.py
        libdenavit-py/src/libdenavit/OpenSees/uniaxial_material_analysis.py
        libdenavit-py/src/libdenavit/camber.py
        libdenavit-py/src/libdenavit/interaction_diagram_2d.py
        libdenavit-py/src/libdenavit/non_sway_column_2d.py
        libdenavit-py/src/libdenavit/section/RC.py
        libdenavit-py/src/libdenavit/section/circle_shape.py
        libdenavit-py/src/libdenavit/section/encased_composite.py
        libdenavit-py/src/libdenavit/section/fiber_section.py
        libdenavit-py/src/libdenavit/section/obround_shape.py
        libdenavit-py/src/libdenavit/section/rectangle_shape.py
        libdenavit-py/src/libdenavit/section/reinf.py
        libdenavit-py/src/libdenavit/sway_column_2d.py
numpy
        libdenavit-py/src/libdenavit/OpenSees/fiber_section.py
        libdenavit-py/src/libdenavit/camber.py
        libdenavit-py/src/libdenavit/cross_section_2d.py
        libdenavit-py/src/libdenavit/interaction_diagram_2d.py
        libdenavit-py/src/libdenavit/joist.py
        libdenavit-py/src/libdenavit/non_sway_column_2d.py
        libdenavit-py/src/libdenavit/section/ACI_phi.py
        libdenavit-py/src/libdenavit/section/ACI_strain_compatibility.py
        libdenavit-py/src/libdenavit/section/RC.py
        libdenavit-py/src/libdenavit/section/ccft.py
        libdenavit-py/src/libdenavit/section/circle_shape.py
        libdenavit-py/src/libdenavit/section/database/to_numpy.py
        libdenavit-py/src/libdenavit/section/encased_composite.py
        libdenavit-py/src/libdenavit/section/fiber_patches.py
        libdenavit-py/src/libdenavit/section/fiber_section.py
        libdenavit-py/src/libdenavit/section/obround_shape.py
        libdenavit-py/src/libdenavit/section/rectangle_shape.py
        libdenavit-py/src/libdenavit/section/reinf.py
        libdenavit-py/src/libdenavit/sway_column_2d.py
openseespy.opensees
        libdenavit-py/src/libdenavit/OpenSees/fiber_section.py
        libdenavit-py/src/libdenavit/OpenSees/get_fiber_data.py
        libdenavit-py/src/libdenavit/OpenSees/plotting.py
        libdenavit-py/src/libdenavit/OpenSees/uniaxial_material_analysis.py
        libdenavit-py/src/libdenavit/cross_section_2d.py
        libdenavit-py/src/libdenavit/non_sway_column_2d.py
        libdenavit-py/src/libdenavit/section/RC.py
        libdenavit-py/src/libdenavit/section/encased_composite.py
        libdenavit-py/src/libdenavit/sway_column_2d.py
pandas
        libdenavit-py/src/libdenavit/section/database/to_numpy.py
        libdenavit-py/src/libdenavit/section/fiber_section.py
pint
        libdenavit-py/src/libdenavit/unit_convert.py
scipy.optimize
        libdenavit-py/src/libdenavit/effective_length_factor.py
        libdenavit-py/src/libdenavit/non_sway_column_2d.py
        libdenavit-py/src/libdenavit/sway_column_2d.py
shapely.geometry
        libdenavit-py/src/libdenavit/interaction_diagram_2d.py
```

## Prior work

Based on [`list-imports`](https://github.com/andrewp-as-is/list-imports.py).

[`findimports`](https://github.com/mgedmin/findimports) is similar, but shows
the reverse relation (for each file, shows the modules/names it imports).
