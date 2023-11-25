import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Switch:
    def __init__(self):
        self.functionApply = ["is null", "is not null"]
        self.noValueRequired = ["is empty", "is not empty"]

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SWITCH")

        # cases, default_value, new_column
        cases: list = settings["cases"] if "cases" in settings and settings["cases"] else []
        default_value: str = settings["default_value"] if "default_value" in settings and settings["default_value"] else None
        new_column: str = settings["new_column"] if "new_column" in settings and settings["new_column"] else "new_column"

        if not default_value:
            msg = app_message.dataprep["nodes"]["switch"]["default_value"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg)

        try:
            conditions = []
            outputs = []
            script.append("conditions = []")
            script.append("outputs = []")
            for case in cases:
                # Se valida el output
                if "output" not in case or case["output"] == "":
                    raise Exception("Para algún case falta la salida por defecto")

                query = ""
                output = case["output"]
                for condition in case["conditions"]:
                    rule = f" {condition['rule']} " if "rule" in condition else ""
                    operator = condition["operator"]
                    field = condition["field"]
                    value = condition["value"]

                    # Para los que requieren función
                    if operator in self.functionApply:
                        value = f"pd.isnull(df['{field}'])" if operator == "is null" else f"pd.notnull(df['{field}'])"
                        query += f"{rule}{value}"
                    elif operator in self.noValueRequired:
                        value = f'df["{field}"] == ""' if operator == "is empty" else f'df["{field}"] != ""'
                        query += f"{rule}{value}"
                    else:
                        # Se formatean los tipos de datos
                        value = " '{}'".format(value) if pd.api.types.is_string_dtype(df[field]) else value
                        value = " '{}'".format(value) if pd.api.types.is_datetime64_any_dtype(df[field]) else value
                        query += f"{rule}df['{field}'] {operator}{value}"

                outputs.append(output)
                script.append(f'outputs.append("{output}")')
                conditions.append(pd.eval(query))
                script.append(f'conditions.append(pd.eval("{query}"))')

            df[new_column] = np.select(conditions, outputs, default=default_value)
            script.append(f'df["{new_column}"] = np.select(conditions, outputs, default="{default_value}")')

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
