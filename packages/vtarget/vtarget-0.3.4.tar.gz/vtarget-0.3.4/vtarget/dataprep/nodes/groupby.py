import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Groupby:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df = pin["In"].copy()  # pyright: ignore
        script.append("\n# GROUPBY")

        def percentile(n):  # pyright: ignore
            def percentile_(x):
                return np.percentile(x, n)

            percentile_.__name__ = "q%s" % n
            return percentile_

        def count_distinct(x):  # pyright: ignore
            return x.nunique()

        def count_null(x):  # pyright: ignore
            return x.isnull().sum()

        def mode(x):  # pyright: ignore
            return x.value_counts().idxmax()

        def count_blank(x):  # pyright: ignore
            return sum(x == "")

        def count_not_blank(x):  # pyright: ignore
            return sum(x == "")

        # https://www.analyticsvidhya.com/blog/2020/03/groupby-pandas-aggregating-data-python/
        group_by_cols = settings["group_by"] if "group_by" in settings and settings["group_by"] else []
        aggs = settings["agg"] if "agg" in settings and settings["agg"] else []
        agg_cols = {}
        pctl_replaces2 = []
        rename_cols = {}

        for a in aggs:
            action = a["action"]
            if action == "percentile":
                fn_name = "quantile_{}".format(a["pctl_value"])
                action = fn_name
                pctl_replaces2.append((fn_name, a["pctl_value"]))

            # Luego agrupo las funciones de agregación
            if a["column"] not in agg_cols:
                agg_cols[a["column"]] = [action]
            else:
                # Valido que no se agreguen agregaciones repetidas
                if action not in agg_cols[a["column"]]:
                    agg_cols[a["column"]].append(action)

            # Si viene una columna de agregación con un renombre desde la vista
            if "rename" in a and a["rename"]:
                # Creo el nombre compuesto entre la columna y la fn de agg
                current_name = a["column"] + "_" + action
                rename_cols[current_name] = a["rename"]

        agg_str = str(agg_cols)
        for pr in pctl_replaces2:
            agg_str = agg_str.replace("'{}'".format(pr[0]), "percentile({})".format(pr[1]))
        if "count_distinct" in agg_str:
            agg_str = agg_str.replace("'count_distinct'", "count_distinct")
        if "count_null" in agg_str:
            agg_str = agg_str.replace("'count_null'", "count_null")
        if "mode" in agg_str:
            agg_str = agg_str.replace("'mode'", "mode")

        grouped = pd.DataFrame()
        try:
            if group_by_cols:
                grouped = eval("df.groupby(group_by_cols).agg({}).reset_index()".format(agg_str))
                # Dado que las columnas vienen en un multiIndex, con esto reseteo el indice
                grouped.columns = ["_".join(x) if str(x[1]) else str(x[0]) for x in grouped.columns]
                script.append("grouped = df.groupby({}).agg({}).reset_index()".format(group_by_cols, agg_str))
            else:
                grouped = eval("df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str))
                grouped.columns = ["_".join(x) if str(x[1]) else str(x[0]) for x in grouped.columns]
                grouped.drop(columns=["index"], axis=1, inplace=True)
                script.append("grouped = df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str))
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        try:
            grouped.rename(columns=rename_cols, inplace=True)
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": grouped},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": grouped}
