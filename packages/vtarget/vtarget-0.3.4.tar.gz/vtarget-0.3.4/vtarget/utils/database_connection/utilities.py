from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.field_validation import FIELD_VALIDATION_DATABASE


class Utilities:
    def __init__(self):
        pass

    def check_fields(self, data: dict = dict(), tier: str = str(), node_key: str = str()) -> tuple:
        """
        Método que retorna si los datos entregados en conjunto con el nivel son válidos
        """
        source: str = data["source"] if ("source" in data and data["source"] is not None) else None

        # Valida que venga el recurso de conexión
        if not source:
            return False, app_message.dataprep["nodes"]["database_utilities"]["source_required"](node_key)

        # Valida que el recurso de conexión exista en el arreglo
        if not (source in FIELD_VALIDATION_DATABASE and tier in FIELD_VALIDATION_DATABASE[source]):
            return False, app_message.dataprep["nodes"]["database_utilities"]["check_missing_source"](node_key)

        fields: list = FIELD_VALIDATION_DATABASE[source][tier]["required"]

        # Valida que cada campo tenga valor
        for field in fields:
            if not field in data:
                return False, app_message.dataprep["nodes"]["database_utilities"]["check_fields_to_connection"](node_key, field)

            value: any = data[field]
            if not value:
                return False, app_message.dataprep["nodes"]["database_utilities"]["check_empty_fields"](node_key, field)

        if "optional" in FIELD_VALIDATION_DATABASE[source][tier]:
            # Se recorren los arreglos de claves
            for _list in FIELD_VALIDATION_DATABASE[source][tier]["optional"]:
                flag: bool = False

                # Se recorren las claves
                for field in _list:
                    # Valida que el campo exista en la data y que tenga un valor
                    if field in data and data[field]:
                        flag = True
                        break

                # En caso que no exista ninguna clave con valor, da error
                if not flag:
                    # return False, "(check_fields) Falló la validación de variables opcionales"
                    return False, app_message.dataprep["nodes"]["database_utilities"]["check_optional_fields"](node_key)

        return True, ""

    def get_url_connection(self, data: dict, with_database: bool = False) -> str:
        """
        Método que retorna el string de conexión para cada base de datos
        """
        if data["source"] == "sqlite":
            return f"sqlite:///{data['path']}"

        if data["source"] == "postgresql":
            password: str = ":" + data["password"] if ("password" in data and data["password"] is not None) else ""
            port: str = ":" + str(data["port"]) if ("port" in data and data["port"] is not None) else ""
            database: str = "/" + data["database"] if with_database else ""

            return f"postgresql://{data['user']}{password}@{data['host']}{port}" + database

        if data["source"] == "sqlserver_2000":
            # ['SQL Server', 'SQL Server Native Client 11.0', 'ODBC Driver 17 for SQL Server']
            database: str = f'Database={data["database"]};' if with_database else ""

            return "DRIVER={SQL Server};" + f'User={data["user"]};Password={data["password"]};' + database + f'Server={data["host"]};Port={data["port"]};'

        if data["source"] == "mysql" or data["source"] == "mariadb":
            password: str = ":" + data["password"] if ("password" in data and data["password"] is not None) else ""
            port: str = ":" + str(data["port"]) if ("port" in data and data["port"] is not None) else ""
            database: str = "/" + data["database"] if with_database else ""

            return f"mysql+pymysql://{data['user']}{password}@{data['host']}{port}" + database

        if data["source"] == "oracle":
            password: str = ":" + data["password"] if ("password" in data and data["password"] is not None) else ""
            port: str = ":" + str(data["port"]) if ("port" in data and data["port"] is not None) else ""
            database: str = "/" + data["database"] if with_database else ""
            service_name: str = "?service_name=" + data["service_name"] if data["service_name"] is not None or len(data["service_name"]) > 0 else ""
            return f"oracle+cx_oracle://{data['user']}{password}@{data['host']}{port}{service_name}"


database_utilities = Utilities()
