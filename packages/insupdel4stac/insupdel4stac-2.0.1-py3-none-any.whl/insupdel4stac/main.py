# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import os
import sys
from typing import Union

import pystac
from pypgstac.db import PgstacDB
from pypgstac.load import Loader
from pystac import Collection

from .analysers.existance_validator import ExistenceValidator
from .analysers.properties_verifier import Verifier
from .analysers.table_details import TableDetails
from .connector import Connector
from .deleter import Deleter
from .inserter import Inserter
from .logger import Logger
from .updater import Updater


class InsUpDel4STAC:
    """
    The current class serves as the primary implementation for performing Insert,
    Update, and Delete actions on STAC-Catalogs. The class gets the STAC directory
    and the action type, for initiating the subsequent process.

    Args:
        stac_dir (str, optional): The directory where the STAC Catalog is located.
            The default value is set to `os.getcwd()`.
        action (string, optional): The type of action. The selection will be made from
            the options of `Insert`, `Update`, and `Delete`. The default setting is set
            to `Insert`.
        table_details (Union[list, None], optional): The permissible objects for input
            actions are a list of dictionaries, STAC-Collections, and STAC-Items. For
            further information about how to construct this argument, please refer
            to :class:`~insupdel4stac.InsUpDel4STAC.table_details`. The default value is set to None.
        default_catalog_name (str, optional): It represents the default name of the
            STAC-catalog. The default value is set to "catalog.json`.
        service_type (Union[str, None], optional): It represents the type of service.
            The selection will be made from the `pgstac` and `stacapi` components. For
            further information on this argument, please refer to
            :class:`~insupdel4stac.InsUpDel4STAC.service_type`. The default value is
            set to `pgstac`.
        stacapi_properties (dict, optional): The current dictionary provides definitions
            for STAC-API environments. To obtain additional information on the construction
            of `stacapi_properties`, please refer to :class:`~insupdel4stac.InsUpDel4STAC.stacapi_properties`.
            The default value is set to an empty dictionary, dict().
        pgstac_properties (dict, optional): The current dictionary provides definitions for
            pgSTAC environments. To obtain additional information on the construction of
            `pgstac_properties`, please refer to :class:`~insupdel4stac.InsUpDel4STAC.pgstac_properties`.
            The default value is set to an empty dictionary, dict().
        logger_properties (dict, optional): The current dictionary provides definitions for
            logger properties. To obtain additional information on the construction of
            `logger_properties`, please refer to :class:`~insupdel4stac.InsUpDel4STAC.logger_properties`.
            The default value is set to an empty dictionary, dict().
    """

    stac_dir: str
    """
    The variable at hand denotes the specific directory in which the STAC Catalog is
    presently situated.
    """
    action: str
    """
    The variable at present denotes the category of action. The decision will be taken
    from the alternatives of `Insert`, `Update`, and `Delete`.
    """
    table_details: Union[list, None]
    """
    The current variable represents the allowable entities for input actions as a list
    of dictionaries, STAC-Collections, and STAC-Items.
    The structure of the dictionary list can be exemplified as follows:

    .. code-block:: javascript
        [
            {
                "table": "collection",
                "collection-id": ["collection-id", "collection-i*"],
            },
            {
                "table": "collection",
                "collection-id": "collection-id",
            },
            {
                "table": "item",
                "collection-id": ["collection-id"],
                "item-id": ["item-id1", "item-id2", "item-i*"],
            },
            {
                "table": "item",
                "collection-id": "collection-id",
                "item-id": ["item-id1", "item-id2", "item-i*"],
            },
            {
                "table": "item",
                "item-id": ["item-i*"],
            },
            {
                "table": "item",
                "item-id": "item-i*",
            },
        ]

        **table (str)**:
            The table name can be one of the following options: `collection` or `item`.

        **collection-id (list, str)**:
            The collection identifier, denoted as `collection-id`, might consist of either a
            Optional(list, str) of collection ids or a partial representation of the collection ids,
            where the remaining portion is indicated by an asterisk (*). Similar to the aforementioned
            illustration.

        **item-id (list, str)**:
            The item identifier (item-id) can consist of either a Optional(list, str) of item identifiers or a truncated
            representation of the item identifiers, with the remaining portion being denoted by an asterisk (*).
            Similar to the aforementioned illustration. However, by selecting the appropriate collection-id while
            dealing with a `item` table, it is possible to enhance the action speed and improve the accuracy of
            the operation. Alternatively, the algorithm searches for the determined `item-id` within all existing
            collections, resulting in a longer than average processing time.
    """

    default_catalog_name: str
    """
    The variable now denotes the default JSON name for the STAC-catalog.
    """
    service_type: Union[str, None]
    """
    The variable now denotes the category of service. The pick will be made from the
    "pgstac" and "stacapi" components.

        **pgstac (str)**: The execution of this operation is carried out on the pgSTAC
            service using SQL-based commands by the pypgSTAC framework.

        **stacapi (str)**: The execution of this procedure is carried out within the STAC-API
            by utilizing POST, PUT, and DELETE requests to conduct the operations of inserting,
            updating, and deleting the STAC-Collections and STAC-Items, respectively. It is crucial
            to recognize that the implementation of the mentioned methods relies on the authorization
            and accessibility of the STAC-API services, together with the existence of authentication
            protocols to enable the execution of the designated tasks. To obtain additional details
            regarding the authentication procedure, please see the documentation for
            :class:`~insupdel4stac.InsUpDel4STAC.stacapi_properties`.
    """
    stacapi_properties: dict
    """
    The existing variable denotes the dictionary that furnishes definitions for STAC-API environments.
    The dictionary contains the following keys:

        **stacapi_url (str)**: The URL of the STAC-API service.

        **auth (dict, optional)**: The dictionary that contains the username and password
            for the STAC-API service. e.g. {"username": "username", "password": "password"}
        **timeout (int)**: The timeout value for the STAC-API service.

        **verify (bool)**: The boolean value that determines whether the verification is enabled.

    """
    pgstac_properties: dict
    """
    The existing variable denotes the dictionary that furnishes definitions for STAC-API environments.
    The dictionary contains the following keys:

        **POSTGRES_HOST_READER (str)**: The host name of the database server for reading.

        **POSTGRES_HOST_WRITER (str)**: The host name of the database server for writing.

        **POSTGRES_PORT (str)**: The port number of the database server.

        **POSTGRES_USER (str)**: The username for the database server.

        **POSTGRES_PASSWORD (str)**: The password for the database server.

        **POSTGRES_DB (str)**: The name of the database.

        **PGUSER (str)**: The username for the database server.

        **PGPASSWORD (str)**: The password for the database server.

        **PGHOST (str)**: The host name of the database server.

        **PGDATABASE (str)**: The name of the database.

        **PgstacDB_dsn (str)**: The data source name (DSN) for the database connection.

        **PgstacDB_pool (object)**: The connection pool for the database.

        **PgstacDB_connection (object)**: The connection object for the database.

        **PgstacDB_commit_on_exit (bool)**: The boolean value that determines whether the

        **PgstacDB_debug (bool)**: The boolean value that determines whether the debug mode is enabled.

        **PgstacDB_use_queue (bool)**: The boolean value that determines whether the queue is used.


    """
    logger_properties: dict
    """
    A dictionary of properties for logger. default is `None`.
    You can look at keys in :class:`~insupdel4stac.logger.Logger` class.

    """

    def __init__(
        self,
        stac_dir: str = os.getcwd(),
        action: str = "Insert",
        table_details: Union[list, None] = None,
        default_catalog_name: str = "catalog.json",
        service_type: Union[str, None] = "pgstac",
        stacapi_properties: dict = dict(),
        pgstac_properties: dict = dict(),
        logger_properties: dict = dict(),
    ):
        verifier = Verifier()
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            verifier.logger_properties(logger_properties)
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            self.logger_properties = logger_properties

        bollean_stac_dir = ExistenceValidator(
            stac_dir=stac_dir,
            default_catalog_name=default_catalog_name,
        ).catalog_existance()
        if bollean_stac_dir:
            self.stac_dir = stac_dir
        else:
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties["logger_msg"] = (
                "Due to the absence of specified directories for the STAC-Catalogs, the current directory was selected as the `stac_dir`. However, the procedure could not commence since no `"
                + default_catalog_name
                + "` were located in said directory. Please reassess the STAC directory and proceed with the program execution once more."
            )
            Logger(self.logger_properties)
            return
        ##############################################
        # Constant values
        ##############################################
        final_collections_list: list[Collection] = []
        star_collection_ids: list[str] = []
        other_collection_ids: list[str] = []
        self.loader: Union[Loader, None] = None
        self.pgstacdb: Union[PgstacDB, None] = None
        self.pgstac_properties = pgstac_properties
        self.stacapi_properties = stacapi_properties

        if table_details is not None and isinstance(table_details, list):
            # list of all collection ids that have * in their names and the other collection ids wihtout *
            star_collection_ids = TableDetails(
                table_details
            ).all_star_collection_ids
            other_collection_ids = TableDetails(
                table_details
            ).all_equal_collection_ids
            table_details = TableDetails(table_details).table_details
        elif table_details is not None and isinstance(table_details, dict):
            logger_properties["logger_level"] = "WARNING"
            logger_properties[
                "logger_msg"
            ] = "The `table_details` is not valid. It should be a list of dictionaries. For more information about the structure of the dictionary, please refer to the documentation."
            Logger(logger_properties)
            table_details = None

        if (
            service_type is not None
            and isinstance(service_type, str)
            and service_type.lower() in ["pgstac", "stacapi"]
        ):
            self.service_type = service_type
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The service type provided is invalid. The preferable options for the naming servies are either `pgstac` or `stacfastapi`. The default service type selected is `pgstac`."
            Logger(self.logger_properties)
            self.service_type = "pgstac"

        if (
            service_type == "pgstac"
            and pgstac_properties is not None
            and isinstance(pgstac_properties, dict)
        ):
            self.pgstac_properties = Connector(
                service=service_type, pgstac_properties=pgstac_properties
            ).pgstac_properties
            try:
                self.loader, self.pgstacdb = Connector(
                    service=service_type,
                    pgstac_properties=self.pgstac_properties,
                ).pgstac_connection()
            except Exception:
                (
                    ex_type,
                    ex_value,
                    ex_traceback,
                ) = sys.exc_info()
                self.logger_properties["logger_level"] = "WARNING"
                if ex_type is not None and ex_value is not None:
                    self.logger_properties["logger_msg"] = (
                        "The connection to the pgstac database could not be established. %s : %s. The default service type selected is `stacapi`."
                        % (ex_type.__name__, ex_value)
                    )
                else:
                    self.logger_properties[
                        "logger_msg"
                    ] = "The connection to the pgstac database could not be established. The default service type selected is `stacapi`."
                Logger(self.logger_properties)
                self.service_type = "stacapi"

        if (
            service_type == "stacapi"
            and stacapi_properties is not None
            and isinstance(stacapi_properties, dict)
        ):
            self.stacapi_properties = Connector(
                service=service_type, stacapi_properties=stacapi_properties
            ).stacapi_properties
            Connection_validator = Connector(
                service=service_type,
                stacapi_properties=self.stacapi_properties,
            ).stacapi_connection(self.stacapi_properties)
            if Connection_validator:
                self.service_type = "stacapi"
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties["logger_msg"] = (
                    "The connection to the STAC-API could not be established. Please check the STAC-API properties."
                    + str(Connection_validator)
                )
                Logger(self.logger_properties)
                pass

        catalog = pystac.Catalog.from_file(
            stac_dir + "/" + default_catalog_name
        )
        all_collection = catalog.get_collections()

        if table_details is not None and isinstance(table_details, list):
            table_details_collections = [
                i for i in table_details if i.get("table") == "collection"
            ]
            if table_details_collections != []:
                for collection in all_collection:
                    if any(c in collection.id for c in star_collection_ids):
                        final_collections_list.append(collection)
                    elif any(c == collection.id for c in other_collection_ids):
                        final_collections_list.append(collection)
            else:
                final_collections_list = list(all_collection)
        else:
            final_collections_list = list(all_collection)

        self.dispatchCollectionActions(
            action,
            final_collections_list,
            self.service_type,
            table_details,
            self.loader,
            self.pgstacdb,
            self.pgstac_properties,
            self.stacapi_properties,
            self.logger_properties,
        )

    def dispatchCollectionActions(
        self,
        action: str,
        collections_list: list,
        service_type: str,
        table_details: Union[list, None] = None,
        loader: Union[Loader, None] = None,
        pgstacdb: Union[PgstacDB, None] = None,
        pgstac_properties: dict = dict(),
        stacapi_properties: dict = dict(),
        logger_properties: dict = dict(),
    ):
        """
        The provided function serves as a dispatcher, responsible for
        directing actions to their respective classes: :class:`~insupdel4stac.deleter.Deleter`,
        :class:`~insupdel4stac.ingester.Ingester`, and :class:`~insupdel4stac.updater.Updater`.

        Args:
            action (str): The type of action. The selection will be made
                from `Insert`, `Update`, and `Delete`. The default setting is set to `Insert`.
            collections_list (list): The permissible pySTAC Collection objects
                for input actions.
            service_type (str): It represents the type of service.
            table_details (Union[list, None], optional): The permissible objects for input actions
            are a list of dictionaries, STAC-Collections, and STAC-Items. For further information
            about how to construct this argument, please refer to
            :class:`~insupdel4stac.InsUpDel4STAC.table_details`. The default value is
            set to None.
            loader (Union[object, None], optional): The `loader` object connector for pgSTAC. The
                default value is set to None.
            pgstacdb (Union[object, None], optional): The `pgstacdb` object connector for pgSTAC. The
                default value is set to None.
            pgstac_properties (dict, optional): An environment dictionary for `pgSTAC`. To obtain
                additional information on the construction of `pgstac_properties`, please refer
                to :class:`~insupdel4stac.InsUpDel4STAC.pgstac_properties`. The default value is
                set to an empty dictionary, dict().
            stacapi_properties (dict, optional): An environment dictionary for `STAC-API`.
                To obtain additional information on the construction of `stacapi_properties`,
                please refer to :class:`~insupdel4stac.InsUpDel4STAC.stacapi_properties`. The
                default value is set to an empty dictionary, dict().
            logger_properties (dict, optional): logger properties. :class:`~insupdel4stac.InsUpDel4STAC.logger_properties`.
        """
        if action == "Insert":
            Inserter(
                collections_list,
                service_type,
                table_details,
                loader,
                pgstacdb,
                pgstac_properties,
                stacapi_properties,
                logger_properties,
            )
        elif action == "Update":
            Updater(
                collections_list,
                service_type,
                table_details,
                loader,
                pgstacdb,
                pgstac_properties,
                stacapi_properties,
                logger_properties,
            )
        elif action == "Delete":
            Deleter(
                collections_list,
                service_type,
                table_details,
                loader,
                pgstacdb,
                pgstac_properties,
                stacapi_properties,
                logger_properties,
            )
        else:
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties[
                "logger_msg"
            ] = "The action is not valid. It should be `Insert`, `Update`, or `Delete`"
            Logger(self.logger_properties)
            pass
