import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Unique:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Unique")

        # field
        field: list = settings["field"] if "field" in settings and settings["field"] else []

        if not field:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        try:
            df = df.groupby(field).size().reset_index().drop(columns=[0])
            script.append("df = df.groupby({}).size().reset_index().drop(columns=[0])".format(field))
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
