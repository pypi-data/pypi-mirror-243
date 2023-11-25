import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Pivot:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# PIVOT")

        # Definición de las funciones de agregación
        def concat(x, sep):
            return sep.join(x)

        # * Validar campos obligatorios
        missing = list(set(["col_group", "col_header", "col_value", "agg_method"]) - set(settings.keys()))

        if len(missing) != 0:
            msg = app_message.dataprep["nodes"]["pivot"]["incompleted_fields"](node_key, missing)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        # Obtengo las configuraciones
        col_group: list[str] = settings["col_group"] if "col_group" in settings and settings["col_group"] else []
        col_header: str = settings["col_header"] if "col_header" in settings and settings["col_header"] else ""
        col_value: str = settings["col_value"] if "col_value" in settings and settings["col_value"] else ""
        agg_method: list[str] = settings["agg_method"] if "agg_method" in settings and settings["agg_method"] else []
        separator: str = settings["separator"] if "separator" in settings and settings["separator"] else ","
        remove_prefix: bool = settings["remove_prefix"] if "remove_prefix" in settings else False

        agg_fn = []
        for am in agg_method:
            if am in ["Concatenate", "Concat"]:

                def lmbd(x):
                    return concat(x, separator)

                lmbd.__name__ = "concat"
                agg_fn.append(lmbd)
            elif am == "Count (Without Nulls)":
                agg_fn.append(lambda x: len(x.dropna().unique()))
            elif am == "Count (With Nulls)":
                agg_fn.append("count")
            elif am == "Average":
                agg_fn.append("mean")
            else:
                agg_fn.append(am.lower())

        # Pivotea la tabla utilizando los métodos de agregación seleccionados
        try:
            df = pd.pivot_table(df, index=col_group, columns=col_header, values=col_value, aggfunc=agg_fn).reset_index()
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        if remove_prefix and len(agg_method) == 1:
            df.columns = [x[1] if str(x[1]) else str(x[0]) for x in df.columns]
        else:
            df.columns = ["_".join(list(map(str, x))) if str(x[1]) else str(x[0]) for x in df.columns]

        script.append("df = pd.pivot_table(df, index={}, columns={}, values={}, aggfunc={}).reset_index()".format(col_group, col_header, col_value, agg_fn))
        script.append('df.columns = ["_".join(list(map(str, x))) if x[1] else x[0] for x in df.columns ]')

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
