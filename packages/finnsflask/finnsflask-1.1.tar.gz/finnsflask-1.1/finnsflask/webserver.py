from http import server
from typing import Callable

from .httprequest import HTTPRequest
from .httpresponse import HTTPResponse


class WebServerClass:
    class WebServer(server.BaseHTTPRequestHandler):
        paths = {}

        @classmethod
        def addPath(cls, path: str, func: Callable):
            cls.paths[path] = func

        def do_GET(self):
            if self.path not in self.paths:
                self.send_response(404)
                return
            rv: HTTPResponse = self.paths[self.path](HTTPRequest(self))
            self.send_response(rv.status)
            self.send_header('Content-type', 'text/html')
            for header in rv.extraHeaders:
                self.send_header(header[0], header[1])
            self.end_headers()
            for line in rv.html.split('\n'):
                self.wfile.write(bytes(line, 'utf-8'))
