from http import cookies


class HTTPRequest:
    def __init__(self, ws):
        self.ws = ws

    def getCookies(self) -> cookies.SimpleCookie:
        cookie_string = self.ws.headers.get("Cookie", "")
        return cookies.SimpleCookie(cookie_string)
