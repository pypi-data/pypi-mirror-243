from vtarget.language.app_message import app_message


class Builder:
    import pandas as pd

    def __init__(self):
        # self.compute_node_counter = 0
        self.nodes: dict = {}
        self.script: str = ""
        self.init_script()  # resetea el script
        self.cur_node_key: str = None
        self.dumpings = 0
        self.execution = 0
        # self.ultra = None

    def init_pipeline(self):
        from vtarget.dataprep.pipeline import Pipeline

        self.pipeline = Pipeline()

    def init_script(self):
        from vtarget.handlers.script_handler import script_handler

        # Headers del script
        script_handler.script.append("#!/usr/bin/env python")
        script_handler.script.append("# coding: utf-8\n")
        script_handler.script.append("import pandas as pd")
        script_handler.script.append("import numpy as np")

    def set_nodes(self, data: dict):
        self.nodes = {}  # Diccionario con los nodos del flujo cuya clave es el atributo "key" del nodo
        for idx, nd in enumerate(data["nodeDataArray"]):
            if not ("isGroup" in nd and nd["isGroup"]) and (nd["type"] not in ["Comment"]) and (nd["category"] not in ["chart"]):  # no es grupo  # no es comment  # no es chart
                self.nodes[nd["key"]] = {
                    "idx": idx,
                    "key": nd["key"],
                    "skip": False,
                    "name": nd["name"],
                    "type": nd["type"],
                    "output": None,
                    "loaded": False,
                    "childs": [],
                    "parents": [],
                }

        # recorrer los links para obtener los padres e hijos por nodo
        for ld in data["linkDataArray"]:
            if "_chart" in ld["to"]:
                continue
            # Agrego los padres
            parent = {"from": ld["from"], "frompid": ld["frompid"], "topid": ld["topid"]}
            if not self.nodes[ld["to"]]["parents"]:
                self.nodes[ld["to"]]["parents"] = [parent]
            else:
                self.nodes[ld["to"]]["parents"].append(parent)

            # Agrego los hijos
            child = {
                "to": ld["to"],
                "topid": ld["topid"],
                "frompid": ld["frompid"],
                "to_id": self.nodes[ld["to"]]["idx"],
            }
            if not self.nodes[ld["from"]]["childs"]:
                self.nodes[ld["from"]]["childs"] = [child]
            else:
                self.nodes[ld["from"]]["childs"].append(child)

    # Resetea todos los nodos hijos cuando cambia la configuración de un padre
    def reset_childs_recursive(self, flow_id: str, node_key: str, reseted_nodes: list):
        import gc

        from vtarget.handlers.cache_handler import cache_handler

        for child in self.nodes[node_key]["childs"]:
            if child["to"] in cache_handler.settings[flow_id]:
                print(node_key, "reset_childs_recursive")
                del cache_handler.settings[flow_id][child["to"]]
                reseted_nodes.append(child["to"])
            self.reset_childs_recursive(flow_id, child["to"], reseted_nodes)
        gc.collect()
        return reseted_nodes

    # Setea a True el parámetro para saltar (no-procesar) los nodos hijos cuando existe un error
    def set_skip_childs_recursive(self, flow_id: str, node_key: str, data: dict):
        for child in self.nodes[node_key]["childs"]:
            # Habilita la bandera para saltarse el nodo
            self.nodes[child["to"]]["skip"] = True
            # Resetea el df completo almacenado en RAM
            self.nodes[child["to"]]["output"] = None
            # Resetea el nodo de gojs
            for port_name in data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"]:
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][port_name]["head"] = []
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][port_name]["rows"] = 0
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][port_name]["cols"] = 0
            data["nodeDataArray"][child["to_id"]]["meta"]["skipped"] = True
            print("=================> se saltará el nodo", child["to"])
            self.set_skip_childs_recursive(flow_id, child["to"], data)
        return True

    # Checkea si todos los hijos están listos
    def check_childs_loaded(self, node_key: str):
        loaded = True
        for child in self.nodes[node_key]["childs"]:
            if not self.nodes[child["to"]]["loaded"]:
                loaded = False
                break
        return loaded

    # Manda a almacenar y liberar los padres que ya están listos
    def dump_parents(self, flow_id, node_key):
        import time

        from vtarget.handlers.cache_handler import cache_handler

        if not cache_handler.dump_enabled:
            return

        t = time.time()

        if not self.nodes[node_key]["loaded"]:
            return
        for parent in self.nodes[node_key]["parents"]:
            if self.check_childs_loaded(parent["from"]):
                cache_handler.dump(flow_id, parent["from"])
        if len(self.nodes[node_key]["childs"]) == 0:
            cache_handler.dump(flow_id, node_key)
        self.dumpings += time.time() - t

    def analyzer(
        self,
        data: dict,
        reset_cache: bool,
        flow_id: str,
        flow_name: str,
        disable_all_write_nodes: bool,
        disable_all_email_nodes: bool,
        deploy_enabled: bool = False,
    ):
        import gc
        import json
        import time
        from typing import Any, Dict

        import pandas as pd

        from vtarget.dataprep.types import NodeType
        from vtarget.handlers.bug_handler import bug_handler
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.handlers.event_handler import event_handler
        from vtarget.handlers.log_handler import log_handler
        from vtarget.handlers.script_handler import script_handler

        print("deploy_enabled", deploy_enabled)

        self.dumpings = 0
        self.execution = 0

        # Reseteo de variables singleton para cada ejecución
        log_handler.log = []
        bug_handler.bug = []
        script_handler.script = []

        # Si se corre el flujo reseteando la cache
        if reset_cache:
            msg = app_message.dataprep["builder"]["reset_cache"](flow_name)
            bug_handler.default_on_error(flow_id, None, msg, console_level="trace", bug_level="info", success=True)
            cache_handler.reset(flow_id)

        # Incializa la caché para el nodo si es que aún no existe
        cache_handler.load_settings(flow_id)
        if flow_id not in cache_handler.cache:
            cache_handler.cache[flow_id] = dict()

        cache_nodes_keys = list(cache_handler.settings[flow_id].keys())

        msg = app_message.dataprep["builder"]["nodes_in_cache"](str(len(cache_nodes_keys)))
        bug_handler.default_on_error(flow_id, None, msg, console_level="trace", bug_level="info", success=True)

        # Inicializa una copia local de los nodos y su metadata
        self.set_nodes(data)

        num_nodes_ok: int = 0  # conteo del número de nodos procesados
        attemps: int = 0  # contador de intentos del while para procesar el flujo completo
        t1 = time.time()  # inicializa el tiempo total de procesamiento de los nodos
        completed_nodes: list = []

        # mientras no estén todos los nodos procesados
        while num_nodes_ok < len(self.nodes):
            # print(num_nodes_ok, "<", len(self.nodes))
            attemps += 1
            for node_key, node_data in self.nodes.items():
                # Salto los nodos que están cargado
                if self.nodes[node_key]["loaded"]:
                    continue

                # * Salto los nodos output data cuando el check de deshabilitar está activado
                if (disable_all_write_nodes and (node_data["type"] in [NodeType.OUTPUTDATA.value, NodeType.EXCEL.value])) or (
                    disable_all_email_nodes and (node_data["type"] in [NodeType.EMAIL.value])
                ):
                    if node_data["type"] in [NodeType.EMAIL.value]:
                        msg = app_message.dataprep["builder"]["not_send"](node_data["key"])
                    else:
                        msg = app_message.dataprep["builder"]["skip_writing"](node_data["key"])
                    bug_handler.default_on_error(flow_id, None, msg, console_level="trace", bug_level="info", success=True)

                    # Para que no entre dos veces en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    self.dump_parents(flow_id, node_key)
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])
                    continue

                # Omito procesar los nodos hijos de un nodo que tuvo un error
                if self.nodes[node_key]["skip"]:
                    bug_handler.console("nodo {} saltado".format(node_data["key"]), "trace", flow_id)
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])
                    continue

                # --------------------------------------------------
                # Dertermina si el/los nodos padres están cargados
                # --------------------------------------------------
                is_loaded = False
                to_load_input_port: Dict[str, Dict[str, Any]] = {}
                # Almancena los df del mapeo de los puertos de entrada
                input_port: Dict[str, pd.DataFrame] = {}
                # Si es una entrada de datos que no tiene padre, se puede procesar
                if not node_data["parents"]:
                    # Omite los nodos de entrada de datos (sin puertos de entrada), ya que por consecuencia no tiene registro de nodos padres
                    if node_data["type"] in [
                        NodeType.INPUTDATA.value,
                        NodeType.DFMAKER.value,
                        NodeType.DATABASE.value,
                        NodeType.SOURCE.value,
                    ]:
                        is_loaded = True
                    else:
                        msg = app_message.dataprep["builder"]["parent_without_entry"](node_data["key"])
                        bug_handler.default_on_error(
                            flow_id,
                            None,
                            msg,
                            console_level="trace",
                            bug_level="info",
                            success=True,
                        )

                        # Para que no entre dos veces en caso que el while haga mas de un intento
                        self.nodes[node_key]["loaded"] = True
                        self.dump_parents(flow_id, node_key)
                        num_nodes_ok += 1
                        completed_nodes.append(node_data["key"])
                        self.set_skip_childs_recursive(flow_id, node_key, data)
                        continue
                else:  # Si el nodo tiene padres
                    # Compruebo si todos los padres tienen sus salidas cargadas
                    for parent in node_data["parents"]:
                        is_loaded = True  # incializo la carga en verdadero
                        # Si está la salida en el nodo padre
                        if self.nodes[parent["from"]]["output"] != None:
                            # if parent['from'] in cache_handler.cache[flow_id]:
                            to_load_input_port[parent["topid"]] = {
                                "node_key": parent["from"],
                                "port_name": parent["frompid"],
                            }
                            # Almaceno en el mapeo de entrada del nodo el df asociado a la salida del padre
                        else:  # Si al menos un padre no está procesado, etonces termina la iteración
                            is_loaded = False  # si al menos uno no está cargado
                            break

                # --------------------------------------------------
                # Si el nodo se puede procesar inicia el procesamiento
                # --------------------------------------------------
                # print(f'is_loaded: {is_loaded} / nodo: ', n_key)
                if is_loaded:
                    node_idx: int = self.nodes[node_key]["idx"]
                    node_name: str = data["nodeDataArray"][node_idx]["name"]
                    node_key: str = data["nodeDataArray"][node_idx]["key"]
                    self.cur_node_key = node_key
                    has_error: bool = False

                    # print(f'PROCESANDO NODO {node_key}')

                    # --------------------------------------------------
                    # Valida si el nodo actual está en caché y si su configuración sigue siendo la misma
                    # --------------------------------------------------
                    node_settings = cache_handler.settings[flow_id][node_key] if node_key in cache_handler.settings[flow_id] else dict()

                    if (
                        node_settings
                        and "config" in node_settings
                        and node_settings["config"] == json.dumps(data["nodeDataArray"][node_idx]["meta"]["config"], sort_keys=True)
                        and (
                            "ports_config" not in node_settings  # no existe ports_config en cache
                            or (
                                "ports_config" in node_settings  # existe ports_config en cache
                                and node_settings["ports_config"]
                                == json.dumps(
                                    data["nodeDataArray"][node_idx]["meta"]["ports_config"],
                                    sort_keys=True,
                                )  # y ports_config no ha cambiado
                            )
                        )
                    ):
                        data["nodeDataArray"][node_idx]["meta"]["readed_from_cache"] = True
                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        script_handler.script += node_settings["script"]
                    # --------------------------------------------------
                    # Procesa el nodo correspondiente y actualiza los valores de los df
                    # --------------------------------------------------
                    else:
                        # --------------------------------------------------
                        # Actualizo los dtypes de la entrada con el dataframe de la salida del nodo anterior
                        # --------------------------------------------------
                        # Omite nodos de entrada de datos (sin puertos de entrada)
                        if node_data["type"] not in [
                            NodeType.INPUTDATA.value,
                            NodeType.DFMAKER.value,
                            NodeType.DATABASE.value,
                            NodeType.SOURCE.value,
                        ]:
                            for _, pin_name in enumerate(data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"]):
                                if "dtypes" in data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name] and pin_name in to_load_input_port:
                                    to_load = to_load_input_port[pin_name]

                                    cache_handler.load(flow_id, to_load["node_key"], to_load["port_name"])

                                    parent_key = to_load["node_key"]
                                    parent_port = to_load["port_name"]
                                    parent_cache = (
                                        cache_handler.cache[flow_id][parent_key] if flow_id in cache_handler.cache and parent_key in cache_handler.cache[flow_id] else dict()
                                    )

                                    if parent_cache and "pout" in parent_cache and parent_port in parent_cache["pout"]:
                                        input_port[pin_name] = parent_cache["pout"][parent_port]

                                        dtypes_list = data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name]["dtypes"]

                                        # NOTE: ¿Esto se ejecuta siempre o solo la primera vez que se carga el nodo?
                                        u_dtypes = self.update_inputs_dtypes(node_name, node_key, dtypes_list, input_port[pin_name])

                                        data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name]["dtypes"] = u_dtypes
                                        # print(pin_index, 'fin')

                        # --------------------------------------------------
                        # Continua con el procesamiento de los nodos que han cambiado
                        # --------------------------------------------------
                        bug_handler.console(f"PROCESANDO NODO {node_key}", "-", flow_id)
                        if node_settings and (
                            (
                                "config" in node_settings
                                and node_settings["config"]
                                != json.dumps(
                                    data["nodeDataArray"][node_idx]["meta"]["config"],
                                    sort_keys=True,
                                )
                            )  # node config ha cambiado
                            or (
                                "ports_config" in node_settings  # existe ports_config en cache
                                # and "ports_config" in data["nodeDataArray"][node_idx]["meta"]
                                and node_settings["ports_config"]
                                != json.dumps(
                                    data["nodeDataArray"][node_idx]["meta"]["ports_config"],
                                    sort_keys=True,
                                )
                            )  # node ports_config ha cambiado
                        ):
                            reseted_nodes = self.reset_childs_recursive(flow_id, node_key, [node_key])
                            event_handler.emit_queue.put(
                                {
                                    "name": "dataprep.reseted_nodes",
                                    "data": {
                                        "flow_id": flow_id,
                                        "reseted_nodes": reseted_nodes,
                                    },
                                }
                            )

                        t = time.time()

                        # agrega parametro de despliegue a la config de cada nodo
                        if "meta" in data["nodeDataArray"][node_idx] and "config" in data["nodeDataArray"][node_idx]["meta"]:
                            data["nodeDataArray"][node_idx]["meta"]["config"]["deploy_enabled"] = deploy_enabled

                        data["nodeDataArray"][node_idx] = self.pipeline.exec(flow_id, data["nodeDataArray"][node_idx], input_port)
                        self.execution += time.time() - t
                        # print(self.execution)

                        has_error = (
                            next(
                                (x for x in bug_handler.bug if x["node_key"] == node_key and x["level"] == "error"),
                                None,
                            )
                            != None
                        )
                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = has_error

                        event_handler.emit_queue.put(
                            {
                                "name": "dataprep.node_processed",
                                "data": {
                                    "flow_id": flow_id,
                                    "key": node_key,
                                    "node": json.dumps(data["nodeDataArray"][node_idx], default=str),
                                    # 'log': log_handler.log, # TODO: Hacer el log del nodo correspondiente
                                },
                            }
                        )

                    # Almaceno los df del mapeo de salida
                    self.nodes[node_key]["output"] = True
                    # Fijo la bandera mara para marcar que el nodo está procesado
                    self.nodes[node_key]["loaded"] = True
                    self.dump_parents(flow_id, node_key)
                    # Aumento el contador para saber que ese nodo fue analizado y salir del while
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])

                    # --------------------------------------------------
                    # Valida si el nodo actual se registró en el singleton de bug con level==error, de estarlo se saltan los hijos de esos nodos
                    # --------------------------------------------------
                    data["nodeDataArray"][node_idx]["meta"]["skipped"] = False
                    data["nodeDataArray"][node_idx]["meta"]["has_error"] = False
                    if has_error:
                        print("\n\n\n----------- has_error", has_error)
                        cache_handler.delete_node(flow_id, node_key)
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = True
                        self.set_skip_childs_recursive(flow_id, node_key, data)

        # --------------------------------------------------
        # Fin del while y for principal
        # --------------------------------------------------
        cache_nodes_keys = list(cache_handler.settings[flow_id].keys())
        msg = app_message.dataprep["builder"]["save_cache"](len(cache_nodes_keys))
        bug_handler.default_on_error(flow_id, None, msg, console_level="debug", bug_level="info", success=True)

        msg = app_message.dataprep["builder"]["processed_flow"](str(round(time.time() - t1, 3)))
        bug_handler.default_on_error(flow_id, None, msg, console_level="debug", bug_level="info", success=True)

        print(self.dumpings, "dumpings")
        print(self.execution, "execution")

        # Una vez que acaba la ejecución del flujo se conforma el script
        self.script = "\n".join(script_handler.script)
        cache_handler.dump_settings(flow_id)
        del self.nodes
        gc.collect()

        return data

    # ---------------------------------------------------------------------------------------
    # Actualiza los dtypes utilizando el df que se está recibiendo de entrada
    # y compara con lo que se tenía en la configuración, manejando tanto la
    # creación de campos que antes no existían, como la eliminación de campos que fueron eliminados

    def update_inputs_dtypes(self, node_name, node_key, current_dtypes, input_df: pd.DataFrame):
        res = input_df.dtypes.to_frame("dtypes")
        res = res["dtypes"].astype(str).reset_index()
        updated_dtypes = {}
        for i, x in res.iterrows():
            updated_dtypes[x["index"]] = {
                "dtype": x["dtypes"],
                "selected": True,
                "order": i,
            }

        return updated_dtypes
        """
        if not len(current_dtypes):
            return current_dtypes

        # Si hay que crear campos nuevos se agregarán al final
        try:
            max_order =  max(list(map(lambda x: x['order'], current_dtypes.values())))
        except Exception as e:
            print('Error (builder): ', e)
            bug_handler.append({'flow_id':flow_id, 'success': False, 'node_key': None, 'level': 'error',
                                        'msg': 'No fue obtener el max de la lista de dtypes', 'exception': str(e)})
            return current_dtypes

        for i,x in res.iterrows():
            if x['index'] in current_dtypes: # si el campo en la salida está en el pin de entrada, sólo actualizo el tipo de dato
                if node_name != 'Select': # los select, al permitir cambiar los datatypes no deben actualizarse
                    current_dtypes[x['index']]['dtype'] = x['dtypes']
            else: # si el campo no está, es porque se editó el flujo en algun punto intermedio y se debe crear el campo
                # del current_dtypes[x['index']]
                max_order += 1
                current_dtypes[x['index']] = {'dtype': x['dtypes'], 'selected': True, 'order': max_order}
                print('previamente no existía el campo "{}" en el nodo "{}", se agrega'.format(x['index'], node_name))
                bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'info',
                                        'msg': 'Campo "{}" no existía en el nodo "{}" previamente, se agrega'.format(x['index'], node_name), 'exception': ''})
                # print('Campo "{}" no existe en nodo "{}" será omitido'.format(x['index'], node_name))
        # print('\n\n\ncurrent_dtypes:\n')
        # print(current_dtypes)
        # Extraigo los campos que antes existían y ya no
        removed_fields = list(set(current_dtypes.keys()) - set(res['index'].tolist()))
        # Remuevo los campos que ya no existen
        # current_dtypes = dict(filter(lambda i: i[0] in res['index'].tolist(), current_dtypes.items()))
        for rf in removed_fields:
            to_remove = current_dtypes[rf]
            # print(rf, to_remove)
            bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'warning',
                                        'msg': 'Ya no existe el campo "{}" en el nodo "{}", se elimina de sus dtypes'.format(rf, node_name), 'exception': ''})
            del current_dtypes[rf]

        # print('\ncurrent_dtypes (modified):')
        # print(current_dtypes)
        return current_dtypes
        """

    def remove_flow_from_cache(self, flow_id: str):
        """DEPRECATED"""
        import gc

        from vtarget.handlers.cache_handler import cache_handler

        if flow_id in cache_handler.settings:
            print("remove_flow_from_cache")
            del cache_handler.settings[flow_id]
        gc.collect()

    def remove_nodes_from_cache(self, flow_id: str, node_keys: list[str]):
        import gc

        from vtarget.handlers.cache_handler import cache_handler

        removeds = []
        if flow_id in cache_handler.settings:
            for node_key in node_keys:
                if node_key in cache_handler.settings[flow_id]:
                    if node_key not in removeds:
                        removeds.append(node_key)
                    del cache_handler.settings[flow_id][node_key]
                    print("remove_nodes_from_cache")
        if flow_id in cache_handler.cache:
            for node_key in node_keys:
                if node_key in cache_handler.cache[flow_id]:
                    if node_key not in removeds:
                        removeds.append(node_key)
                    del cache_handler.cache[flow_id][node_key]

        gc.collect()
        return removeds

    # Actualiza node['meta']['ports_map']['pout'][port_name]['summary']
    def load_detailed_view(self, flow_id: str, node_key: str, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        # NOTE: No sé cuantas veces se ejecuta esta carga
        cache_handler.load(flow_id, node_key, port_name)
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.viz_summary(df)
        return {}

    # Actualiza node['meta']['ports_map']['pout'][port_name]['describe']
    def load_column_view(self, flow_id: str, node_key: str, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        # NOTE: No sé cuantas veces se ejecuta esta carga
        cache_handler.load(flow_id, node_key, port_name)
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.get_central_tendency_measures(df)
        return {}

    def modify_node(self, flow_id: str, node_key: str, node: dict, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        try:
            cache_handler.load(flow_id, node_key, port_name)
            if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
                cached_node = cache_handler.cache[flow_id][node_key]
                if "pout" in cached_node and port_name in cached_node["pout"]:
                    port_df = cached_node["pout"][port_name]
                    port_config = utilities.get_table_config(node["meta"], port_name)
                    head = utilities.get_head_of_df_as_list(port_df, port_config, flow_id, node_key, port_name)
                    node["meta"]["ports_map"]["pout"][port_name]["head"] = head
                else:
                    msg = app_message.dataprep["builder"]["exec_flow"]
                    return {
                        "flow_id": flow_id,
                        "node_key": node_key,
                        "node": node,
                        "success": False,
                        "error": msg,
                    }
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return {
                "flow_id": flow_id,
                "node_key": node_key,
                "node": node,
                "success": False,
                "error": str(e),
            }

        return {"flow_id": flow_id, "node_key": node_key, "node": node, "success": True}

    def run_node(self, flow_id: str, node_key: str, node: dict, links_to: list):
        import json
        from typing import Dict

        import pandas as pd

        from vtarget.handlers.bug_handler import bug_handler
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.handlers.event_handler import event_handler

        print("run node", node_key)

        # Resetea los bug
        bug_handler.bug = []

        # Incializa la caché para el nodo si es que aún no existe
        cache_handler.load_settings(flow_id)

        # Almancena los df del mapeo de los puertos de entrada
        input_port: Dict[str, pd.DataFrame] = {}

        # Cargar la cache de los padres en los puertos de entrada del nodo
        for ld in links_to:
            if "_chart" in ld["to"]:
                continue
            parent_port = ld["frompid"]
            parent_key = ld["from"]
            node_port = ld["topid"]

            cache_handler.load(flow_id, parent_key, parent_port)  # carga la cache del padre
            parent_cache = cache_handler.cache[flow_id][parent_key] if flow_id in cache_handler.cache and parent_key in cache_handler.cache[flow_id] else dict()

            if parent_cache and "pout" in parent_cache and parent_port in parent_cache["pout"]:
                input_port[node_port] = parent_cache["pout"][parent_port]  # actualiza pin del nodo con la salida correspondiente del padre

        node = self.pipeline.exec(flow_id, node, input_port)

        # Valida si la ejecucion del nodo tuvo algun error
        has_error = (
            next(
                (x for x in bug_handler.bug if x["node_key"] == node_key and x["level"] == "error"),
                None,
            )
            != None
        )
        node["meta"]["skipped"] = False
        node["meta"]["processed"] = True
        node["meta"]["has_error"] = has_error

        event_handler.emit_queue.put(
            {
                "name": "dataprep.node_processed",
                "data": {
                    "flow_id": flow_id,
                    "key": node_key,
                    "node": json.dumps(node, default=str),
                },
            }
        )

        if has_error:
            cache_handler.delete_node(flow_id, node_key)

        # TODO: deberia guardarse el resultado en cache
        cache_handler.dump_settings(flow_id)

        return {
            "flow_id": flow_id,
            "key": node_key,
            "node": json.dumps(node, default=str),
        }


if __name__ == "__main__":
    b = Builder()
    m = b.load_model()
    print(m)
