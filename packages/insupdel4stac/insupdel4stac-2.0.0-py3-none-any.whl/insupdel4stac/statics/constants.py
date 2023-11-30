# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

pgstac_configuration_dict = {
    "POSTGRES_HOST_READER": "localhost",
    "POSTGRES_HOST_WRITER": "localhost",
    "POSTGRES_PORT": "5439",
    "POSTGRES_USER": "username",
    "POSTGRES_PASSWORD": "password",
    "POSTGRES_DB": "postgis",
    "PGUSER": "username",
    "PGPASSWORD": "password",
    "PGHOST": "localhost",
    "PGDATABASE": "postgis",
    "PgstacDB_dsn": "",
    "PgstacDB_pool": None,
    "PgstacDB_connection": None,
    "PgstacDB_commit_on_exit": True,
    "PgstacDB_debug": False,
    "PgstacDB_use_queue": False,
}
stacapi_configuration_dict = {
    "stacapi_url": "http://localhost:8082",
    "auth": None,
    "timeout": 2,
    "verify": False,
}
