import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.utilities import database_utilities


class DatabaseWrite:
    def exec(self, flow_id, node_key, pin, settings):
        import pyodbc
        import snowflake.connector
        from google.oauth2 import service_account
        from pymongo import MongoClient
        from snowflake.connector.pandas_tools import write_pandas
        from sqlalchemy import create_engine

        df: pd.DataFrame = pin["In"].copy()
        script = []
        script.append("\n# DATABASE WRITE")

        try:
            # Valida los campos de entrada y los nombres de los campos que utilizará cada conexión
            checked, msg = database_utilities.check_fields(settings, tier="write_data", node_key=node_key)

            if not checked:
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            source = settings["source"]
            if source == "postgresql" or source == "mysql" or source == "sqlite" or source == "mariadb" or source == "oracle":
                table = settings["table"]
                save_type = settings["save_type"]
                connection = database_utilities.get_url_connection(settings, with_database=True)
                engine = create_engine(connection)
                df.to_sql(name=table, con=engine, if_exists=save_type, index=False)
                engine.dispose()

            elif source == "sqlserver_2000":
                table = settings["table"]
                save_type = settings["save_type"]
                connection = database_utilities.get_url_connection(settings, with_database=True)
                engine = pyodbc.connect(connection)
                cursor = engine.cursor()
                # Preparación de datos
                columns_name = ", ".join(df.columns)
                values = ", ".join(["?" for x in df.columns])
                params = iter(np.asarray(df).tolist())
                # Limpia o no la tabla seleccionada de la base de datos

                if save_type == "replace":
                    cursor.execute(f"TRUNCATE TABLE {table}")
                # Inserción
                cursor.executemany(f"INSERT INTO {table} ({columns_name}) VALUES ({values})", params)
                cursor.commit()
                cursor.close()
                engine.close()

            elif source == "bigquery":
                service_account_host = settings["service_account_host"]
                database = settings["database"]
                project = settings["project"]
                table = settings["table"]
                save_type = settings["save_type"]
                with open(service_account_host) as file:
                    service_account_host = json.load(file)
                    credentials = service_account.Credentials.from_service_account_info(service_account_host)
                    df.to_gbq(
                        f"{database}.{table}",
                        project_id=project,
                        if_exists=save_type,
                        credentials=credentials,
                    )

            elif source == "snowflake":
                table = settings["table"]
                user = settings["user"]
                database = settings["database"]
                project = settings["project"]
                account = settings["account"]
                password = settings["password"]
                save_type = settings["save_type"]
                connection = snowflake.connector.connect(user=user, password=password, account=account, database=project, schema=database)
                write_pandas(
                    connection,
                    df,
                    table,
                    project,
                    database,
                    overwrite=save_type == "replace",
                    auto_create_table=False,
                )
                connection.close()

            elif source == "mongodb":
                mongo_client = settings["mongo_client"]
                database = settings["database"]
                table = settings["table"]
                save_type = settings["save_type"]
                client = MongoClient(mongo_client)
                db = client[database]
                collection = db[table]
                if save_type == "replace":
                    collection.drop()
                collection.insert_many(df.to_dict("records"), ordered=True)
                client.close()

            else:
                msg = app_message.dataprep["nodes"]["database_write"]["source_required"](node_key)
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
