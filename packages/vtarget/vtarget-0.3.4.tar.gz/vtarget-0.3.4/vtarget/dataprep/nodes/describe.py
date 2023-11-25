import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Describe:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# DESCRIBE")
        all_: str = "all"  # TODO: recibir desde la config
        groupby: list = settings["groupby"] if ("groupby" in settings and settings["groupby"]) else []
        fields: list = settings["fields"] if ("fields" in settings and settings["fields"]) else []
        percentiles: list = settings["percentiles"] if ("percentiles" in settings and settings["percentiles"]) else []
        custom_percentiles: list = settings["custompercentiles"] if ("custompercentiles" in settings and settings["custompercentiles"]) else []

        if "pivot_data" not in settings:
            settings["pivot_data"] = True
        pivot_data: bool = settings["pivot_data"] if "pivot_data" in settings else True

        if not fields:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        fields = list(filter(lambda x: x in df.columns, fields))
        all_percentiles = percentiles + custom_percentiles

        # Quitar percentiles repetidos
        if type(all_percentiles) is list and len(all_percentiles) > 0:
            all_percentiles = list(set(all_percentiles))

        try:
            if groupby:
                df = df.groupby(by=groupby)[fields].describe(include=all_, percentiles=all_percentiles).reset_index()
                script.append("df = df.groupby(by={})[{}].describe(include='{}', percentiles={}).reset_index()".format(groupby, fields, all_, all_percentiles))
                if len(fields) > 1:
                    df.columns = ["_".join(list(map(str, x))) if x[1] else x[0] for x in df.columns]
                    script.append("df.columns = ['_'.join(list(map(str, x))) if x[1] else x[0] for x in df.columns]")
                else:
                    df.columns = [x[1] if x[1] else x[0] for x in df.columns]
                    script.append("df.columns = [x[1] if x[1] else x[0] for x in df.columns]")

            else:
                df = df[fields].describe(include=all_, percentiles=all_percentiles)
                script.append("df = df.describe(include='{}', percentiles={})".format(all_, all_percentiles))
                if pivot_data and len(fields) == 1:
                    df = df.T.reset_index().rename(columns={"index": "column"})
                    script.append("# pivot data")
                    script.append("df = df.T.reset_index().rename(columns={'index': 'column'})")
                else:
                    df = df.reset_index()
                    script.append("df=df.reset_index()")

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        df = df.round(2)
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
