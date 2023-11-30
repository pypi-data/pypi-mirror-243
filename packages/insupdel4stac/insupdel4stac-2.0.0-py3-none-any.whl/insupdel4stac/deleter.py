# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import os
import sys
from typing import Optional, Union

import pystac
import requests
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from requests.exceptions import RequestException

from .analysers.table_details import TableDetails
from .logger import Logger


class Deleter(object):
    """
    This is a class for deleting items and collections from pgSTAC and STAC-API.

    Args:
        collections_list (list): A list of collections to be deleted.
        service_type (str): The service type to be used for deleting. It can be `pgstac` or `stacapi`.
        table_details (list, optional): A list of dictionaries that contains the details of the tables. Defaults to None.
        loader (Loader, optional): The loader object to be used for deleting.
        pgstacdb (PgstacDB, optional): The PgstacDB object to be used for deleting.
        pgstac_properties (dict, optional): The properties of pgstac. Defaults to None.
        stacapi_properties (dict, optional): The properties of stacapi. Defaults to None.
        logger_properties (dict, optional): The properties of logger. Defaults to None.

    """

    def __init__(
        self,
        collections_list: list,
        service_type: str,
        table_details: Union[list, None] = None,
        loader: Optional[Loader] = None,
        pgstacdb: Optional[PgstacDB] = None,
        pgstac_properties: Optional[dict] = None,
        stacapi_properties: Optional[dict] = None,
        logger_properties: Optional[dict] = None,
    ):
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            self.logger_properties = logger_properties
        self.collections_list = collections_list
        if stacapi_properties is not None and isinstance(
            stacapi_properties, dict
        ):
            self.stacapi_properties = stacapi_properties
        if pgstac_properties is not None and isinstance(
            pgstac_properties, dict
        ):
            self.pgstac_properties = pgstac_properties
        if pgstacdb is not None and isinstance(pgstacdb, PgstacDB):
            self.PgstacDB = pgstacdb
        if loader is not None and isinstance(loader, Loader):
            self.loader = loader

        for collection in self.collections_list:
            self.delete(collection, service_type, loader, table_details)

    def delete(
        self,
        collection: pystac.Collection,
        service: str,
        loader: Optional[Loader] = None,
        table_details: Union[list, None] = None,
    ):
        """
        This function ingests the items and collections from pgSTAC
        and STAC-API according to the `service_type` and `table_details`.
        """

        collection_self_path: str = ""
        for link in collection.links:
            if link.rel == "self" and collection_self_path == "":
                collection_self_path = str(link.target)
        for link in collection.links:
            if link.rel == "item" or link.rel == "child":
                item_path = os.path.join(
                    os.path.dirname(collection_self_path), str(link.target)
                )
                item_id = os.path.splitext(os.path.basename(item_path))[0]
                item = collection.get_item(item_id)

                if table_details is not None:
                    for table_detail in table_details:
                        if (
                            table_detail.get("table") is not None
                            and table_detail.get("item-id") is not None
                            and table_detail["table"] == "item"
                            and (
                                isinstance(table_detail.get("item-id"), list)
                                or isinstance(table_detail.get("item-id"), str)
                            )
                        ):
                            if TableDetails().item_table_details(table_detail)[
                                0
                            ] is not None and any(
                                i in item_id
                                for i in TableDetails().item_table_details(
                                    table_detail
                                )[0]
                            ):  # star_item_ids
                                if (
                                    table_detail.get("collection-id")
                                    is not None
                                ):
                                    if TableDetails().collection_table_details(
                                        table_detail
                                    )[0] is not None and any(
                                        c in collection.id
                                        for c in TableDetails().collection_table_details(
                                            table_detail
                                        )[
                                            0
                                        ]
                                    ):  # star_collection_ids
                                        if (
                                            service == "pgstac"
                                            and loader is not None
                                        ):
                                            self.pgstac_item_delete(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_delete(
                                                item, collection
                                            )
                                        continue
                                    elif TableDetails().collection_table_details(
                                        table_detail
                                    )[
                                        1
                                    ] is not None and any(
                                        c == collection.id
                                        for c in TableDetails().collection_table_details(
                                            table_detail
                                        )[
                                            1
                                        ]
                                    ):  # other_collection_ids
                                        if (
                                            service == "pgstac"
                                            and loader is not None
                                        ):
                                            self.pgstac_item_delete(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_delete(
                                                item, collection
                                            )
                                        continue
                                    else:
                                        self.logger_properties[
                                            "logger_level"
                                        ] = "WARNING"
                                        self.logger_properties[
                                            "logger_msg"
                                        ] = "Please ensure that the collection-id is provided accurately."
                                        Logger(self.logger_properties)
                                # elif table_detail.get("collection-id") is not None and isinstance(table_detail.get("collection-id"), list):
                                #     self.logger_properties["logger_level"] = "WARNING"
                                #     self.logger_properties["logger_msg"] = "When the `table` is `item`, each item in a list has a unique collection-id, and it is not possible for several items to have more than one collection-id. The collectio-id should correspond to the existing list of items. Please revise the details provided in the `table_details`."
                                #     Logger(self.logger_properties)
                                elif table_detail.get("collection-id") is None:
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "WARNING"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "The collection ID has been left blank in table_details. In order to enhance the efficiency of the procedure, please furnish the collection-id."
                                    Logger(self.logger_properties)
                                    if (
                                        service == "pgstac"
                                        and loader is not None
                                    ):
                                        self.pgstac_item_delete(
                                            item_path, loader
                                        )
                                    elif (
                                        service == "stacapi"
                                        and item is not None
                                    ):
                                        self.stacapi_item_delete(
                                            item, collection
                                        )
                                    continue
                                else:
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "ERROR"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "Review your `table_details` and run the process again."
                                    Logger(self.logger_properties)
                                    continue
                            elif TableDetails().item_table_details(
                                table_detail
                            )[1] is not None and any(
                                i == item_id
                                for i in TableDetails().item_table_details(
                                    table_detail
                                )[1]
                            ):  # other_item_ids
                                if (
                                    table_detail.get("collection-id")
                                    is not None
                                ):
                                    if TableDetails().collection_table_details(
                                        table_detail
                                    )[0] is not None and any(
                                        c in collection.id
                                        for c in TableDetails().collection_table_details(
                                            table_detail
                                        )[
                                            0
                                        ]
                                    ):  # star_collection_ids
                                        if (
                                            service == "pgstac"
                                            and loader is not None
                                        ):
                                            self.pgstac_item_delete(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_delete(
                                                item, collection
                                            )
                                        continue
                                    elif TableDetails().collection_table_details(
                                        table_detail
                                    )[
                                        1
                                    ] is not None and any(
                                        c == collection.id
                                        for c in TableDetails().collection_table_details(
                                            table_detail
                                        )[
                                            1
                                        ]
                                    ):  # other_collection_ids
                                        if (
                                            service == "pgstac"
                                            and loader is not None
                                        ):
                                            self.pgstac_item_delete(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_delete(
                                                item, collection
                                            )
                                        continue
                                    else:
                                        self.logger_properties[
                                            "logger_level"
                                        ] = "WARNING"
                                        self.logger_properties[
                                            "logger_msg"
                                        ] = "Please ensure that the collection-id is provided accurately."
                                        Logger(self.logger_properties)
                                # elif table_detail.get("collection-id") is not None and isinstance(table_detail.get("collection-id"), list):
                                #     self.logger_properties["logger_level"] = "WARNING"
                                #     self.logger_properties["logger_msg"] = "When the `table` is `item`, each item in a list has a unique collection-id, and it is not possible for several items to have more than one collection-id. The collectio-id should correspond to the existing list of items. Please revise the details provided in the `table_details`."
                                #     Logger(self.logger_properties)
                                elif table_detail.get("collection-id") is None:
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "WARNING"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "The collection ID has been left blank in table_details. In order to enhance the efficiency of the procedure, please furnish the collection-id."
                                    Logger(self.logger_properties)
                                    if (
                                        service == "pgstac"
                                        and loader is not None
                                    ):
                                        self.pgstac_item_delete(
                                            item_path, loader
                                        )
                                    elif (
                                        service == "stacapi"
                                        and item is not None
                                    ):
                                        self.stacapi_item_delete(
                                            item, collection
                                        )
                                    continue
                                else:
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "ERROR"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "Review your `table_details` and run the process again."
                                    Logger(self.logger_properties)
                                    continue
                        elif (
                            table_detail.get("table") is not None
                            and table_detail.get("collection-id") is not None
                            and table_detail["table"] == "collection"
                            and not (
                                isinstance(
                                    table_detail.get("collection-id"), list
                                )
                                or isinstance(
                                    table_detail.get("collection-id"), str
                                )
                            )
                        ):
                            if TableDetails().collection_table_details(
                                table_detail
                            )[0] is not None and any(
                                c in collection.id
                                for c in TableDetails().collection_table_details(
                                    table_detail
                                )[
                                    0
                                ]
                            ):  # star_collection_ids
                                if service == "pgstac":
                                    self.pgstac_collection_delete(
                                        collection, self.PgstacDB
                                    )
                                elif service == "stacapi":
                                    self.stacapi_collection_delete(collection)
                                continue
                            elif TableDetails().collection_table_details(
                                table_detail
                            )[1] is not None and any(
                                c == collection.id
                                for c in TableDetails().collection_table_details(
                                    table_detail
                                )[
                                    1
                                ]
                            ):  # other_collection_ids
                                if service == "pgstac":
                                    self.pgstac_collection_delete(
                                        collection, self.PgstacDB
                                    )
                                elif service == "stacapi":
                                    self.stacapi_collection_delete(collection)
                                continue
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "The item in query does not belong to the current collection or the collection ID has been left blank in table_details. In order to enhance the efficiency of the procedure, please furnish the collection-id."
                                Logger(self.logger_properties)
                                continue
                        else:
                            self.logger_properties["logger_level"] = "ERROR"
                            self.logger_properties["logger_msg"] = (
                                "Please ensure that the `table` is `item` and the `item-id` is a `list` or `str` in the "
                                + str(table_detail)
                            )
                            Logger(self.logger_properties)
                            continue
                else:
                    if service == "pgstac" and loader is not None:
                        self.pgstac_item_delete(item_path, loader)
                    elif service == "stacapi" and item is not None:
                        self.stacapi_item_delete(item, collection)
        if table_details is None:
            print(
                "The collection " + str(collection.id) + " is being deleted."
            )
            if service == "pgstac":
                self.pgstac_collection_delete(collection, self.PgstacDB)
            elif service == "stacapi":
                self.stacapi_collection_delete(collection)

    def pgstac_collection_delete(
        self, collection: pystac.Collection, PgstacDB: PgstacDB
    ):
        """
        This function deletes the collection from pgSTAC.
        """
        try:
            gen_collections = PgstacDB.func(
                "delete_collection",
                collection.id,
            )
            [e for e in gen_collections]
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = "The removing of collection in pgSTAC database has been done successfully."
            Logger(self.logger_properties)
        except Exception:
            (
                ex_type,
                ex_value,
                ex_traceback,
            ) = sys.exc_info()
            import traceback

            print(traceback.format_exc())
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_msg"] = (
                    "The deletion of collection from pgSTAC database could not be done. %s : %s."
                    % (ex_type.__name__, ex_value)
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = "The deletion of collection from pgSTAC database could not be done."
            Logger(self.logger_properties)
            pass

    def stacapi_collection_delete(self, collection: pystac.Collection):
        """
        This function deletes the collection from STAC-API via DELETE method.
        """
        url = (
            self.stacapi_properties["stacapi_url"]
            + "/collections/"
            + str(collection.id)
        )
        headers = {"accept": "application/json"}
        try:
            req = requests.delete(
                url,
                headers=headers,
                timeout=self.stacapi_properties["timeout"],
                verify=self.stacapi_properties["verify"],
            )
            if req.status_code == 200:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The removing of collection in STAC-API database has been done successfully."
                Logger(self.logger_properties)
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties["logger_msg"] = (
                    "The removing of collection in STAC-API database could not be done. %s: %s"
                    % (req.status_code, req.reason)
                )
                Logger(self.logger_properties)
                pass
        except RequestException as e:
            # Handle any exceptions (e.g., timeout, connection error)
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties["logger_msg"] = (
                "The removing of collection in STAC-API database could not be done. %s"
                % e
            )
            Logger(self.logger_properties)
            pass

    def pgstac_item_delete(self, item_path: str, loader: Loader):
        """
        This function deletes the item from pgSTAC.
        """
        try:
            loader.load_items(
                str(item_path),
                Methods.delsert,
            )
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = "The removing of item in pgSTAC database has been done successfully."
            Logger(self.logger_properties)
        except Exception:
            (
                ex_type,
                ex_value,
                ex_traceback,
            ) = sys.exc_info()
            # import traceback

            # print(traceback.format_exc())
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_msg"] = (
                    "The deletion of item from pgSTAC database could not be done. %s : %s."
                    % (ex_type.__name__, ex_value)
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = "The deletion of item from pgSTAC database could not be done."
            Logger(self.logger_properties)

    def stacapi_item_delete(
        self, item: pystac.Item, collection: pystac.Collection
    ):
        """
        This function deletes the item from STAC-API via DELETE method.
        """
        url = (
            self.stacapi_properties["stacapi_url"]
            + "/collections/"
            + str(collection.id)
            + "/items/"
            + str(item.id)
        )
        headers = {"accept": "application/json"}
        try:
            req = requests.delete(
                url,
                headers=headers,
                timeout=self.stacapi_properties["timeout"],
                verify=self.stacapi_properties["verify"],
            )
            if req.status_code == 200:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The removing of item in STAC-API database has been done successfully."
                Logger(self.logger_properties)
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties["logger_msg"] = (
                    "The removing of item in STAC-API database could not be done. %s: %s"
                    % (req.status_code, req.reason)
                )
                Logger(self.logger_properties)
                pass
        except RequestException as e:
            # Handle any exceptions (e.g., timeout, connection error)
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties["logger_msg"] = (
                "The removing of item in STAC-API database could not be done. %s"
                % e
            )
            Logger(self.logger_properties)
            pass
