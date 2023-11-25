import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Melt:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# MELT")

        # Obtengo las configuraciones
        id_vars: list[str] = settings["id_vars"] if "id_vars" in settings and settings["id_vars"] else []
        value_vars: list[str] = settings["value_vars"] if "value_vars" in settings and settings["value_vars"] else []

        # Transpone multiples columnas dejandolas en una sola columna con variables categoricas
        try:
            df = pd.melt(df, id_vars=id_vars, value_vars=value_vars).reset_index(drop=True)
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        script.append("df = pd.melt(df, id_vars={}, value_vars={}).reset_index(drop=True)".format(id_vars, value_vars))

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
