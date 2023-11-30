# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

from typing import Union

from ..logger import Logger


class TableDetails:
    """
    This class provides access to the table details. It is used to
    determine which tables are to be updated, inserted, or deleted.

    Args:
        table_details (list): List of dictionaries containing the table details.
            To learn more about constructing the dictionary, see
            :class:`~insupdel4stac.InsUpDel4STAC.table_details`.
    """

    def __init__(
        self,
        table_details: Union[list, None] = None,
        logger_properties: dict = dict(),
    ):
        self.logger_properties = logger_properties

        self.table_details = table_details
        self.table_details_temp: Union[list, None] = table_details
        self.all_collection_ids = None
        self.all_item_ids = None
        self.star_collection_ids = None
        self.other_collection_ids = None
        self.star_item_ids = None
        self.other_item_ids = None
        self.all_star_collection_ids: list = []
        self.all_star_item_ids: list = []
        self.all_equal_collection_ids: list = []
        self.all_equal_item_ids: list = []
        if self.table_details is not None:
            for table_detail in self.table_details:
                # if table_detail["table"] == "collection":
                # this condition is for making collection for all available collection-ids
                if (
                    table_detail.get("table") is not None
                    and table_detail.get("table") == "collection"
                ):
                    if (
                        table_detail.get("collection-id") is not None
                        and isinstance(table_detail.get("collection-id"), list)
                    ) or (
                        table_detail.get("collection-id") is not None
                        and isinstance(table_detail.get("collection-id"), str)
                    ):
                        (
                            self.star_collection_ids,
                            self.other_collection_ids,
                        ) = self.collection_table_details(table_detail)

                        if (
                            self.star_collection_ids is not None
                            and isinstance(self.star_collection_ids, list)
                        ):
                            self.all_star_collection_ids.extend(
                                self.star_collection_ids
                            )
                        if (
                            self.other_collection_ids is not None
                            and isinstance(self.other_collection_ids, list)
                        ):
                            self.all_equal_collection_ids.extend(
                                self.other_collection_ids
                            )

                    elif (
                        table_detail.get("collection-id") is None
                        and table_detail.get("item-id") is None
                    ):
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "When you choose the `table` as a `collection` or `item`, you have to define the `collection-id` or `item-id` respectively. In this process, `table_details` is not taken into consideration of this process because it is not defined."
                        Logger(self.logger_properties)
                        if (
                            self.table_details_temp is not None
                            and table_detail in self.table_details_temp
                        ):
                            self.table_details_temp.remove(table_detail)
                    elif not isinstance(
                        table_detail.get("collection-id"), list
                    ) or not isinstance(
                        table_detail.get("collection-id"), str
                    ):
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "When you choose the `table` as a `collection`, you should regard it as either a `list` or a `string`. In this process, `table_details` is not taken into consideration of this process because it is not part of a `list` or `str`"
                        Logger(self.logger_properties)
                        if (
                            self.table_details_temp is not None
                            and table_detail in self.table_details_temp
                        ):
                            self.table_details_temp.remove(table_detail)
                elif (
                    table_detail.get("table") is not None
                    and table_detail.get("table") == "item"
                ):
                    if (
                        table_detail.get("collection-id") is None
                        and table_detail.get("item-id") is None
                    ):
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "When you choose the `table` as a `collection` or `item`, you have to define the `collection-id` or `item-id` respectively. In this process, `table_details` is not taken into consideration of this process because it is not defined."
                        Logger(self.logger_properties)
                        if (
                            self.table_details_temp is not None
                            and table_detail in self.table_details_temp
                        ):
                            self.table_details_temp.remove(table_detail)
                    elif not isinstance(
                        table_detail.get("item-id"), list
                    ) and not isinstance(table_detail.get("item-id"), str):
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = "When you choose the `table` as a `collection`, you should regard it as either a `list` or a `string`. In this process, `table_details` is not taken into consideration of this process because it is not part of a `list` or `str`"
                        Logger(self.logger_properties)
                        if (
                            self.table_details_temp is not None
                            and table_detail in self.table_details_temp
                        ):
                            self.table_details_temp.remove(table_detail)
        self.table_details = self.table_details_temp
        # if table_detail["table"] == "item":
        #     if table_detail.get("item-id") is not None and isinstance(table_detail.get("item-id"), list):
        #         self.item_table_details(table_detail)
        #         if self.star_item_ids is not None:
        #             self.all_star_item_ids.extend(self.star_item_ids)
        #         if self.other_item_ids is not None:
        #             self.all_equal_item_ids.extend(self.other_item_ids)
        #     elif (table_detail.get("item-id") is None):
        #         self.logger_properties["logger_level"] = "WARNING"
        #         self.logger_properties["logger_msg"] = "When you choose the `table` as an `item`, you have to define the `item-id`. In this process, `table_details` is not taken into consideration of this process because it is not defined."
        #         Logger(self.logger_properties)
        #         table_detail = None
        #     elif (not isinstance(table_detail.get("item-id"), list)):
        #         self.logger_properties["logger_level"] = "WARNING"
        #         self.logger_properties["logger_msg"] = "When you choose the `table` as an `item`, you should regard it as a `list`. In this process, `table_details` is not taken into consideration of this process because it is not part of a `list`"
        #         Logger(self.logger_properties)
        #         table_detail = None
        # elif table_detail["table"] == "item":

        # if table_detail["table"] == "item":
        #     if table_detail.get("item-id") is not None and isinstance(table_detail.get("item-id"), list):
        #         self.item_table_details(table_detail)
        #         if self.star_item_ids is not None:
        #             self.all_star_item_ids.extend(self.star_item_ids)
        #         if self.other_item_ids is not None:
        #             self.all_equal_item_ids.extend(self.other_item_ids)

    def item_table_details(self, table_detail: dict):
        self.all_item_ids = table_detail["item-id"]
        if self.all_item_ids is not None and isinstance(
            table_detail["item-id"], list
        ):
            self.star_item_ids = [
                i.replace("*", "")
                for i in self.all_item_ids
                if i.endswith("*") or i.startswith("*")
            ]
            self.other_item_ids = [
                i for i in self.all_item_ids if i not in self.star_item_ids
            ]
        elif self.all_item_ids is not None and isinstance(
            table_detail["item-id"], str
        ):
            if self.all_item_ids.startswith("*") or self.all_item_ids.endswith(
                "*"
            ):
                self.star_item_ids = [self.all_item_ids.replace("*", "")]
            else:
                self.other_item_ids = [self.all_item_ids]
        return self.star_item_ids, self.other_item_ids

    def collection_table_details(self, table_detail: dict):
        self.all_collection_ids = table_detail["collection-id"]
        if self.all_collection_ids is not None and isinstance(
            table_detail["collection-id"], list
        ):
            self.star_collection_ids = [
                c.replace("*", "")
                for c in self.all_collection_ids
                if c.endswith("*") or c.startswith("*")
            ]
            self.other_collection_ids = [
                c
                for c in self.all_collection_ids
                if c not in self.star_collection_ids
            ]
        elif self.all_collection_ids is not None and isinstance(
            table_detail["collection-id"], str
        ):
            if self.all_collection_ids.startswith(
                "*"
            ) or self.all_collection_ids.endswith("*"):
                self.star_collection_ids = [
                    self.all_collection_ids.replace("*", "")
                ]
            else:
                self.other_collection_ids = [self.all_collection_ids]

        return self.star_collection_ids, self.other_collection_ids
