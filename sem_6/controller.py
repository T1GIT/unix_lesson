import os
from datetime import datetime
from config import SEP, STATIC, ENC
from request import Request, Response

CONTENT_TYPE = {
    "text": {
        "html": "text/html; charset=utf-8", "css": "text/css", "js": "text/javascript",
    },
    "image": {
        "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif"
    }
}


class ControllerException(Exception):
    pass


class FileNotFoundException(ControllerException):
    pass


class PageNotFoundException(ControllerException):
    pass


class MethodNotAllowedException(ControllerException):
    pass


class RewriteMappingException(ControllerException):
    pass


class Controller:
    def __init__(self):
        self.static_dir = os.path.abspath(os.path.join(*STATIC.split("/")))
        self.map_dict: dict[str: dict[str: callable]] = dict()

    def mapping(self, path: str, method: str = "GET"):
        def wrap(func: callable):
            if path in self.map_dict:
                if method in self.map_dict:
                    raise RewriteMappingException()
                self.map_dict[path][method] = func
            self.map_dict[path] = {method: func}
            return func
        return wrap

    def request(self, req: Request, res: Response):
        res.headers["Date"] = datetime.now().strftime("%a, %d %b %Y %X GMT")
        res.headers["Server"] = "T1SERVER"
        res.headers["Connection"] = "close"
        if req.url in self.map_dict:
            if req.method in self.map_dict[req.url]:
                self.map_dict[req.url][req.method](req, res)
            else:
                raise MethodNotAllowedException()
        else:
            if req.url.startswith(STATIC) and req.method == "GET":
                self.send_static(req, res)
                res.headers["Content-Length"] = len(res.body)
            else:
                raise PageNotFoundException()

    def send_static(self, req: Request, res: Response):
        path = os.path.abspath(os.path.join(*req.url.split("/")))
        if (not path.startswith(self.static_dir)
                or not os.path.exists(path)
                or "." not in req.url):
            raise FileNotFoundException()
        ext = req.url[req.url.rfind(".") + 1:]
        if ext in CONTENT_TYPE["text"]:
            self.send_text(req, res, ext)
        elif ext in CONTENT_TYPE["image"]:
            self.send_binary(req, res, ext)
        else:
            res.code, res.status = 403, "DENIED FILE TYPE"

    @staticmethod
    def send_text(req: Request, res: Response, ext: str):
        with open(os.path.abspath(os.path.join(*req.url.split("/"))), "r", encoding=ENC) as file:
            res.body = SEP.join(file.readlines())
        res.headers["Content-Type"] = CONTENT_TYPE["text"][ext]

    @staticmethod
    def send_binary(req: Request, res: Response, ext: str):
        with open(os.path.abspath(os.path.join(*req.url.split("/"))), "rb") as file:
            res.body = "".join(map(lambda x: chr(x), file.read()))
        res.headers["Connection"] = "keep-alive"
        res.headers["Cache-Control"] = "max-age=315360000"
        res.headers["Accept-Ranges"] = "bytes"
        res.headers["Pragma"] = "public"
        res.headers["Content-Type"] = CONTENT_TYPE["image"][ext]

