from http import server
from typing import Callable

from .webserver import WebServerClass


class FinnsFlask:
    def __init__(self):
        self.ws = WebServerClass().WebServer

    def route(self, path: str):
        def route_inner(func: Callable):
            self.ws.addPath(path, func)
            return func
        return route_inner

    def listen(self, port=8000):
        webServer = server.HTTPServer(('127.0.0.1', port), self.ws)
        print("Server started http://%s:%s" % ('127.0.0.1', port))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
