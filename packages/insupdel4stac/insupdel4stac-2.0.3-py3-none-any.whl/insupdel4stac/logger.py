# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import logging
from logging.handlers import HTTPHandler, SMTPHandler, SocketHandler
from typing import Any, Union

from .analysers.properties_verifier import Verifier


class Logger:
    """
    A class-based logger for INSUPDEL4STAC. It supports
    all the handlers from the standard python logging
    library.

    Args:
        logger_properties (dict, optional): Logger properties. Defaults to `dict()`.
            It's optional and has the following keys:

                logger_msg (str, optional)

                logger_handler (str, optional)

                logger_name (str, optional)

                logger_id (str, optional)

                logger_level (str, optional)

                logger_formatter (str, optional)

                logger_handler_host (str, optional)

                logger_handler_port (str, optional)

                logger_handler_url (str, optional)

                logger_handler_method (str, optional)

                logger_handler_secure (bool, optional)

                logger_handler_credentials (tuple, optional)

                logger_handler_context (tuple, optional)

                logger_handler_filename (str, optional)

                logger_handler_mode (str, optional)

                logger_handler_encoding (str, optional)

                logger_handler_delay (bool, optional)

                logger_handler_errors (str, optional)

                logger_handler_mailhost (str, optional)

                logger_handler_fromaddr (str, optional)

                logger_handler_toaddrs (str, optional)

                logger_handler_subject (str, optional)

                logger_handler_timeout (str, optional)
    """

    logger_properties: Union[dict[str, Any], None]
    """
    A dictionary that contains all the logger properties.

        It is optional and it is set to `None` by default.
        The following keys are supported:
                **logger_msg (str, optional):**
                    Logger message. Defaults to `None`.
                    But it is required when you want to log a message.
                **logger_handler (str, optional):**
                    Logger handler. Defaults to `NullHandler`.
                    Check the following website for more information:

                    https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers
                **logger_name (str, optional):**
                    Logger name. Defaults to `INSUPDEL4STAC`. It's required
                    when you choose `HTTPHandler` as logger_handler.
                **logger_id (str, optional):**
                    Logger id. Defaults to `1`. It's required when you
                    choose `HTTPHandler` as logger_handler.
                **logger_level (str, optional):**
                    Logger level. Defaults to `DEBUG`. It's optional.
                    For more information check the following website:

                    https://docs.python.org/3/library/logging.html#levels
                **logger_formatter (str, optional):**
                    Logger format. Defaults to `%(levelname)-8s %(asctime)s \\t
                    %(filename)s @function %(funcName)s line %(lineno)s - %(message)s`.
                    For more information check the following website:

                    https://docs.python.org/3/library/logging.html#formatter-objects
                **logger_handler_host (str, optional):**
                    Logger host. Sets the value to 'None' by default.
                    It is required when `HTTPHandler` or `SocketHandler` are selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `HTTPHandler` or `SocketHandler` is
                    selected as the `logger_handler` value and neither `logger_handler_host` nor
                    `logger_handler_port` nor are specified.
                **logger_handler_port (str, optional):**
                    Logger port. Sets the value to 'None' by default.
                    It is required when `HTTPHandler` or `SocketHandler` are selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `HTTPHandler` or `SocketHandler` is
                    selected as the `logger_handler` value and neither `logger_handler_host` nor
                    `logger_handler_port` are specified.
                **logger_handler_url (str, optional):**
                    Logger url. Sets the value to 'None' by default.
                    It is required when `HTTPHandler` is selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `HTTPHandler` is
                    selected as the `logger_handler` value and neither `logger_handler_url`
                    is specified.
                **logger_handler_method (str, optional):**
                    HTTP methods. It supports sending logging messages
                    to a web server, using either GET or POST semantics. Sets the value to 'None' by default.
                    It is required when `HTTPHandler` is selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `HTTPHandler` is
                    selected as the `logger_handler` value and `logger_handler_method`
                    is not specified.
                **logger_handler_secure (bool, optional):**
                    HTTP secure. Sets the value to 'False' by default.
                    It is utilized when `HTTPHandler` or `SMTPHandler` are selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_credentials (tuple, optional):**
                    HTTP credentials. Sets the value to 'None' by default.
                    It is utilized when `HTTPHandler` or `SMTPHandler` are selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_context (tuple, optional):**
                    HTTP context. Sets the value to 'None' by default.
                    It is utilized when `HTTPHandler` is selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_filename (str, optional):**
                    File name. Sets the value to 'None' by default.
                    It is required when `FileHandler` or `WatchedFileHandler` are selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `FileHandler` or `WatchedFileHandler` is
                    selected as the `logger_handler` value and `logger_handler_filename` is not specified.
                **logger_handler_mode (str, optional):**
                    File mode. Sets the value to 'None' by default.
                    It is required when `FileHandler` or `WatchedFileHandler` are selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `FileHandler` or `WatchedFileHandler` is
                    selected as the `logger_handler` value and `logger_handler_mode` is not specified.
                **logger_handler_encoding (str, optional):**
                    File encoding. Sets the value to 'None' by default.
                    It is utilized when `FileHandler` or `WatchedFileHandler` are selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_delay (bool, optional):**
                    File delay. Sets the value to 'False' by default.
                    It is utilized when `FileHandler` or `WatchedFileHandler` are selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_errors (str, optional):**
                    File errors. Sets the value to 'None' by default.
                    It is utilized when `FileHandler` or `WatchedFileHandler` are selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_mailhost (str, optional):**
                    Mail host. Sets the value to 'None' by default.
                    It is required when `SMTPHandler` is selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `SMTPHandler` is
                    selected as the `logger_handler` value and `logger_handler_mailhost` is not specified.
                **logger_handler_fromaddr (str, optional):**
                    Mail from address. Sets the value to 'None' by default.
                    It is required when `SMTPHandler` is selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `SMTPHandler` is
                    selected as the `logger_handler` value and `logger_handler_fromaddr` is not specified.
                **logger_handler_toaddrs (str, optional):**
                    Mail to address. Sets the value to 'None' by default.
                    It is required when `SMTPHandler` is selected as the `logger_handler`.
                    The `logger_handler` will be set to 'NullHandler' if `SMTPHandler` is
                    selected as the `logger_handler` value and `logger_handler_toaddrs` is not specified.
                **logger_handler_subject (str, optional):**
                    Mail subject. Sets the value to 'None' by default.
                    It is utilized when `SMTPHandler` is selected as the `logger_handler`.
                    But it is optional in both logger handlers.
                **logger_handler_timeout (str, optional):**
                    Mail timeout. Sets the value to 'None' by default.
                    It is utilized when `SMTPHandler` is selected as the `logger_handler`.
                    But it is optional in both logger handlers.
    """

    def __init__(
        self,
        logger_properties: Union[dict[str, Any], None] = dict(),
    ):
        ##############################################
        # Setting the logger properties
        ##############################################

        verifier = Verifier()

        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            verifier.logger_properties(logger_properties)
            ###############################################
            # Choosing the logger name and ID if they are
            # not set when the HTTPHandler is selected as
            # the logger handler
            ###############################################
            if logger_properties.get("logger_name") is None:
                logger_properties["logger_name"] = "INSUPDEL4STAC"
            if logger_properties.get("logger_id") is None:
                logger_properties["logger_id"] = "1"
            ###############################################
            # Specifying the standard logger parameters for
            # all handlers
            ###############################################
            self.logger = logging.getLogger(
                str(logger_properties["logger_name"])
                + "_"
                + str(logger_properties["logger_id"])
            )
            if logger_properties.get("logger_level") is None:
                self.logger.setLevel(level=logging.DEBUG)
                logger_properties["logger_level"] = "DEBUG"
            elif logger_properties.get(
                "logger_level"
            ) is not None and logger_properties.get("logger_level") in [
                "NOTSET",
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ]:
                self.logger.setLevel(level=logger_properties["logger_level"])
            if logger_properties.get("logger_formatter") is None:
                logFormatter = logging.Formatter(
                    fmt="%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
                )
            elif logger_properties.get("logger_formatter") is not None:
                logFormatter = logging.Formatter(
                    fmt=logger_properties["logger_formatter"],
                )
            ###############################################
            # Verifying that the logger handler is supported
            # by the current version of INSUPDEL4STAC
            ###############################################
            if logger_properties.get(
                "logger_handler"
            ) is not None and logger_properties.get("logger_handler") not in [
                "NullHandler",
                "StreamHandler",
                "HTTPHandler",
                "FileHandler",
                "WatchedFileHandler",
                "SocketHandler",
                "SMTPHandler",
            ]:
                print(
                    "Warning: The current version of INSUPDEL4STAC is incompatible with your Logging Handler. It will be set automatically to `NullHandler`"
                )
                self.Null_Handler()
                return
            ###############################################
            # Self.legger is defining here depending on the
            # `logger_handler`
            ###############################################
            if (
                logger_properties.get("logger_handler") is None
                or logger_properties.get("logger_handler") == "NullHandler"
            ):
                self.Null_Handler()
            elif logger_properties.get("logger_handler") == "StreamHandler":
                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(logFormatter)
                streamHandler.setLevel(logging.DEBUG)
                if self.logger.handlers == [] or not any(
                    "StreamHandler"
                    in self.logger.handlers[i].__class__.__name__
                    for i in range(len(self.logger.handlers))
                ):
                    self.logger.addHandler(streamHandler)
            elif logger_properties.get("logger_handler") == "SocketHandler":
                if (
                    logger_properties.get("logger_handler_host") is None
                    or logger_properties.get("logger_handler_port") is None
                ):
                    print(
                        "Warning: You must specify `logger_handler_host` and `logger_handler_port` \
                        when selecting `SocketHandler` as the `logger_handler`. if not, `logger_handler` \
                        will transition to `NullHandler`"
                    )
                    self.Null_Handler()
                    return
                socketHandler = SocketHandler(  # type: ignore
                    host=str(logger_properties.get("logger_handler_host")),
                    port=(logger_properties.get("logger_handler_port")),
                )
                socketHandler.setFormatter(logFormatter)
                socketHandler.setLevel(logging.DEBUG)
                if self.logger.handlers == [] or not any(
                    "SocketHandler"
                    in self.logger.handlers[i].__class__.__name__
                    for i in range(len(self.logger.handlers))
                ):
                    self.logger.addHandler(socketHandler)
            elif logger_properties.get("logger_handler") == "HTTPHandler":
                if (
                    logger_properties.get("logger_handler_host") is None
                    or logger_properties.get("logger_handler_port") is None
                    or logger_properties.get("logger_handler_url") is None
                    or logger_properties.get("logger_handler_method") is None
                ):
                    print(
                        "Warning: You must specify `logger_handler_host`, `logger_handler_port`, \
                        `logger_handler_url`, `logger_handler_method` when selecting `HTTPHandler` \
                        as the `logger_handler`. if not, `logger_handler` will transition to `NullHandler`"
                    )
                    self.Null_Handler()
                    return
                httpHandler = HTTPHandler(  # type: ignore
                    host=str(logger_properties.get("logger_handler_host"))
                    + ":"
                    + str(logger_properties.get("logger_handler_port")),
                    url=str(logger_properties.get("logger_handler_url")),
                    method=str(logger_properties.get("logger_handler_method")),
                    secure=bool(
                        logger_properties.get("logger_handler_secure")
                    ),
                    credentials=logger_properties.get(
                        "logger_handler_credentials"
                    ),
                    context=logger_properties.get("logger_handler_context"),
                )
                httpHandler.setFormatter(logFormatter)
                httpHandler.setLevel(logging.DEBUG)
                if self.logger.handlers == [] or not any(
                    "HTTPHandler" in self.logger.handlers[i].__class__.__name__
                    for i in range(len(self.logger.handlers))
                ):
                    self.logger.addHandler(httpHandler)
            elif logger_properties.get("logger_handler") == "FileHandler":
                if (
                    logger_properties.get("logger_handler_filename") is None
                    or logger_properties.get("logger_handler_mode") is None
                ):
                    print(
                        "Warning: You must specify `logger_handler_filename` and `logger_handler_mode` \
                        when selecting `FileHandler` as the `logger_handler`. if not, `logger_handler`\
                          will transition to `NullHandler`"
                    )
                    self.Null_Handler()
                    return
                fileHandler = logging.FileHandler(
                    filename=str(
                        logger_properties.get("logger_handler_filename")
                    ),
                    mode=str(logger_properties.get("logger_handler_mode")),
                    encoding=logger_properties.get("logger_handler_encoding"),
                    delay=bool(logger_properties.get("logger_handler_delay")),
                    errors=logger_properties.get("logger_handler_errors"),
                )
                fileHandler.setFormatter(logFormatter)
                fileHandler.setLevel(logging.DEBUG)
                if self.logger.handlers == [] or not any(
                    "FileHandler" in self.logger.handlers[i].__class__.__name__
                    for i in range(len(self.logger.handlers))
                ):
                    self.logger.addHandler(fileHandler)
            elif logger_properties.get("logger_handler") == "SMTPHandler":
                if (
                    logger_properties.get("logger_handler_mailhost") is None
                    or logger_properties.get("logger_handler_fromaddr") is None
                    or logger_properties.get("logger_handler_toaddrs") is None
                    or logger_properties.get("logger_handler_subject") is None
                ):
                    print(
                        "Warning: You must specify `logger_handler_mailhost`, `logger_handler_fromaddr`, \
                        `logger_handler_toaddrs`, `logger_handler_subject` when selecting `SMTPHandler` \
                        as the `logger_handler`. if not, `logger_handler` will transition to `NullHandler`"
                    )
                    self.Null_Handler()
                    return
                smtpHandler = SMTPHandler(  # type: ignore
                    mailhost=str(
                        logger_properties.get("logger_handler_mailhost")
                    ),
                    fromaddr=str(
                        logger_properties.get("logger_handler_fromaddr")
                    ),
                    toaddrs=str(
                        logger_properties.get("logger_handler_toaddrs")
                    ),
                    subject=str(
                        logger_properties.get("logger_handler_subject")
                    ),
                    credentials=logger_properties.get(
                        "logger_handler_credentials"
                    ),
                    secure=logger_properties.get("logger_handler_secure"),
                    timeout=float(
                        str(logger_properties.get("logger_handler_timeout"))
                    ),
                )
                smtpHandler.setFormatter(logFormatter)
                smtpHandler.setLevel(logging.DEBUG)
                if self.logger.handlers == [] or not any(
                    "SMTPHandler" in self.logger.handlers[i].__class__.__name__
                    for i in range(len(self.logger.handlers))
                ):
                    self.logger.addHandler(smtpHandler)

            if logger_properties.get("logger_msg") is not None:
                if logger_properties.get("logger_level") is not None and (
                    logger_properties.get("logger_level") == "DEBUG"
                    or logger_properties.get("logger_level") == "NOTSET"
                ):
                    self.logger.debug(logger_properties.get("logger_msg"))
                elif (
                    logger_properties.get("logger_level") is not None
                    and logger_properties.get("logger_level") == "INFO"
                ):
                    self.logger.info(logger_properties.get("logger_msg"))
                elif (
                    logger_properties.get("logger_level") is not None
                    and logger_properties.get("logger_level") == "WARNING"
                ):
                    self.logger.warning(logger_properties.get("logger_msg"))
                elif (
                    logger_properties.get("logger_level") is not None
                    and logger_properties.get("logger_level") == "ERROR"
                ):
                    self.logger.error(logger_properties.get("logger_msg"))
                elif (
                    logger_properties.get("logger_level") is not None
                    and logger_properties.get("logger_level") == "CRITICAL"
                ):
                    self.logger.critical(logger_properties.get("logger_msg"))

    def Null_Handler(self):
        """
        This is a function to return a NullHandler
        """
        nullhandler = logging.NullHandler()
        self.logger.handlers = []
        self.logger.addHandler(nullhandler)
