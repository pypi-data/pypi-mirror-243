import jinja2


class HTTPResponse:
    def __init__(self, html: str = "", status: int = 200):
        self.html = html
        self.status = status
        self.extraHeaders = []

    def setStatus(self, status: int):
        self.status = status

    def setHTML(self, html: str):
        self.html = html

    def setCookies(self, key: str, value: str) -> None:
        self.extraHeaders.append(("Set-cookie", f"{key}={value}"))

    @staticmethod
    def load_template(template_name: str, **kwargs):
        with open(template_name, 'r') as f:
            environment = jinja2.Environment()
            template = environment.from_string(f.read())
            return HTTPResponse(template.render(**kwargs))
