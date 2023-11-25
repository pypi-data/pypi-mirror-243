import ast
import json
import re

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from scipy import stats

from vtarget.handlers.cache_handler import cache_handler


class Utilities:
    # retorna la metadata del dtypes de un df
    def get_dtypes_of_df(self, df: pd.DataFrame):
        dict_dtypes = {}
        res = df.dtypes.to_frame("dtypes")
        # print(res)
        res = res["dtypes"].astype(str).reset_index()
        res["selected"] = True
        res["order"] = pd.RangeIndex(stop=res.shape[0])
        # return res.values.tolist()
        # print(res.columns)
        for _, x in res.iterrows():
            dict_dtypes[x["index"]] = {
                "dtype": x["dtypes"],
                "selected": x["selected"],
                "order": x["order"],
            }

        return dict_dtypes

    def get_table_config(self, meta: dict, port_name: str):
        # ? sacar config desde meta.ports_config con el puerto
        ports_config: dict = meta["ports_config"][port_name] if "ports_config" in meta and port_name in meta["ports_config"] else {}
        # print(ports_config)
        return {
            "rows": ports_config["rows"] if "rows" in ports_config and ports_config["rows"] is not None else 50,
            "decimals": ports_config["decimals"] if "decimals" in ports_config and ports_config["decimals"] is not None else -1,
            "source": ports_config["source"] if "source" in ports_config and ports_config["source"] else "head",
            "sort_by": ports_config["sort_by"] if "sort_by" in ports_config and ports_config["sort_by"] else [],
        }

    def sort_df(self, full_df: pd.DataFrame, sorts: list[dict]):
        if sorts:
            setting_list = list(
                map(
                    lambda x: (x["field"], int(x["ascending"])),
                    [item for item in sorts if "field" in item and item["field"]],
                )
            )
            if setting_list:
                columns, order = zip(*setting_list)
                if columns and order:
                    full_df = full_df.sort_values(by=list(columns), ascending=list(order))
        return full_df

    def get_head_of_df_as_list(
        self,
        port_df: pd.DataFrame,
        config: dict,
        flow_id: str = None,
        node_key: str = None,
        port_name: str = None,
    ):
        df: pd.DataFrame = port_df.head(50).copy()
        rows = len(port_df) if config["rows"] > len(port_df) else config["rows"]

        # sort
        if "sort_by" in config and len(config["sort_by"]) > 0:
            port_df = self.sort_df(port_df, config["sort_by"])
            cached_node = cache_handler.cache[flow_id][node_key] if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id] else dict()
            # actualizar cache del nodo con el nuevo order
            if flow_id and node_key and port_name:
                # actualizar cache del nodo con el nuevo order
                if cached_node["pout"]:
                    cached_node["pout"][port_name] = port_df
                    cache_handler.update_node(flow_id, node_key, {"pout": cached_node["pout"]})

        if config["source"] == "head":
            df = port_df[:rows].copy()
        elif config["source"] == "tail":
            df = port_df[-rows:].copy()
        elif config["source"] == "sample":
            df = port_df.sample(rows).copy()
            if "sort_by" in config and len(config["sort_by"]) > 0:
                df = self.sort_df(df, config["sort_by"])
        else:
            df = port_df.head(50).copy()
            print("Source {} no reconocido opciones válidas [head|sample|tail]. Se utilizará head(50)".format(config["source"]))

        # decimals
        if config["decimals"] != -1:
            df = df.round(config["decimals"])

            # float_columns = df.select_dtypes(include=['float16', 'float32', 'float64']).columns
            # for c in float_columns:
            #     df[c] = df[c].apply(lambda x: f'{{:.{config["decimals"]}f}}'.format(x))

        # Esto para efectos de la visualización al transformar a json
        # special_cols = df.select_dtypes(include=['bool', 'datetime64', 'category']).columns.values.tolist()
        special_cols = df.select_dtypes(
            exclude=[
                # "object",  # NOTE: Timestamp parece ser de tipo 'object'. TypeError: Object of type Timestamp is not JSON serializable
                "int8",
                "int16",
                "int32",
                "int64",
                "float16",
                "float32",
                "float64",
            ]
        ).columns.values.tolist()

        if len(special_cols):
            # print(special_cols)
            df[special_cols] = df[special_cols].astype(str)

        # TODO: Ver qué problema entrega esta línea con los vacíos int y string
        df = df.fillna("NaN")  # df = df.fillna(np.nan)

        # df = df.replace([np.inf, -np.inf], 0, inplace=True)
        # print(bool_cols)
        # df_head = [df.columns.values.tolist()] + df.values.tolist()
        df_head = df.to_dict("records")
        return df_head

    def format_setting(self, settings, ignore_keys=["ports_map", "readed_from_cache"]):
        setting_copy = {key: value for key, value in settings.items() if key not in ignore_keys}
        return json.dumps(setting_copy, sort_keys=True)

    def viz_summary(self, df):
        cat_col = df.select_dtypes(include=["object", "category", "bool", "datetime64", "timedelta"]).columns.tolist()
        num_col = df.select_dtypes(include=["int16", "int32", "int64", "float16", "float32", "float64"]).columns.tolist()
        # date_col = df.select_dtypes(include=['datetime64', 'timedelta']).columns.tolist()
        out = {}
        for c in num_col:
            count, bin_ = np.histogram(df[c][np.isfinite(df[c])])
            out[c] = {
                "viz_type": "histogram",
                "y": count.tolist(),
                "x": np.around(bin_, decimals=2).tolist(),
            }

        max_cat = 3
        for c in cat_col:
            cat_viz = "pie"
            vc = df[c].value_counts().iloc[:max_cat]
            vc.index = vc.index.astype("str")
            cat_counts = vc.to_dict()
            if df[c].nunique() > max_cat:
                others = df[~df[c].isin(vc.index)][c].value_counts()
                cat_counts[f"Other ({len(others)})"] = others.sum().item()
                cat_viz = "list"
            out[c] = {"viz_type": cat_viz, "values": cat_counts}
        return out

    def get_central_tendency_measures(self, df: pd.DataFrame):
        if df.empty:
            return {}
        info = df.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9], include="all", datetime_is_numeric=True).T.reset_index()
        # info = info.astype(str)
        # print(info.dtypes)
        jsonlist = json.loads(info.to_json(orient="records"))
        return dict([(x["index"], x) for x in jsonlist])

    def find_imports(self, code_snippet: str):
        code_snippet = "\n".join([l for l in code_snippet.split("\n") if len(l) > 0 and l[0] != "#"])
        # Busco los modulos que tienen la forma ['import * as *']
        matchs = re.findall("import (.*?) as (.*?)$", code_snippet, flags=re.MULTILINE)
        # print(matchs)
        out = [{"name": m[0].strip(), "alias": m[1].strip(), "objects": []} for m in matchs]
        # print(out)
        # Busco los ['from * import *', 'import *']
        # modules = []
        for node in ast.iter_child_nodes(ast.parse(code_snippet)):
            if isinstance(node, ast.ImportFrom):
                objects = [node.names[i].name for i in range(len(node.names))]
                if not node.names[0].asname:  # excluding the 'as' part of import
                    # modules.append(node.module)
                    out.append({"name": node.module, "alias": None, "objects": objects})
            elif isinstance(node, ast.Import):  # excluding the 'as' part of import
                if not node.names[0].asname:
                    out.append({"name": node.names[0].name, "alias": None, "objects": []})
                    # modules.append(node.names[0].name)
        return out

    def iqr_outliers(self, col: pd.Series):
        q1 = col.quantile(0.25)
        q3 = col.quantile(0.75)
        IQR = q3 - q1
        ll = q1 - (1.5 * IQR)
        ul = q3 + (1.5 * IQR)
        upper_outliers = col[col > ul].index.tolist()
        lower_outliers = col[col < ll].index.tolist()
        return list(set(upper_outliers + lower_outliers))

    def zscore_outliers(self, col: pd.Series, limit: int):
        return col[np.abs(stats.zscore(col)) >= limit]

    def get_nulls(self, df: pd.DataFrame):
        nulls = {}
        for col_name in df.columns:
            col = df[col_name]
            nulls[col_name] = len(col[col.isnull()])
        return nulls

    def get_zero_excess(self, col: pd.Series):
        r = col.rolling(int(round(len(col) * 0.05)))
        return col[r.min().eq(0) & r.max().eq(0)]

    def get_interaction_data(self, df: pd.DataFrame, x_col: str, y_col: str, max_cats: int = 5):
        if x_col not in df.columns:
            return {"success": False, "error": f"{x_col} var not in Dataframe"}
        if y_col not in df.columns:
            return {"success": False, "error": f"{y_col} var not in Dataframe"}

        x_isNumeric = is_numeric_dtype(df[x_col])
        y_isNumeric = is_numeric_dtype(df[y_col])

        if x_isNumeric and y_isNumeric:  # ambos numericos
            return {
                "type": "scatter",
                "data": [
                    {
                        "x": df[x_col].values.tolist(),
                        "y": df[y_col].values.tolist(),
                        "mode": "markers",
                        "type": "scatter",
                    }
                ],
            }
        else:
            x_cats = df[x_col].value_counts(dropna=False)[:max_cats].keys()
            y_cats = df[y_col].value_counts(dropna=False)[:max_cats].keys()

            x_cats = [str(x) for x in x_cats]
            y_cats = [str(x) for x in y_cats]

            df["x_"] = df[x_col].apply(lambda l: str(l) if str(l) in x_cats else "Other")
            df["y_"] = df[y_col].apply(lambda l: str(l) if str(l) in y_cats else "Other")

            # agregar contador de others
            other_x = df[df["x_"] == "Other"][x_col].nunique(dropna=False)
            df["x_"] = df["x_"].apply(lambda x: f"{x}({other_x})" if x == "Other" else x)

            other_y = df[df["y_"] == "Other"][y_col].nunique(dropna=False)
            df["y_"] = df["y_"].apply(lambda x: f"{x}({other_y})" if x == "Other" else x)

            if not x_isNumeric and not y_isNumeric:  # ambos categoricos
                df_out = df[["x_", "y_"]].value_counts().reset_index(name="count")
                df_out["x_"] = df_out["x_"].astype(str)
                df_out["y_"] = df_out["y_"].astype(str)

                return {
                    "type": "table",
                    "data": df_out.rename(columns={"x_": "x", "y_": "y"}).to_dict("records"),
                }
            else:  # categorico y numerico
                cat_key = "x_" if y_isNumeric else "y_"
                val_key = "x_" if x_isNumeric else "y_"
                val_col = x_col if x_isNumeric else y_col

                df_out = df.groupby(cat_key)[val_col].apply(list).reset_index(name=val_key.replace("_", ""))
                df_out[cat_key] = df_out[cat_key].astype(str)
                df_out["type"] = "box"
                return {
                    "type": "box",
                    "data": df_out.rename(columns={cat_key: "name"}).to_dict("records"),
                }


utilities = Utilities()
