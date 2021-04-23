from datetime import datetime
from socket import socket

from config import SEP, ENC


class EmptyRequest(Exception):
    pass


class Response:
    def __init__(self, protocol: str = "HTTP/1.1", code: int = 200, status: str = "OK", headers: dict = None,
                 body=None):
        self.headers = dict() if headers is None else headers
        self.protocol = protocol
        self.code = code
        self.status = status
        self.body = body

    def stringify(self) -> str:
        splited = list()
        splited.append(f"{self.protocol} {self.code} {self.status}")
        splited.extend(map(lambda item: f"{item[0]}: {item[1]}", self.headers.items()))
        splited.append("")
        if self.body is not None:
            splited.append(self.body)
        return SEP.join(splited)

    def send(self, conn: socket):
        conn.send(self.stringify().encode(ENC))


class Request:
    def __init__(self, method: str = "GET", url: str = "/", protocol: str = "HTTP/1.1", headers: dict = None,
                 params: dict = None, body: str = ""):
        self.headers = dict() if headers is None else headers
        self.params = dict() if params is None else params
        self.headers = headers
        self.method = method
        self.url = url
        self.protocol = protocol
        self.body = body

    @staticmethod
    def parse(req: str):
        splited = req.split(SEP)
        if splited == ['']:
            raise EmptyRequest()
        method, url, protocol = splited.pop(0).split()
        if "?" in url:
            url, paramsRow = url.split("?")
            params = {k: v for k, v in map(lambda row: row.split("=", 1), paramsRow.split("&"))}
        else:
            params = None
        body_sep = splited.index("")
        headers = {k: v for k, v in map(lambda row: row.split(": ", 1), splited[:body_sep])}
        body = SEP.join(splited[body_sep + 1:])
        return Request(method, url, protocol, headers, params, body)

    @staticmethod
    def receive(conn: socket):
        return Request.parse(conn.recv(8192).decode(ENC))
