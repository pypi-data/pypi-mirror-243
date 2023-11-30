# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import os

import requests
from pypgstac.db import PgstacDB
from pypgstac.load import Loader
from requests.exceptions import RequestException

from .statics import constants


class Connector:
    """
    This class provides access to the loader and PgstacDB. Conversely,
    it also affords the opportunity to configure the connection to
    the database and API. The setup can be achieved through the utilization
    of either environment variables and constant variables, or by utilizing
    :class:`~insupdel4stac.InsUpDel4STAC.pgstac_properties` or
    :class:`~insupdel4stac.InsUpDel4STAC.stacapi_properties`.

    Args:
        service (str, optional): Service to be configured. Defaults to "pgstac".
        pgstac_properties (dict, optional): Properties for pgstac. Defaults to dict().
        stacapi_properties (dict, optional): Properties for stacapi. Defaults to dict().

    """

    service: str
    """
    For more information see :class:`~insupdel4stac.InsUpDel4STAC.service_type`.
    """
    pgstac_properties: dict
    """
    To learn more about constructing the dictionary, see :class:`~insupdel4stac.InsUpDel4STAC.pgstac_properties`.
    """
    stacapi_properties: dict
    """
    To learn more about constructing the dictionary, see :class:`~insupdel4stac.InsUpDel4STAC.stacapi_properties`.
    """

    def __init__(
        self,
        service: str = "pgstac",
        pgstac_properties: dict = dict(),
        stacapi_properties: dict = dict(),
    ):
        if service == "pgstac":
            self.PgstacDB: PgstacDB = PgstacDB()
            self.loader: Loader = Loader(db=self.PgstacDB)
            self.pgstac_properties = self.properties_config(
                service, pgstac_properties
            )
        elif service == "stacapi":
            self.stacapi_properties = self.properties_config(
                service, stacapi_properties
            )

    def pgstac_connection(self):
        self.PgstacDB = PgstacDB(
            dsn="postgresql://"
            + self.pgstac_properties["POSTGRES_USER"]
            + ":"
            + self.pgstac_properties["POSTGRES_PASSWORD"]
            + "@"
            + self.pgstac_properties["PGHOST"]
            + ":"
            + self.pgstac_properties["POSTGRES_PORT"]
            + "/postgis",
            pool=self.pgstac_properties["PgstacDB_pool"],
            connection=self.pgstac_properties["PgstacDB_connection"],
            commit_on_exit=self.pgstac_properties["PgstacDB_commit_on_exit"],
            debug=self.pgstac_properties["PgstacDB_debug"],
        )
        self.loader = Loader(db=self.PgstacDB)
        return self.loader, self.PgstacDB

    def stacapi_connection(self, properties: dict = dict()):
        try:
            response = requests.head(
                properties["stacapi_url"],
                verify=properties["verify"],
                timeout=properties["timeout"],
            )
            # Check if the response status code is OK (200)
            if response.status_code == 200:
                return True
            else:
                return "The response status code is not OK (200). But it can possibly be OK (200) if you set the verify parameter to False."
        except RequestException as e:
            # Handle any exceptions (e.g., timeout, connection error)
            return f"Error occurred: {e}"

    def properties_config(
        self,
        service: str,
        properties: dict = dict(),
    ) -> dict:
        constant_configuration_dict: dict = dict()
        if service == "pgstac":
            constant_configuration_dict = constants.pgstac_configuration_dict
        elif service == "stacapi":
            constant_configuration_dict = constants.stacapi_configuration_dict

        if properties is None or properties == {}:
            for key, value in constant_configuration_dict.items():
                if os.getenv(key) is not None:
                    properties[key] = os.getenv(key)
                else:
                    properties[key] = value
        else:
            for key, value in constant_configuration_dict.items():
                if key not in properties.keys():
                    if os.getenv(key) is not None:
                        properties[key] = os.getenv(key)
                    else:
                        properties[key] = value
                else:
                    continue
        return properties
