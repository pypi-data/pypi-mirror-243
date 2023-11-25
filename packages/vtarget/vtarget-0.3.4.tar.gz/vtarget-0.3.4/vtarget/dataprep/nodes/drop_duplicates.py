import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DropDuplicates:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Drop Duplicates")

        columns: list[str] = settings["columns"] if ("columns" in settings and settings["columns"]) else []
        keep: str = settings["keep"] if ("keep" in settings and settings["keep"]) else "first"
        only_subset: bool = settings["only_subset"] if "only_subset" in settings else False

        try:
            if len(columns) == 0:
                df = df.drop_duplicates(keep=keep)
                script.append(f"df = df.drop_duplicates(keep={keep})")
            else:
                df = df.drop_duplicates(subset=columns, keep=keep)
                script.append(f"df = df.drop_duplicates(subset={columns}, keep={keep})")

            if only_subset:
                df = df[columns]
                script.append(f"df = df[{columns}]")

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
