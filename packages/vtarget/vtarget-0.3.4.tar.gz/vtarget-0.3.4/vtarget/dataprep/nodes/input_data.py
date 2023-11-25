import json
import os

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils import normpath


class InputData:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        encoding: str = settings["encoding"] if "encoding" in settings else "ISO-8859-1"
        dtype = str if "as_string" in settings and settings["as_string"] == True else None
        delimiter: str = settings["delimiter"] if "delimiter" in settings and settings["delimiter"] else None
        header: str = None if "has_header" in settings and settings["has_header"] == False else "infer"
        file_path = normpath(settings["file_path"]) if "file_path" in settings else ""

        # * Deploy mode habilitado
        deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False

        if deploy_enabled:
            if "deploy_file_path" not in settings or not settings["deploy_file_path"]:
                msg = app_message.dataprep["nodes"]["deploy_enabled"](node_key)
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            file_path = normpath(settings["deploy_file_path"]) if "deploy_file_path" in settings else ""

        _, file_ext = os.path.splitext(file_path)
        file_ext = file_ext[1:]
        try:
            bug_handler.console('Leyendo fuente "{}"...'.format(file_path), "trace", flow_id)
            if file_ext in ["csv", "txt"]:
                df = pd.read_csv(
                    file_path,
                    dtype=dtype,
                    encoding=encoding,
                    delimiter=delimiter,
                    header=header,
                    prefix="col_" if header is None else None,
                )
            elif file_ext == "json":
                orient = settings["orient"] if "orient" in settings else "columns"
                df = pd.read_json(file_path, orient=orient, encoding=encoding)
            elif file_ext in ["xls", "xlsx", "xlsm", "xlsb"]:
                sheet_name = settings["sheet_name"] if "sheet_name" in settings else 0
                df = pd.read_excel(file_path, dtype=dtype, sheet_name=sheet_name)
            else:
                msg = app_message.dataprep["nodes"]["input_data"]["unknow_format"](node_key, file_ext)
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            df.columns = [str(c) for c in df.columns]

            # revisar si alguna nombre de columna tiene espacio al inicio o al final
            if True in [c.startswith((" ", "\t")) or c.endswith((" ", "\t")) for c in df.columns]:
                df.columns = [c.strip() for c in df.columns]
                msg = app_message.dataprep["nodes"]["input_data"]["end_start_spaces"](node_key)
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="warn", bug_level="warning")

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        # TODO: Modificar por tipo de archivo, csv, json, excel
        script.append("\n# INPUT")
        script.append("df = pd.read_csv('{}', encoding='{}')".format(file_path, encoding))
        script.append(f"df = df.astype(str)")

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
