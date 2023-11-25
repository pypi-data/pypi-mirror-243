import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DataCleansing:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Data Cleansing")

        selected_columns: list = settings["columns"] if "columns" in settings and settings["columns"] else []
        replace_blanks: bool = settings["replace_blanks"] if "replace_blanks" in settings else False
        replace_zeros: bool = settings["replace_zeros"] if "replace_zeros" in settings else False
        remove_leading_trailing: bool = settings["remove_leading_trailing"] if "remove_leading_trailing" in settings else False
        remove_tabs_line_breaks: bool = settings["remove_tabs_line_breaks"] if "remove_tabs_line_breaks" in settings else False
        remove_all_whitespaces: bool = settings["remove_all_whitespaces"] if "remove_all_whitespaces" in settings else False
        remove_letters: bool = settings["remove_letters"] if "remove_letters" in settings else False
        remove_numbers: bool = settings["remove_numbers"] if "remove_numbers" in settings else False
        remove_punctuation: bool = settings["remove_punctuation"] if "remove_punctuation" in settings else False
        remove_nulls: bool = settings["remove_nulls"] if "remove_nulls" in settings else False
        modify_case_type: str = settings["modify_case_type"] if "modify_case_type" in settings and settings["modify_case_type"] else None

        try:
            columns = selected_columns if selected_columns else df.columns
            for column in columns:
                if replace_blanks and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].fillna("")
                    script.append(f'df["{column}"] = df["{column}"].fillna("")')
                if replace_zeros and pd.api.types.is_numeric_dtype(df[column]):
                    df[column] = df[column].fillna(0)
                    script.append(f'df["{column}"] = df["{column}"].fillna(0)')
                if remove_leading_trailing and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.strip()
                    script.append(f'df["{column}"].str.strip()')
                if remove_tabs_line_breaks and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.replace(r"[ \r\t\n]+", " ")
                    script.append(f'df["{column}"] = df["{column}"].str.replace(r"[ \\r\\t\\n]+", " ")')
                if remove_all_whitespaces and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.replace(" ", "")
                    script.append(f'df["{column}"] = df["{column}"].str.replace(" ", "")')
                if remove_letters and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.replace(r"[a-zA-Z]", "")
                    script.append(f'df["{column}"] = df["{column}"].str.replace(r"[a-zA-Z]", "")')
                if remove_numbers and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.replace(r"\d", "")
                    script.append(f'df["{column}"] = df["{column}"].str.replace(r"\d", "")')
                if remove_punctuation and pd.api.types.is_string_dtype(df[column]):
                    df[column] = df[column].str.replace(r"[^\w\s]", "")
                    script.append(f'df["{column}"] = df["{column}"].str.replace(r"[^\w\s]", "")')
                if remove_nulls:
                    df = df.dropna(subset=[column])
                    script.append(f'df = df.dropna(subset=["{column}"])')
                if modify_case_type and pd.api.types.is_string_dtype(df[column]):
                    if modify_case_type == "upper_case":
                        df[column] = df[column].str.upper()
                        script.append(f'df["{column}"] = df["{column}"].str.upper()')
                    if modify_case_type == "lower_case":
                        df[column] = df[column].str.lower()
                        script.append(f'df["{column}"] = df["{column}"].str.lower()')
                    if modify_case_type == "title_case":
                        df[column] = df[column].str.title()
                        script.append(f'df["{column}"] = df["{column}"].str.title()')

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
