import datetime
import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DatetimeFormatter:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Datetime Formatter")
        items: list[str] = settings["items"] if ("items" in settings and settings["items"]) else None

        if items:
            for item in items:
                # column_to_convert, new_column_name, pattern, custom_pattern
                column_to_convert: str = item["column_to_convert"] if "column_to_convert" in item and item["column_to_convert"] else None
                new_column_name: str = item["new_column_name"] if "new_column_name" in item and item["new_column_name"] else column_to_convert
                preconfigured_pattern: str = item["preconfigured_pattern"] if "preconfigured_pattern" in item and item["preconfigured_pattern"] else None
                custom_pattern: str = item["custom_pattern"] if "custom_pattern" in item and item["custom_pattern"] else None

                if not column_to_convert:
                    msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

                if custom_pattern:
                    if custom_pattern[0] not in ["'", '"'] or custom_pattern[-1] not in ["'", '"']:
                        msg = app_message.dataprep["nodes"]["datetime_formatter"]["pattern_quotes"](node_key)
                        return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                    preconfigured_pattern = custom_pattern[1:-1]
                else:
                    if not preconfigured_pattern:
                        msg = app_message.dataprep["nodes"]["datetime_formatter"]["pattern_required"](node_key)
                        return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

                try:
                    script.append(f"""df["{new_column_name}"] = df.apply(lambda x: process_datetime(x["{column_to_convert}"], "{preconfigured_pattern}"), axis=1)""")

                    df[new_column_name] = df.apply(
                        lambda x: self.process_datetime(x[column_to_convert], preconfigured_pattern, script),
                        axis=1,
                    )

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
        else:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")


    def process_datetime(self, _datetime, pattern, script):
        # Hay que ver por qué ocurren estos 2 casos
        # Cuando es string entra como None
        if isinstance(_datetime, float):
            return None
        # Cuando es datetime entra como NaT
        if pd.isnull(_datetime):
            return None
        if not _datetime:
            return None

        result = _datetime
        # Es string
        if isinstance(_datetime, str):
            result = datetime.datetime.strptime(_datetime.lower(), pattern)
            if len(script) == 2:
                script.append(f"""def process_datetime(_datetime, pattern): \n\treturn datetime.datetime.strptime(_datetime.lower(), pattern)""")
        else:
            result = _datetime.strftime(pattern)
            if len(script) == 2:
                script.append(f"""def process_datetime(_datetime, pattern): \n\treturn _datetime.strftime(pattern)""")
        return result
