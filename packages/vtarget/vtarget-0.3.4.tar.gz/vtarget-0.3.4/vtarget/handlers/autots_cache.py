from vtarget.utils import TEMP_DIR


def find(arr, prop, value):
    for x in arr:
        if x[prop] == value:
            return x


class __AutoTSCache:
    from typing import Any, Dict, List, Union

    import pandas as pd

    def __load(self, name: str, obj: Union[Any, None] = None) -> Any:
        import os
        import pickle

        if os.path.exists(f"{TEMP_DIR}/cache") and os.path.exists(f"{TEMP_DIR}/cache/autots_{name}"):
            try:
                with open(f"{TEMP_DIR}/cache/autots_{name}", "rb") as file:
                    return pickle.load(file)
            except:
                pass
        if obj is not None:
            return obj()

    def __dump(self, name: str, obj: Any) -> None:
        import os
        import pickle

        if not os.path.exists(f"{TEMP_DIR}/cache"):
            os.mkdir(f"{TEMP_DIR}/cache")
        if os.path.exists(f"{TEMP_DIR}/cache/autots_{name}"):
            os.remove(f"{TEMP_DIR}/cache/autots_{name}")
        with open(f"{TEMP_DIR}/cache/autots_{name}.tmp", "wb") as file:
            pickle.dump(obj, file)
        os.rename(f"{TEMP_DIR}/cache/autots_{name}.tmp", f"{TEMP_DIR}/cache/autots_{name}")

    # NOTE: Getters and setters

    def get_df(self) -> pd.DataFrame:
        import pandas as pd

        return self.__load("df", pd.DataFrame)

    def set_df(self, df: pd.DataFrame):
        self.__dump("df", df)

    def get_basic_config(self) -> Dict:
        return self.__load("basic_config", dict)

    def set_basic_config(self, basic_config: Dict):
        self.__dump("basic_config", basic_config)

    def get_ts_quality(self) -> Dict:
        return self.__load("ts_quality", dict)

    def set_ts_quality(self, ts_quality: Dict):
        self.__dump("ts_quality", ts_quality)

    def get_series(self) -> List[Dict[str, Any]]:
        return self.__load("series", list)

    def set_series(self, series: List[Dict[str, Any]]):
        self.__dump("series", series)

    def get_current_serie_name(self) -> str:
        return self.__load("current_serie_name", str)

    def set_current_serie_name(self, current_serie_name: str):
        self.__dump("current_serie_name", current_serie_name)

    def get_current_model_name(self) -> str:
        return self.__load("current_model_name", str)

    def set_current_model_name(self, current_model_name: str):
        self.__dump("current_model_name", current_model_name)

    def get_automl_search(self):
        return self.__load("automl_search")

    def set_automl_search(self, automl_search):
        self.__dump("automl_search", automl_search)

    # NOTE: Methods

    def is_a_serie_model(self, model_name: str, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        model = self.find_serie_model(serie_name, model_name)
        return model is not None

    def find_serie(
        self,
        serie_name: str,
        series: Union[List[Dict[str, Any]], None] = None,
    ) -> Union[Dict[str, Any], None]:
        series = series or self.get_series()
        return find(series, "name", serie_name)

    def find_serie_model(
        self,
        serie_name: str,
        model_name: str,
        series: Union[List[Dict[str, Any]], None] = None,
    ) -> dict:
        series = series or self.get_series()
        serie_name = find(series, "name", serie_name)
        if serie_name is not None and serie_name["models"] is not None and len(serie_name["models"]) > 0:
            return find(serie_name["models"], "name", model_name)

    def set_serie_model_prop(
        self,
        prop: str,
        value: any,
        serie_name: str = None,
        model_name: str = None,
    ):
        import json

        from vtarget.handlers.event_handler import event_handler

        series = self.get_series()
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        if model_name is None:
            model_name = self.get_current_model_name()

        model = self.find_serie_model(serie_name, model_name, series)
        if model is not None:
            model[prop] = value
            event_handler.emit_queue.put(
                {
                    "name": "autots.update_model",
                    "data": json.dumps({"serie": serie_name, "model": model}, default=str),
                }
            )
        self.set_series(series)

    def update_serie_model(self, props: dict = {}, serie_name: str = None, model_name: str = None):
        import json

        from vtarget.handlers.event_handler import event_handler

        series = self.get_series()
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        if model_name is None:
            model_name = self.get_current_model_name()
        model = self.find_serie_model(serie_name, model_name, series)
        if model is not None:
            model.update(props)
            event_handler.emit_queue.put(
                {
                    "name": "autots.update_model",
                    "data": json.dumps({"serie": serie_name, "model": model}, default=str),
                }
            )
        self.set_series(series)

    def update_serie(self, props: dict = {}, serie_name: str = None, send_to_view: bool = True):
        import json

        from termcolor import colored

        from vtarget.handlers.event_handler import event_handler

        series = self.get_series()

        if serie_name is None:
            serie_name = self.get_current_serie_name()

        serie = self.find_serie(serie_name, series)

        if serie is not None:
            serie.update(props)
            if send_to_view:
                event_handler.emit_queue.put(
                    {
                        "name": "autots.update_serie",
                        "data": json.dumps(
                            {k: v for k, v in serie.items() if k not in ["partition_data"]},
                            default=str,
                        ),
                    }
                )
        else:
            print(colored("NO EXISTE SERIE", "red", "on_white"))
        self.set_series(series)

    def get_serie_prop(self, prop: str, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        if serie is not None:
            if prop in serie:
                return serie[prop]
        return None


autots_cache = __AutoTSCache()
