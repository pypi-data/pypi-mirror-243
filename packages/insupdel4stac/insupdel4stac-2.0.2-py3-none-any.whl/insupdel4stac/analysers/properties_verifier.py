# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


class Verifier(object):  # type: ignore
    """
    A class is implemented to validate the logger_properties
    prior to use them in the primary source code.
    """

    def logger_properties(
        self,
        logger_properties: dict,
    ) -> dict:
        if logger_properties == {}:
            logger_properties["logger_handler"] = "NullHandler"
            logger_properties["logger_handler_timeout"] = 30
        return logger_properties
