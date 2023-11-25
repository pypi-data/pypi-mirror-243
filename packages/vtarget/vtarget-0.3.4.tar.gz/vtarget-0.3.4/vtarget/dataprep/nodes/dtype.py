import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Dtype:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        df: pd.DataFrame = pin["In"].copy()
        self.script.append("\n# DTYPE")

        if "items" not in settings or not settings["items"]:
            msg = app_message.dataprep["nodes"]["dtype"]["no_columns_selected"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        df, _, rename_cols = self.select_types_and_fields(flow_id, node_key, df, settings["items"])
        # Si hay alguna columna para renombrar en las seleccionadas
        if rename_cols:
            try:
                df = df.rename(columns=rename_cols)
            except Exception as e:
                msg = app_message.dataprep["nodes"]["dtype"]["rename_columns"](node_key)
                return bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            self.script.append("\n# RENAME")
            self.script.append("df = df.rename(columns={})".format(rename_cols))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script.copy(),
            },
        )

        script_handler.script += self.script.copy()
        self.script = []
        return {"Out": df}

    # Retorna el df con las columnas seleccionadas y el tipo de dato
    def select_types_and_fields(self, flow_id: str, node_key: str, df: pd.DataFrame, dtypes: dict):
        # https://pbpython.com/pandas_dtypes.html
        # Obtengo solo los campos seleccionados de la lista total de campos (selected==True)
        # ? Para nodos de tipo DTYPE usar todos los campos, sin importar si estan o no en la config
        if "dtype" in node_key.lower():  # aas
            all_dtypes = utilities.get_dtypes_of_df(df)  # ? Todos los dtypes del Dataframe
            dtypes = all_dtypes | dtypes

        selected_dtypes = (
            dict(
                filter(
                    lambda x: True if "selected" in x[1] and x[1]["selected"] else False,
                    dtypes.items(),
                )
            )
            if "select" in node_key.lower()
            else dtypes
        )

        # Se maneja la posibilidad de que ya no existan columnas que previamente fueron creadas
        available_cols = []
        removed_cols = []
        for field, x in selected_dtypes.items():
            if field in df.columns:
                available_cols.append(field)
            else:
                removed_cols.append(field)
                del dtypes[field]  # dado que no existe la eliminamos de dtypes
                msg = app_message.dataprep["nodes"]["dtype"]["column_not_in_df"](node_key, field)
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True)

        # Remuevo las columnas que ya no existen
        for del_key in removed_cols:
            del selected_dtypes[del_key]

        # Mantiene solamente columnas existentes y seleccionadas
        df = df[available_cols]

        self.script.append("df = df[{}]".format(available_cols))
        self.script.append("\n# DATA TYPES")

        rename_cols = {}

        for field, x in selected_dtypes.items():
            # Genero el diccionario para el renombrado de variables
            if "rename" in dtypes[field] and dtypes[field]["rename"]:
                rename_cols[field] = dtypes[field]["rename"]

            standard_dtypes = [
                "object",
                "bool",
                "category",
                "int8",
                "int16",
                "int32",
                "int64",
                "float16",
                "float32",
                "float64",
            ]

            if x["dtype"] in standard_dtypes:
                # Si el campo ya es un numérico conocido no lo cambio
                if df[field].dtype == x["dtype"]:
                    continue
                df, status = self.select_change_col_dtype(flow_id, node_key, df.copy(), field, x["dtype"])
                if not status:  # Si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"

            elif x["dtype"] in ["datetime64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_datetime(df[field])

                except Exception as e:
                    msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, x["dtype"])
                    bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                    # Si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"

            elif x["dtype"] in ["timedelta64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_timedelta(df[field])
                except Exception as e:
                    msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, x["dtype"])
                    bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                    # si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"

            else:
                msg = app_message.dataprep["nodes"]["dtype"]["unknow_dtype"](node_key, field, x["dtype"])
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="warn", bug_level="warning")
                dtypes[field]["dtype"] = "object"

        # Ordeno las columnas segun el orden que se le dio en la interfaz
        order_cols = list(dict(sorted(selected_dtypes.items(), key=lambda item: item[1]["order"])).keys())
        return df[order_cols], dtypes, rename_cols

    # Cambia el tipo de dato y maneja los errores que podrían salir en el intento
    def select_change_col_dtype(self, flow_id, node_key, df, field, dtype):
        try:
            df[field] = df[field].astype(dtype)
        except Exception as e:
            msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, dtype)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return df, False
        else:
            dtype_ = dtype if isinstance(dtype, str) else dtype.__name__
            self.script.append("df['{0}'] = df['{0}'].astype('{1}')".format(field, dtype_))
            return df, True
