class Pipeline:
    def __init__(self):
        from vtarget.dataprep.nodes.code import Code
        from vtarget.dataprep.nodes.column import Column
        from vtarget.dataprep.nodes.concat import Concat
        from vtarget.dataprep.nodes.cross_join import CrossJoin
        from vtarget.dataprep.nodes.cumsum import Cumsum
        from vtarget.dataprep.nodes.data_cleansing import DataCleansing
        from vtarget.dataprep.nodes.database import Database
        from vtarget.dataprep.nodes.database_write import DatabaseWrite
        from vtarget.dataprep.nodes.datetime_extract import DatetimeExtract
        from vtarget.dataprep.nodes.datetime_formatter import DatetimeFormatter
        from vtarget.dataprep.nodes.describe import Describe
        from vtarget.dataprep.nodes.df_maker import DfMaker
        from vtarget.dataprep.nodes.drop_duplicates import DropDuplicates
        from vtarget.dataprep.nodes.dtype import Dtype
        from vtarget.dataprep.nodes.email import Email
        from vtarget.dataprep.nodes.excel import ExcelOutput
        from vtarget.dataprep.nodes.filter import Filter
        from vtarget.dataprep.nodes.formula import Formula
        from vtarget.dataprep.nodes.groupby import Groupby
        from vtarget.dataprep.nodes.input_data import InputData
        from vtarget.dataprep.nodes.inter_row import InterRow
        from vtarget.dataprep.nodes.isin import IsIn
        from vtarget.dataprep.nodes.melt import Melt
        from vtarget.dataprep.nodes.merge import Merge
        from vtarget.dataprep.nodes.output import Output
        from vtarget.dataprep.nodes.pivot import Pivot
        from vtarget.dataprep.nodes.shape import Shape
        from vtarget.dataprep.nodes.sort import Sort
        from vtarget.dataprep.nodes.switch import Switch
        from vtarget.dataprep.nodes.unique import Unique
        from vtarget.dataprep.nodes.v_output import VOutput
        from vtarget.dataprep.nodes.value_counts import ValueCounts

        self.decimal_round = False
        self.nodes_instances = {
            "Input_Data": InputData(),
            "Database": Database(),
            "Database_Write": DatabaseWrite(),
            "Sort": Sort(),
            "Filter": Filter(),
            "Formula": Formula(),
            "Merge": Merge(),
            "Group_By": Groupby(),
            "Cross_Join": CrossJoin(),
            "Concat": Concat(),
            "Pivot": Pivot(),
            "Shape": Shape(),
            "Melt": Melt(),
            "Output_Data": Output(),
            "Code": Code(),
            "Value_Counts": ValueCounts(),
            "Describe": Describe(),
            "Isin": IsIn(),
            "Cumsum": Cumsum(),
            "V_Output": VOutput(),
            "Inter_Row": InterRow(),
            "Unique": Unique(),
            "Drop_Duplicates": DropDuplicates(),
            "Data_Cleansing": DataCleansing(),
            "Datetime_Formatter": DatetimeFormatter(),
            "Datetime_Extract": DatetimeExtract(),
            "Switch": Switch(),
            "Select": Dtype(),
            "Dtype": Dtype(),
            "Column": Column(),
            "Excel": ExcelOutput(),
            "Email": Email(),
            "DF_Maker": DfMaker(),
            "Source": Code(),
        }

    def exec(self, flow_id: str, node: dict, input_port: dict):
        import gc
        import json

        import pandas as pd

        from vtarget.dataprep.types import NodeType
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        dict_pout: dict = self.nodes_instances[node["type"]].exec(
            flow_id,
            node["key"],
            input_port,
            node["meta"]["config"] if "config" in node["meta"] else {},
        )

        if "STDOUT" in dict_pout:
            node["meta"]["STDOUT"] = dict_pout["STDOUT"]

        node["meta"]["script"] = (
            cache_handler.settings[flow_id][node["key"]]["script"]
            if node["key"] in cache_handler.settings[flow_id] and "script" in cache_handler.settings[flow_id][node["key"]]
            else []
        )

        # agregar ports_config a caché
        if "ports_config" in node["meta"]:
            cache_handler.update_node(
                flow_id,
                node["key"],
                {"ports_config": json.dumps(node["meta"]["ports_config"], sort_keys=True)},
            )

        for port_name in node["meta"]["ports_map"]["pout"].keys():
            port_config: dict = utilities.get_table_config(node["meta"], port_name)
            port_df: pd.DataFrame = dict_pout[port_name]
            node["meta"]["ports_map"]["pout"][port_name]["head"] = utilities.get_head_of_df_as_list(port_df, port_config, flow_id, node["key"], port_name)
            # TODO: revisar si la referencia de dict_pout se actualiza al modifcar cache por el sort_by del puerto
            node["meta"]["ports_map"]["pout"][port_name]["rows"] = port_df.shape[0]
            node["meta"]["ports_map"]["pout"][port_name]["cols"] = port_df.shape[1]
            prev_dtypes: dict = (
                node["meta"]["ports_map"]["pout"][port_name]["dtypes"]
                if port_name in node["meta"]["ports_map"]["pout"] and "dtypes" in node["meta"]["ports_map"]["pout"][port_name]
                else {}
            )
            new_dtypes: dict = utilities.get_dtypes_of_df(port_df)

            # * Merge dtypes previo con los nuevos, para conservar config de la tabla
            if prev_dtypes and new_dtypes:
                for k in new_dtypes:
                    if k in prev_dtypes:
                        if "visible" in prev_dtypes[k]:
                            new_dtypes[k]["visible"] = prev_dtypes[k]["visible"]
                        if "numberFormat" in prev_dtypes[k]:
                            new_dtypes[k]["numberFormat"] = prev_dtypes[k]["numberFormat"]
                        # * mantener orden seteado desde las opciones de la tabla (excepto para nodos Column, Dtypes y Select)
                        if (
                            node["type"]
                            not in [
                                NodeType.COLUMN.value,
                                NodeType.DTYPE.value,
                                NodeType.SELECT.value,
                            ]
                            and "order" in prev_dtypes[k]
                        ):
                            new_dtypes[k]["order"] = prev_dtypes[k]["order"]

            node["meta"]["ports_map"]["pout"][port_name]["dtypes"] = new_dtypes
            node["meta"]["ports_map"]["pout"][port_name]["summary"] = {}
            node["meta"]["ports_map"]["pout"][port_name]["describe"] = {}
            node["meta"]["readed_from_cache"] = False

        del dict_pout
        gc.collect()
        return node
