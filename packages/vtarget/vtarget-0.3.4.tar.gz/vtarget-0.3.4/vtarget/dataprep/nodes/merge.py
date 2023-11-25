import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Merge:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        edf = pd.DataFrame()
        pout_struct = {"L": edf, "J": edf, "R": edf, "F": edf}

        if "iL" not in pin or "iR" not in pin:
            msg = app_message.dataprep["nodes"]["merge"]["input_port"](node_key)
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            return pout_struct

        self.script.append("\n# MERGE")

        # * Columnas de salida
        left_columns: list[str] = settings["left_columns"] if "left_columns" in settings else []
        right_columns: list[str] = settings["right_columns"] if "right_columns" in settings else []

        # * Dataframes de entrada
        df_iL = pin["iL"].copy()
        df_iR = pin["iR"].copy()

        # * Validar que array de columnas de salida exista en su respectivo DF
        for col in left_columns:
            if col not in df_iL:
                msg = app_message.dataprep["nodes"]["merge"]["input_port_il"](node_key, col)
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                return pout_struct

        for col in right_columns:
            if col not in df_iR:
                msg = app_message.dataprep["nodes"]["merge"]["input_port_iR"](node_key, col)
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                return pout_struct

        try:
            df_iL: pd.DataFrame = df_iL[left_columns].copy()
            df_iR: pd.DataFrame = df_iR[right_columns].copy()

            on_l: list[str] = [x["left"] for x in settings["items"] if "left" in x and x["left"]]
            on_r: list[str] = [x["right"] for x in settings["items"] if "right" in x and x["right"]]
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return pout_struct

        if "L" in settings["outputs"]:
            pout_struct["L"] = self.apply_join(flow_id, node_key, "left", df_iL, df_iR, on_l, on_r)
        if "J" in settings["outputs"]:
            pout_struct["J"] = self.apply_join(flow_id, node_key, "inner", df_iL, df_iR, on_l, on_r)
        if "R" in settings["outputs"]:
            pout_struct["R"] = self.apply_join(flow_id, node_key, "right", df_iL, df_iR, on_l, on_r)
        if "F" in settings["outputs"]:
            pout_struct["F"] = self.apply_join(flow_id, node_key, "outer", df_iL, df_iR, on_l, on_r)

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": pout_struct,
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        script_handler.script += self.script
        return pout_struct

    def apply_join(self, flow_id, node_key, how, df_iL, df_iR, on_l, on_r):
        try:
            if how == "outer":
                df_o = pd.merge(
                    df_iL,
                    df_iR,
                    left_on=on_l,
                    right_on=on_r,
                    how="outer",
                    indicator=True,
                )
                # Campo _merge viene como category, lo cambio a object (str)
                df_o["merge_type"] = df_o["_merge"].astype(str)
                del df_o["_merge"]
                self.script.append("df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='outer', indicator=True)".format(on_l, on_r))
            else:
                df_o = pd.merge(df_iL, df_iR, left_on=on_l, right_on=on_r, how=how)
                self.script.append("df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='{}', indicator=True)".format(on_l, on_r, how))
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return pd.DataFrame()
        return df_o

    # def full_outer_join(self, flow_id, node_key, df_iL, df_iR, on_l, on_r):
    # 	try:
    # 		# Outer join con indicator (que genera la columna merge) para sacar sólo las columnas de lado correspondiente
    # 		df_o = pd.merge(df_iL, df_iR, left_on=on_l, right_on=on_r, how="outer", indicator=True)#, validate="many_to_one")
    # 		self.script.append("df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='outer', indicator=True)".format(on_l, on_r))
    # 	except Exception as e:
    # 		msg = '(merge) Exception:' + str(e)
    # 		bug_handler.console(msg, 'fatal', flow_id)
    # 		bug_handler.append({'flow_id': flow_id, 'success': False, 'node_key': node_key, 'level': 'error', 'msg': msg, 'exception': str(e)})
    # 		edf = pd.DataFrame()
    # 		return {'L': edf, 'J': edf, 'R': edf, 'F': edf}

    # 	# print('J',df_iL.shape, df_iR.shape)
    # 	df_l = df_o[df_o['_merge'].isin(['left_only', 'both'])].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)
    # 	df_j = df_o[df_o['_merge'] == 'both'].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)
    # 	df_r = df_o[df_o['_merge'].isin(['right_only', 'both'])].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)

    # 	self.script.append("df_l = df_o[df_o['_merge'] == 'left_only'].drop(columns=['_merge'], axis=1)")
    # 	self.script.append("df_j = df_o[df_o['_merge'] == 'both'].drop(columns=['_merge'], axis=1)")
    # 	self.script.append("df_r = df_o[df_o['_merge'] == 'right_only'].drop(columns=['_merge'], axis=1)")

    # 	df_o['_merge'] = df_o['_merge'].astype(str) # campo _merge viene como category, lo cambio a object (str)
    # 	# df_o.rename(columns={'_merge': 'merge'}, inplace=True)
    # 	# print(df_j.head())

    # 	return {'L': df_l, 'J': df_j, 'R': df_r, 'F': df_o}
