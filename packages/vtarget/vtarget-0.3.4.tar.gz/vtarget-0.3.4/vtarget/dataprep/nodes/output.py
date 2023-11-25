import json
import os

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils import normpath


class Output:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script_handler.script.append("\n# OUPUT")
        output_format: str = settings["format"] or "csv"
        output_name: str = settings["name"] if "name" in settings else "output"
        output_path: str = settings["path"] if "path" in settings else ""
        encoding: str = settings["encoding"] or "UTF-8"

        # * Deploy mode habilitado
        deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False
        if deploy_enabled:
            if "deploy_path" not in settings:
                msg = app_message.dataprep["nodes"]["deploy_enabled"](node_key)
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            output_path = settings["deploy_path"] if "deploy_path" in settings else ""

        script = ""
        df: pd.DataFrame = pin["In"].copy()
        try:
            if output_format == "excel":
                file_path = output_path + os.path.sep + output_name + ".xlsx"
                file_path = normpath(file_path)
                df.to_excel(
                    file_path,
                    index=False,
                    encoding=encoding,
                )
                script = f"df.to_excel('{file_path}', index= False, encoding={encoding})"
            else:
                file_path = output_path + os.path.sep + output_name + ".csv"
                file_path = normpath(file_path)
                df.to_csv(
                    file_path,
                    encoding=encoding,
                    index=False,
                )
                script = f"df.to_csv('{file_path}', index= False, encoding={encoding})"

            cache_handler.update_node(
                flow_id,
                node_key,
                {
                    "config": json.dumps(settings, sort_keys=True),
                    "script": script,
                },
            )

            script_handler.script.append(script)

        except Exception as e:
            print("Error (output): ", e)
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        return df
