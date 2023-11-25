import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DfMaker:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# DFMAKER")
        data: list = settings["data"] if "data" in settings and settings["data"] else []

        df = pd.DataFrame()

        # TODO: Agregar Script
        try:
            columns = []
            rows = []
            if len(data):
                columns = [c["value"] or f"col_{idx+1}" for idx, c in enumerate(data[0])]
                if len(data) > 1:
                    rows = [[c["value"] for c in r] for r in data[1:]]

            df = pd.DataFrame(np.array(rows), columns=columns)

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
