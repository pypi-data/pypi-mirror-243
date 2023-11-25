import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class CrossJoin:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        script.append("\n# CROSS_JOIN")
        df_T: pd.DataFrame = pin["Tgt"].copy()
        df_S: pd.DataFrame = pin["Src"].copy()

        # Me quedo con los campos seleccionados del Target
        selected_T: list = settings["tgt"] if "tgt" in settings else []
        if not selected_T:
            msg = app_message.dataprep["nodes"]["cross_join"]["column_required"](node_key, "Target")
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_T = df_T[selected_T]
        script.append("df_T = df_T[{}]".format(selected_T))

        # Me quedo con los campos seleccionados del Source
        selected_S: list = settings["src"] if "src" in settings else []
        if not selected_S:
            msg = app_message.dataprep["nodes"]["cross_join"]["column_required"](node_key, "Source")
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_S = df_S[selected_S]
        script.append("df_S = df_S[{}]".format(selected_S))

        try:
            df = pd.merge(df_T, df_S, how="cross")  # , validate="many_to_one")
            script.append("df = pd.merge(df_T, df_S, how='cross')")

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
