import gc
import os
import pickle
import sys
import traceback
from random import randint
from typing import Any, Dict

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.utils import TEMP_DIR


def get_size(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum([get_size(v) for v in obj.values()])
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i) for i in obj])
    return size


class __Cache_Handler:
    cache: Dict[str, Dict[str, Dict[str, Dict[str, pd.DataFrame]]]]
    settings: Dict[str, Dict[str, Dict[str, Any]]]
    dump_enabled: bool

    def __init__(self):
        super().__init__()
        self.cache = dict()
        self.settings = dict()
        self.dump_enabled = False
        self.wtf = randint(0, 256)

    def write(self, flow_id: str, node_key: str) -> None:
        if flow_id not in self.cache or node_key not in self.cache[flow_id] or "pout" not in self.cache[flow_id][node_key]:
            return
        try:
            if not os.path.exists(f"{TEMP_DIR}/cache"):
                os.mkdir(f"{TEMP_DIR}/cache")
            if not os.path.exists(f"{TEMP_DIR}/cache/{flow_id}"):
                os.mkdir(f"{TEMP_DIR}/cache/{flow_id}")
            for port_name in self.cache[flow_id][node_key]["pout"]:
                if os.path.exists(f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}"):
                    os.remove(f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}")
                with open(f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}.tmp", "wb") as file:
                    pickle.dump(self.cache[flow_id][node_key]["pout"][port_name], file)
                os.rename(
                    f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}.tmp",
                    f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}",
                )
            bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache (stg)', "info", flow_id)
            if self.dump_enabled:
                del self.cache[flow_id][node_key]
                gc.collect()
        except:
            traceback.print_exception(*sys.exc_info())

    def reset(self, flow_id: str):
        if flow_id in self.cache:
            self.cache[flow_id].clear()
            del self.cache[flow_id]
        if flow_id in self.settings:
            self.settings[flow_id].clear()
            del self.settings[flow_id]
        gc.collect()
        if not os.path.exists(f"{TEMP_DIR}/cache"):
            return
        if not os.path.exists(f"{TEMP_DIR}/cache/{flow_id}"):
            return
        for root, dirs, files in os.walk(f"{TEMP_DIR}/cache/{flow_id}", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def update_node(self, flow_id: str, node_key: str, new_props: Dict[str, Any] = {}):
        if node_key not in cache_handler.settings[flow_id]:
            cache_handler.settings[flow_id][node_key] = dict()
        if "pout" in new_props:
            pout: Dict[str, pd.DataFrame] = new_props.pop("pout")
            for port_name in pout:
                if flow_id not in self.cache:
                    self.cache[flow_id] = dict()
                if node_key not in self.cache[flow_id]:
                    self.cache[flow_id][node_key] = dict()
                if "pout" not in self.cache[flow_id][node_key]:
                    self.cache[flow_id][node_key]["pout"] = dict()
                self.cache[flow_id][node_key]["pout"][port_name] = pout[port_name]
            self.settings[flow_id][node_key]["pout"] = list(pout.keys())
        self.settings[flow_id][node_key].update(new_props)
        if not self.dump_enabled:
            if node_key.startswith("v_output"):
                self.write(flow_id, node_key)
            else:
                bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache (ram)', "info", flow_id)

    def delete_node(self, flow_id: str, node_key: str) -> bool:
        cache_deleted = False
        if flow_id in self.cache:
            if node_key in self.cache[flow_id]:
                del self.cache[flow_id][node_key]
                gc.collect()
                cache_deleted = True
        settings_deleted = False
        if flow_id in self.settings:
            if node_key in self.settings[flow_id]:
                del self.settings[flow_id][node_key]
                gc.collect()
                settings_deleted = True
        return cache_deleted and settings_deleted

    def dump(self, flow_id: str, node_key: str) -> None:
        if self.dump_enabled:
            self.write(flow_id, node_key)

    def load(self, flow_id: str, node_key: str, port_name: str) -> None:
        loaded = True
        if flow_id not in self.cache:
            self.cache[flow_id] = dict()
        if node_key not in self.cache[flow_id]:
            self.cache[flow_id][node_key] = dict()
        if "pout" not in self.cache[flow_id][node_key]:
            self.cache[flow_id][node_key]["pout"] = dict()
        # NOTE: se comentó para tener siempre la data actualizada desde el archivo en disco del voutput
        # if port_name not in self.cache[flow_id][node_key]["pout"]:
        if os.path.exists(f"{TEMP_DIR}/cache") and os.path.exists(f"{TEMP_DIR}/cache/{flow_id}") and os.path.exists(f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}"):
            try:
                with open(f"{TEMP_DIR}/cache/{flow_id}/{node_key}_{port_name}", "rb") as file:
                    self.cache[flow_id][node_key]["pout"][port_name] = pickle.load(file)
            except:
                traceback.print_exception(*sys.exc_info())
                loaded = False
        return loaded

    def load_settings(self, flow_id: str) -> None:
        if flow_id not in self.settings:
            self.settings[flow_id] = dict()
        if os.path.exists(f"{TEMP_DIR}/cache") and os.path.exists(f"{TEMP_DIR}/cache/{flow_id}") and os.path.exists(f"{TEMP_DIR}/cache/{flow_id}/settings"):
            try:
                with open(f"{TEMP_DIR}/cache/{flow_id}/settings", "rb") as file:
                    self.settings[flow_id] = pickle.load(file)
            except:
                traceback.print_exception(*sys.exc_info())

    def dump_settings(self, flow_id: str) -> None:
        if flow_id not in self.settings:
            return
        try:
            if not os.path.exists(f"{TEMP_DIR}/cache"):
                os.mkdir(f"{TEMP_DIR}/cache")
            if not os.path.exists(f"{TEMP_DIR}/cache/{flow_id}"):
                os.mkdir(f"{TEMP_DIR}/cache/{flow_id}")
            if os.path.exists(f"{TEMP_DIR}/cache/{flow_id}/settings"):
                os.remove(f"{TEMP_DIR}/cache/{flow_id}/settings")
            with open(f"{TEMP_DIR}/cache/{flow_id}/settings.tmp", "wb") as file:
                pickle.dump(self.settings[flow_id], file)
            os.rename(
                f"{TEMP_DIR}/cache/{flow_id}/settings.tmp",
                f"{TEMP_DIR}/cache/{flow_id}/settings",
            )
            if self.dump_enabled:
                self.settings[flow_id].clear()
                del self.settings[flow_id]
                gc.collect()
        except:
            traceback.print_exception(*sys.exc_info())

    def log(self, *args, **kwargs):
        print("[cache-handler]", *args, **kwargs)


cache_handler = __Cache_Handler()
