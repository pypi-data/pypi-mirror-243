<!--
SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie

SPDX-License-Identifier: CC-BY-4.0
-->

# INSUPDEL4STAC

[![CI](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac/badges/development/pipeline.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac/-/pipelines?page=1&scope=all&ref=development)
[![Code coverage](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac/badges/development/coverage.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac/-/graphs/development/charts)
<!-- TODO: uncomment the following line when the package is registered at https://readthedocs.org -->
[![Docs](https://readthedocs.org/projects/insupdel4stac/badge/?version=latest)](https://insupdel4stac.readthedocs.io/en/latest/)
[![Latest Release](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac/-/badges/release.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac)
<!-- TODO: uncomment the following line when the package is published at https://pypi.org -->
[![PyPI version](https://img.shields.io/pypi/v/insupdel4stac.svg)](https://pypi.python.org/pypi/insupdel4stac/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
<!-- TODO: uncomment the following line when the package is registered at https://api.reuse.software -->
[![REUSE status](https://api.reuse.software/badge/codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac)](https://api.reuse.software/info/codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac)


A Python package to provide seamless functionality for INSerting, UPDating, and DELeting STAC-Metadata toward either pgSTAC or STAC-API.

## Installation

Install this package in a dedicated python environment via

```bash
python -m venv venv
source venv/bin/activate
pip install insupdel4stac
```

To use this in a development setup, clone the [source code][source code] from
gitlab, start the development server and make your changes::

```bash
git clone https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac
cd insupdel4stac
python -m venv venv
source venv/bin/activate
make dev-install
```

More detailed installation instructions my be found in the [docs][docs].


[source code]: https://codebase.helmholtz.cloud/cat4kit/ds2stac/insupdel4stac
[docs]: https://insupdel4stac.readthedocs.io/en/latest/installation.html

## Technical note

This package has been generated from the template
https://codebase.helmholtz.cloud/hcdc/software-templates/python-package-template.git.

See the template repository for instructions on how to update the skeleton for
this package.


## License information

Copyright © 2023 Karlsruher Institut für Technologie



Code files in this repository are licensed under the
EUPL-1.2, if not stated otherwise
in the file.

Documentation files in this repository are licensed under CC-BY-4.0, if not stated otherwise in the file.

Supplementary and configuration files in this repository are licensed
under CC0-1.0, if not stated otherwise
in the file.

Please check the header of the individual files for more detailed
information.



### License management

License management is handled with [``reuse``](https://reuse.readthedocs.io/).
If you have any questions on this, please have a look into the
[contributing guide][contributing] or contact the maintainers of
`insupdel4stac`.

[contributing]: https://insupdel4stac.readthedocs.io/en/latest/contributing.html
