# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

import json
import os
import sys
from typing import Optional, Union

import pystac
import requests
from pypgstac.load import Loader, Methods
from requests.exceptions import RequestException

from .analysers.table_details import TableDetails
from .logger import Logger


class Inserter(object):
    """
    This is a class for ingesting items and collections into pgSTAC and STAC-API.

    Args:
        collections_list (list): A list of collections to be ingested.
        service_type (str): The service type to be used for ingestion. It can be `pgstac` or `stacapi`.
        table_details (list, optional): A list of dictionaries that contains the details of the tables. Defaults to None.
        loader (Loader, optional): The loader object to be used for ingestion.
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
        if loader is not None and isinstance(loader, Loader):
            self.loader = loader

        for collection in self.collections_list:
            self.ingester(collection, service_type, loader, table_details)

    def ingester(
        self,
        collection: pystac.Collection,
        service: str,
        loader: Optional[Loader] = None,
        table_details: Union[list, None] = None,
    ):
        """
        This function ingests the items and collections into pgSTAC
        and STAC-API according to the `service_type` and `table_details`.
        """
        collection_self_path: str = ""

        for link in collection.links:
            if link.rel == "self" and collection_self_path == "":
                collection_self_path = str(link.target)
        if service == "pgstac" and loader is not None:
            self.pgstac_collection_ingest(collection_self_path, loader)
        elif service == "stacapi":
            self.stacapi_collection_ingest(collection)
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
                                            self.pgstac_item_ingest(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_ingest(item)
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
                                            self.pgstac_item_ingest(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_ingest(item)
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
                                        self.pgstac_item_ingest(
                                            item_path, loader
                                        )
                                    elif (
                                        service == "stacapi"
                                        and item is not None
                                    ):
                                        self.stacapi_item_ingest(item)
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
                                            self.pgstac_item_ingest(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_ingest(item)
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
                                            self.pgstac_item_ingest(
                                                item_path, loader
                                            )
                                        elif (
                                            service == "stacapi"
                                            and item is not None
                                        ):
                                            self.stacapi_item_ingest(item)
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
                                        self.pgstac_item_ingest(
                                            item_path, loader
                                        )
                                    elif (
                                        service == "stacapi"
                                        and item is not None
                                    ):
                                        self.stacapi_item_ingest(item)
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
                        self.pgstac_item_ingest(item_path, loader)
                    elif service == "stacapi" and item is not None:
                        self.stacapi_item_ingest(item)

    def pgstac_collection_ingest(
        self, collection_self_path: str, loader: Loader
    ):
        """
        This function ingests the collections into pgSTAC.
        """
        try:
            loader.load_collections(
                str(collection_self_path),
                Methods.insert,
            )
        except Exception:
            (
                ex_type,
                ex_value,
                ex_traceback,
            ) = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_msg"] = (
                    "The ingesting of collection into pgSTAC database could not be done. %s : %s."
                    % (ex_type.__name__, ex_value)
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = "The ingesting of collection into pgSTAC database could not be done."
            Logger(self.logger_properties)
            pass

    def stacapi_collection_ingest(self, collection: pystac.Collection):
        """
        This function ingests the collections into STAC-API via POST method.
        """
        url = self.stacapi_properties["stacapi_url"] + "/collections"
        collection_json = collection.to_dict()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            req = requests.post(
                url,
                headers=headers,
                data=json.dumps(collection_json),
                timeout=self.stacapi_properties["timeout"],
                verify=self.stacapi_properties["verify"],
            )
            if req.status_code == 200:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The ingesting of collection in STAC-API database has been done successfully."
                Logger(self.logger_properties)
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties["logger_msg"] = (
                    "The ingesting of collection in STAC-API database could not be done. %s: %s"
                    % (req.status_code, req.reason)
                )
                Logger(self.logger_properties)
                pass
        except RequestException as e:
            # Handle any exceptions (e.g., timeout, connection error)
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties["logger_msg"] = (
                "The ingesting of collection in STAC-API database could not be done. %s"
                % e
            )
            Logger(self.logger_properties)
            pass

    def pgstac_item_ingest(self, item_path: str, loader: Loader):
        """
        This function ingests the items into pgSTAC.
        """
        try:
            loader.load_items(
                str(item_path),
                Methods.insert,
            )
        except Exception:
            (
                ex_type,
                ex_value,
                ex_traceback,
            ) = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_msg"] = (
                    "The ingesting of item into pgSTAC database could not be done. %s : %s."
                    % (ex_type.__name__, ex_value)
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = "The ingesting of item into pgSTAC database could not be done."
            Logger(self.logger_properties)

    def stacapi_item_ingest(self, item: pystac.Item):
        """
        This function ingests the items into STAC-API via POST method.
        """
        url = (
            self.stacapi_properties["stacapi_url"]
            + "/collections/"
            + item.collection_id
            + "/items"
        )
        item_json = item.to_dict()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            req = requests.post(
                url,
                headers=headers,
                data=json.dumps(item_json),
                timeout=self.stacapi_properties["timeout"],
                verify=self.stacapi_properties["verify"],
            )
            if req.status_code == 200:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The ingesting of item in STAC-API database has been done successfully."
                Logger(self.logger_properties)
            else:
                self.logger_properties["logger_level"] = "ERROR"
                self.logger_properties["logger_msg"] = (
                    "The ingesting of item in STAC-API database could not be done. %s: %s"
                    % (req.status_code, req.reason)
                )
                Logger(self.logger_properties)
                pass
        except RequestException as e:
            # Handle any exceptions (e.g., timeout, connection error)
            self.logger_properties["logger_level"] = "ERROR"
            self.logger_properties["logger_msg"] = (
                "The ingesting of item in STAC-API database could not be done. %s"
                % e
            )
            Logger(self.logger_properties)
            pass
