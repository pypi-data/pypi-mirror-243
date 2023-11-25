import importlib
import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Formula:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# FORMULA")

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

        for i, item in enumerate(settings["items"]):
            col_name: str = ""
            if not item["field"]:  # crea una columna nueva
                col_name = item["new_column_name"] if "new_column_name" in item and item["new_column_name"] else f"x_{i}"
            else:  # Edita una existente
                col_name = item["field"]
            if "sentence" not in item:
                continue

            try:
                df = df.copy()  # con esto evito los warning
                df.loc[:, col_name] = eval(item["sentence"])
                script.append("df.loc[:, '{}'] = {}".format(col_name, item["sentence"]))
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
