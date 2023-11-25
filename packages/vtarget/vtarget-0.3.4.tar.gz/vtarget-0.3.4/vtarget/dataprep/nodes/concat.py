import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Concat:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        script.append("\n# CONCAT")
        df_A: pd.DataFrame = pin["A"].copy()
        df_B: pd.DataFrame = pin["B"].copy()
        selected_A: list = settings["a"] if "a" in settings and settings["a"] else None
        selected_B: list = settings["b"] if "b" in settings and settings["b"] else None

        if not selected_A:
            msg = app_message.dataprep["nodes"]["concat"]["column_required"](node_key, "A")
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_A = df_A[selected_A]
        script.append("df_A = df_A[{}]".format(selected_A))

        # Me quedo con los campos seleccionados del Source
        if not selected_B:
            msg = app_message.dataprep["nodes"]["concat"]["column_required"](node_key, "B")
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_B = df_B[selected_B]
        script.append("df_B = df_B[{}]".format(selected_B))

        try:
            df = pd.concat([df_A, df_B], ignore_index=True)
            script.append("df = pd.concat([df_A, df_B], ignore_index=True)")
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
