import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.utilities import database_utilities


class Database:
    def exec(self, flow_id, node_key, pin, settings):
        import pyodbc
        import snowflake.connector
        from google.cloud import bigquery
        from google.oauth2 import service_account
        from pymongo import MongoClient
        from sqlalchemy import create_engine, text

        script = []
        script.append("\n# DATABASE")

        try:
            # Valida los campos de entrada y los nombres de los campos que utilizará cada conexión
            checked, msg = database_utilities.check_fields(settings, tier="data")
            if not checked:
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            source = settings["source"]

            if source == "postgresql" or source == "mysql" or source == "sqlite" or source == "mariadb" or source == "oracle":
                table: str = settings["table"] if ("table" in settings and settings["table"] is not None) else None
                query: str = settings["query"] if ("query" in settings and settings["query"] is not None) else None
                connection = database_utilities.get_url_connection(settings, with_database=True)

                engine = create_engine(connection)
                df = pd.read_sql(text(query if query else f'SELECT * FROM "{table}"'), con=engine.connect())
                engine.dispose()

            elif source == "sqlserver_2000":
                table: str = settings["table"] if ("table" in settings and settings["table"] is not None) else None
                query: str = settings["query"] if ("query" in settings and settings["query"] is not None) else None
                connection = database_utilities.get_url_connection(settings, with_database=True)

                engine = pyodbc.connect(connection)
                cursor = engine.cursor()
                cursor.execute(query if query else f"SELECT * FROM [{table}]")
                results = np.array(cursor.fetchall())
                column_names = [str(column[0]) for column in cursor.description]
                df = pd.DataFrame(results, columns=column_names)
                cursor.close()
                engine.close()

            elif source == "bigquery":
                service_account_host = settings["service_account_host"]
                database = settings["database"]
                project = settings["project"]
                table = settings["table"]

                with open(service_account_host) as file:
                    service_account_host = json.load(file)
                    credentials = service_account.Credentials.from_service_account_info(service_account_host)
                    client = bigquery.Client(credentials=credentials)
                    table_ref = client.dataset(database, project=project).table(table)
                    rows = client.list_rows(table_ref)
                    df = rows.to_dataframe()

                    client.close()

            elif source == "snowflake":
                table: str = settings["table"] if ("table" in settings and settings["table"] is not None) else None
                query: str = settings["query"] if ("query" in settings and settings["query"] is not None) else None
                user = settings["user"]
                database = settings["database"]
                project = settings["project"]
                account = settings["account"]
                password = settings["password"]
                connection = snowflake.connector.connect(user=user, password=password, account=account, database=project, schema=database)
                cursor = connection.cursor()
                cursor.execute(query if query else f'SELECT * FROM "{table}"')
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(results, columns=column_names)
                connection.close()
                cursor.close()
            elif source == "mongodb":
                mongo_client = settings["mongo_client"]
                database = settings["database"]
                table = settings["table"]
                client = MongoClient(mongo_client)
                db = client[database]
                collection = db[table]
                data = list(collection.find())
                df = pd.DataFrame(data)
                client.close()
            else:
                msg = app_message.dataprep["nodes"]["database"]["source_required"](node_key)
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))
        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
