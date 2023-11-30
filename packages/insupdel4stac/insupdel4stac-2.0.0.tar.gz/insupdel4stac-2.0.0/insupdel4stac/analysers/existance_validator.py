# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import os
from typing import Union


class ExistenceValidator(object):
    """
    A class for verifying the main STAC catalog's existence.
    This class is implemented in :class:`~insupdel4stac.InsUpDel4STAC`.

    Args:
        stac_dir (str): Directory of the main STAC catalog (*)
        default_catalog_name (str, optional): Name of the main STAC catalog. default is "catalog.json".
        logger_properties (dict, optional): A dictionary of properties for logger. default is `None`.

    """

    stac_dir: str
    """
    Directory of the main STAC catalog. It can be a relative or absolute path.
    """
    default_catalog_name: str
    """
    Name of the main STAC catalog. default is "catalog.json".
    """

    logger_properties: Union[dict, None]
    """
    A dictionary of properties for logger. default is `None`.
    You can look at keys in :class:`~insupdel4stac.logger.Logger` class.
    """

    def __init__(
        self,
        stac_dir: str = os.getcwd(),
        default_catalog_name: str = "catalog.json",
        collection_id: Union[str, None] = None,
    ):
        self.stac_dir = stac_dir
        self.default_catalog_name = default_catalog_name
        self.collection_id = collection_id
        self.catalog_existance_result = None
        self.collection_existance_result = None

    def catalog_existance(self):
        """
        This function verifies the existence of the main STAC catalog.
        """
        if os.path.exists(self.stac_dir + "/" + self.default_catalog_name):
            self.catalog_existance_result = True
        else:
            self.catalog_existance_result = False
        return self.catalog_existance_result
