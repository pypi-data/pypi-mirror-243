# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2
import os

from insupdel4stac import InsUpDel4STAC

os.environ["current_dir"] = os.getcwd()


def get_linux_distribution():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("NAME"):
                    # Typical content: NAME="Alpine Linux"
                    return line.strip().split("=")[1].strip('"')
    except IOError:
        pass

    return "Other"


if get_linux_distribution() != "Other":
    os.environ["stacapi_url"] = "http://docker:8082"
    os.environ["POSTGRES_HOST"] = "docker"
    os.environ["POSTGRES_USER"] = "username"
    os.environ["POSTGRES_PASS"] = "password"
    os.environ["POSTGRES_DBNAME"] = "postgis"
    os.environ["POSTGRES_HOST_READER"] = "docker"
    os.environ["POSTGRES_HOST_WRITER"] = "docker"
    os.environ["POSTGRES_PORT"] = "5439"
    os.environ["current_dir"] = os.getcwd()


def test_without_stac_dir():
    InsUpDel4STAC(
        service_type="pgstac",
        action="Insert",
        table_details=[
            {
                "table": "item",
            }
        ],
    )


def test_without_stac_dir_with_default_catalog_name():
    InsUpDel4STAC(
        default_catalog_name="catalogs.json",
        service_type="pgstac",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_insert_pgstac():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    # For geting the exeption
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_update_pgstac():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_delete_pgstac():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_insert_stacapi():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_delete_stacapi():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_update_stacapi():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_table_details_collection():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "collection",
                "collection-id": [
                    "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                ],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        table_details=[
            {
                "table": "collection",
                "collection-id": [
                    "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                ],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "collection",
                "collection-id": ["catalog_regclim_raster_global_era5_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        table_details=[
            {
                "table": "collection",
                "collection-id": ["catalog_regclim_raster_global_era5_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Insert",
        table_details=[
            {
                "table": "collection",
                "collection-id": ["catalog_regclim_raster_global_era5_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        table_details=[
            {
                "table": "collection",
                "collection-id": ["catalog_regclim_raster_global_era5_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        table_details=[
            {
                "table": "collection",
                "collection-id": [
                    "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                ],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        table_details=[
            {
                "table": "collection",
                "collection-id": {
                    "collection": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                },
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_table_details_item():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "item",
                "collection-id": [
                    "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                ],
                "item-id": "era5_sfc_0_25_single_daily_era5_daily_sp*",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "item",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1979"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1979"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_*",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_*",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "collection-id": "else",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        table_details=[
            {
                "table": "item",
                "item-id": ["era5_sfc_0_25_single_daily_era5_dail*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "item-id": "era5_sfc_0_25_single_daily_era5_daily_sp_1979",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": "era5_sfc_0_25_single_daily_era5_*",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "item-id": "era5_sfc_0_25_single_daily_era5_daily_sp_1979",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        table_details=[
            {
                "table": "item",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir="/Users/hadizadeh-m/stac/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "item-id": "era5_sfc_0_25_single_daily_era5_daily_sp_*",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "collection",
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "collection",
                "collection-id": {
                    "collection": "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
                },
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )

    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_*",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_*"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "catalog_regclim_raster_global_era5_sfc_single_daily_*",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        table_details=[
            {
                "table": "item",
                "collection-id": "else",
                "item-id": ["era5_sfc_0_25_single_daily_era5_daily_sp_1980"],
            }
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_logs():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "NullHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "WrongHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={
            "logger_handler": "NullHandler",
            "logger_level": "DEBUG",
            "logger_formatter": "%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "FileHandler",
            "logger_handler_filename": "test.log",
            "logger_handler_mode": "w",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "FileHandler",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "SMTPHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "SMTPHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "SMTPHandler",
            "logger_handler_mailhost": "localhost",
            "logger_handler_fromaddr": "",
            "logger_handler_toaddrs": "",
            "logger_handler_subject": "",
            "logger_handler_timeout": "30",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "HTTPHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "HTTPHandler",
            "logger_handler_host": "localhost",
            "logger_handler_port": 9999,
            "logger_handler_url": "/test",
            "logger_handler_method": "Post",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "SocketHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "SocketHandler",
            "logger_handler_host": "localhost",
            "logger_handler_port": 9999,
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "StreamHandler",
            "logger_level": "DEBUG",
            "logger_msg": "test",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "StreamHandler",
            "logger_level": "INFO",
            "logger_msg": "test",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "StreamHandler",
            "logger_level": "ERROR",
            "logger_msg": "test",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "StreamHandler",
            "logger_level": "WARNING",
            "logger_msg": "test",
        },
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={
            "logger_handler": "StreamHandler",
            "logger_level": "CRITICAL",
            "logger_msg": "test",
        },
    )


def test_invalid():
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac1",
        action="Insert1",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac1",
        action="Insert1",
        table_details={
            "table": "collection",
            "collection-id": [
                "catalog_regclim_raster_global_era5_sfc_single_daily_catalog_html_collection"
            ],
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )
    os.environ["stacapi_url"] = "http://localhost:8086"
    os.environ["POSTGRES_PORT"] = "5438"
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="pgstac",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Insert",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Update",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    InsUpDel4STAC(
        stac_dir=os.environ["current_dir"] + "/unittestdata/stac/",
        service_type="stacapi",
        action="Delete",
        logger_properties={"logger_handler": "StreamHandler"},
    )
    os.environ["stacapi_url"] = "http://docker:8082"
    os.environ["POSTGRES_PORT"] = "5439"
