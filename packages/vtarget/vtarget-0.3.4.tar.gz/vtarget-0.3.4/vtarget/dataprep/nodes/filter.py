import importlib
import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Filter:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        if "rule_type" not in settings:
            msg = app_message.dataprep["nodes"]["filter"]["rules"](node_key)
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            return {"T": pd.DataFrame(), "F": pd.DataFrame()}

        df: pd.DataFrame = pin["In"].copy()
        df_T, df_F = pd.DataFrame(), pd.DataFrame()
        if settings["rule_type"] == "preconfigured":
            try:
                df_T, df_F = self.filter_preconfigured(flow_id, node_key, df, settings)
            except Exception as e:
                msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
                bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                return {"T": pd.DataFrame(), "F": pd.DataFrame()}

        elif settings["rule_type"] == "code":
            # Agrego los modulos y alias al entorno de variables globales
            imports_code: str = settings["imports"] if "imports" in settings and settings["imports"] else ""
            used_modules = utilities.find_imports(imports_code)
            for m in used_modules:
                try:
                    if m["alias"]:
                        globals()[m["alias"]] = importlib.import_module(m["name"])
                    else:
                        globals().update(importlib.import_module(m["name"]).__dict__)
                except ModuleNotFoundError as e:
                    import os
                    import subprocess

                    current_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                    python_path = os.path.join(current_path, "python", "python")
                    if os.path.exists(python_path):
                        subprocess.run(
                            [
                                python_path,
                                "-m",
                                "pipenv",
                                "install",
                                "--skip-lock",
                                m["name"].split(".")[0],
                            ]
                        )
                    else:
                        import pip

                        pip.main(["install", m["name"].split(".")[0]])
                    if m["alias"]:
                        globals()[m["alias"]] = importlib.import_module(m["name"])
                    else:
                        globals().update(importlib.import_module(m["name"]).__dict__)
            df_T, df_F = self.filter_code(flow_id, node_key, df, settings["sentence"])
        else:
            msg = app_message.dataprep["nodes"]["filter"]["unknow_rule"](node_key, str(settings["rule_type"]))
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="warn", bug_level="warning")
        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"T": df_T, "F": df_F},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )
        script_handler.script += self.script.copy()
        self.script = []
        return {"T": df_T, "F": df_F}

    # Nodo: filter - Procesa el filtro de sentencia
    def filter_code(self, flow_id, node_key, df, sentence):
        self.script.append("\n# FILTER (CUSTOMIZED)")
        str_rule = "df[{}]".format(sentence)
        try:
            df_T = eval(str_rule)
            self.script.append("df_T = {}".format(str_rule))
        except Exception as e:
            msg = app_message.dataprep["nodes"]["filter"]["failed_condition"](node_key)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return pd.DataFrame(), pd.DataFrame()
        else:
            # Obtengo el complemento (la parte negada de la condición)
            df_F = df[~df.index.isin(df_T.index)]
            self.script.append("df_F = df[~df.index.isin(df_T.index)]")
            return df_T, df_F

    # Nodo: filter - Procesa el filtro preconfigurado
    def filter_preconfigured(self, flow_id, node_key, df: pd.DataFrame, rule):
        df_T, df_F = pd.DataFrame(), pd.DataFrame()
        self.script.append("\n# FILTER (PRECONFIGURED)")
        field: str = rule["field"]
        operator: str = rule["operator"]
        value: str = rule["value"] if "value" in rule else '""'
        sensitive_case: bool = True if pd.api.types.is_string_dtype(df[field]) and "sensitive_case" in rule and rule["sensitive_case"] else False
        if field not in df.columns:
            # msg = "(filter_code) No existe la columna {} en el dataframe de entrada".format(field)
            msg = app_message.dataprep["nodes"]["filter"]["unknow_column"](node_key, field)
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            return pd.DataFrame(), pd.DataFrame()

        if pd.api.types.is_datetime64_any_dtype(df[field]):
            value = "'{}'".format(value)
        if operator == "=":  # Numeric, String
            if pd.api.types.is_string_dtype(df[field]):
                value = "'{}'".format(value)
            str_rule = "df[(df['{}'] == {})]".format(field, value)
            if not sensitive_case:
                str_rule = "df[(df['{}'].str.lower() == {}.lower())]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "!=":  # Numeric, String
            if pd.api.types.is_string_dtype(df[field]):
                value = "'{}'".format(value)
            str_rule = "df[(df['{}'] != {})]".format(field, value)
            if not sensitive_case:
                str_rule = "df[(df['{}'].str.lower() != {}.lower())]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "<":  # Numeric
            str_rule = "df[(df['{}'] < {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "<=":  # Numeric
            str_rule = "df[(df['{}'] <= {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == ">":  # Numeric
            str_rule = "df[(df['{}'] > {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == ">=":  # Numeric
            str_rule = "df[(df['{}'] >= {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_null":  # Numeric, String
            df_T = df[df[field].isnull()]
            self.script.append("df_T = df[df['{}'].isnull()]".format(field))
        elif operator == "is_not_null":  # Numeric, String
            df_T = df[df[field].notnull()]
            self.script.append("df_T = df[df['{}'].notnull()]".format(field))
        elif operator == "contains":  # String
            df_T = df[df[field].str.contains(value, case=sensitive_case)]
            self.script.append("df_T = df[df['{}'].str.contains('{}', case={})]".format(field, value, sensitive_case))
        elif operator == "does_not_contain":  # String
            df_T = df[~df[field].str.contains(value, case=sensitive_case)]
            self.script.append("df_T = df[~df['{}'].str.contains('{}', case={})]".format(field, value, sensitive_case))
        elif operator == "is_empty":  # String
            str_rule = "df[(df['{}'] == " ")]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_not_empty":  # String
            str_rule = "df[(df['{}'] != " ")]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_true":  # True
            str_rule = "df[(df['{}'] == True)]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_false":  # False
            str_rule = "df[(df['{}'] == False)]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        else:
            msg = app_message.dataprep["filter"]["unknow_operator"](node_key, rule["operator"])
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error", bug_level="error")
        # Obtengo el complemento (la parte negada de la condición)
        df_F = df[~df.index.isin(df_T.index)]
        self.script.append(f"df_F = df[~df.index.isin(df_T.index)]")

        return df_T, df_F
