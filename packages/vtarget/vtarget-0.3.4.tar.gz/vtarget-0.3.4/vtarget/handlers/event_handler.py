import json
import queue
import sys
import threading
import traceback


class EventHandler(threading.Thread):
    def __init__(self):
        super().__init__()
        self.emit_queue = queue.Queue()
        self.__event_callback = None
        self.daemon = True
        self.start()

    def on_event(self, callback):
        self.__event_callback = callback

    def event_callback(self, payload):
        if self.__event_callback is not None:
            self.__event_callback(payload)

    def log(self, *args, **kwargs):
        print("[event-handler]", *args, **kwargs)

    def run(self):
        self.log("iniciando hilo envio de eventos")
        self.running = True
        while self.running:
            try:
                payload = self.emit_queue.get(timeout=1)
                # self.log(payload["name"], len(json.dumps(payload)), "bytes") # NOTE: Descomentar para depurar
                self.event_callback(payload)
            except:
                c, e, t = sys.exc_info()
                if c is not queue.Empty:
                    error = f"{c.__name__}: {e}"
                    tb = [f"{s.filename}:{s.lineno}" for s in traceback.extract_tb(t)]
                    self.log(error)
                    for line in tb:
                        self.log(line)

    def stop(self):
        self.log("stopping...")
        self.running = False
        self.join()
        self.log("stopped")


event_handler = EventHandler()
