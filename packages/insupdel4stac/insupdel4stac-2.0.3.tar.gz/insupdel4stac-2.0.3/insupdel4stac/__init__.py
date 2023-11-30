# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

"""INSUPDEL4STAC

A python-based module to ingest STAC metadata catalogs into STAC-databases like pgSTAC
"""

from __future__ import annotations

from insupdel4stac.analysers.existance_validator import ExistenceValidator
from insupdel4stac.analysers.properties_verifier import Verifier
from insupdel4stac.analysers.table_details import TableDetails
from insupdel4stac.connector import Connector
from insupdel4stac.deleter import Deleter
from insupdel4stac.inserter import Inserter
from insupdel4stac.logger import Logger
from insupdel4stac.main import InsUpDel4STAC
from insupdel4stac.updater import Updater

from . import _version

__all__ = [
    "__version__",
    "InsUpDel4STAC",
    "Logger",
    "TableDetails",
    "ExistenceValidator",
    "Verifier",
    "Inserter",
    "Updater",
    "Deleter",
    "Connector",
]


__version__ = _version.get_versions()["version"]

__author__ = "Mostafa Hadizadeh"
__copyright__ = "2023 Karlsruher Institut für Technologie"
__credits__ = [
    "Mostafa Hadizadeh",
]
__license__ = "EUPL-1.2"

__maintainer__ = "Mostafa Hadizadeh"
__email__ = "mostafa.hadizadeh@kit.edu"

__status__ = "Pre-Alpha"

__version__ = _version.get_versions()["version"]

__version__ = _version.get_versions()["version"]

__version__ = _version.get_versions()["version"]

__version__ = _version.get_versions()["version"]
