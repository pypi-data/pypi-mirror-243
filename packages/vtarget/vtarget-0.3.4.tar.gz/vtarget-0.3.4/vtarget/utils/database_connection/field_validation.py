# TIER 1
FIELD_VALIDATION_DATABASE = {
    "oracle": {
        "database": {
            "required": ["host", "user", "service_name"],
        },
        "table": {"required": ["host", "user", "service_name", "database"]},
        "data": {
            "required": ["host", "user", "service_name", "database"],
            "optional": [["table", "query"]],
        },
        "write_data": {"required": ["host", "user", "service_name", "database", "table", "save_type"]},
    },
    "sqlserver_2000": {
        "database": {
            "required": ["host", "user"],
        },
        "table": {"required": ["host", "user", "database"]},
        "data": {"required": ["host", "user", "database"], "optional": [["table", "query"]]},
        "write_data": {"required": ["host", "user", "database", "table", "save_type"]},
    },
    "postgresql": {
        "database": {
            "required": ["host", "user"],
        },
        "table": {"required": ["host", "user", "database"]},
        "data": {"required": ["host", "user", "database"], "optional": [["table", "query"]]},
        "write_data": {"required": ["host", "user", "database", "table", "save_type"]},
    },
    "mysql": {
        "database": {"required": ["host", "user"]},
        "table": {"required": ["host", "user", "database"]},
        "data": {"required": ["host", "user", "database"], "optional": [["table", "query"]]},
        "write_data": {"required": ["host", "user", "database", "table", "save_type"]},
    },
    "mariadb": {
        "database": {"required": ["host", "user"]},
        "table": {"required": ["host", "user", "database"]},
        "data": {"required": ["host", "user", "database"], "optional": [["table", "query"]]},
        "write_data": {"required": ["host", "user", "database", "table", "save_type"]},
    },
    "sqlite": {
        "database": {"required": ["path"]},
        "table": {"required": ["path"]},
        "data": {"required": ["path"], "optional": [["table", "query"]]},
        "write_data": {"required": ["path", "table", "save_type"]},
    },
    "mongodb": {
        "database": {"required": ["mongo_client"]},
        "table": {"required": ["mongo_client", "database"]},
        "data": {"required": ["mongo_client", "database", "table"]},
        "write_data": {"required": ["mongo_client", "database", "table", "save_type"]},
    },
    "bigquery": {
        "project": {"required": ["service_account_host"]},
        "database": {"required": ["service_account_host", "project"]},
        "table": {"required": ["service_account_host", "project", "database"]},
        "data": {"required": ["service_account_host", "project", "database", "table"]},
        "write_data": {"required": ["service_account_host", "project", "database", "table", "save_type"]},
    },
    "snowflake": {
        "project": {"required": ["account", "user", "password"]},
        "database": {"required": ["account", "user", "password", "project"]},
        "table": {"required": ["account", "user", "password", "project", "database"]},
        "data": {
            "required": ["account", "user", "password", "project", "database"],
            "optional": [["table", "query"]],
        },
        "write_data": {"required": ["account", "user", "password", "project", "database", "table", "save_type"]},
    },
}
