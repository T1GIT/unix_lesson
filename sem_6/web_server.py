import socket
from threading import Thread
import logging
from urllib3.response import HTTPResponse

import requests

from config import HOST, PORT, ENC, POOL
from controller import PageNotFoundException, MethodNotAllowedException, Controller
from request import Response, Request, EmptyRequest

logger = logging.getLogger("controllerLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("request.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)


def init_connection() -> socket.socket:
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(POOL)
    return sock


def process_request(conn: socket.socket, addr: tuple):
    try:
        req = Request.receive(conn)
        res = Response()
        try:
            controller.request(req, res)
        except FileNotFoundError:
            res.code, res.status = 404, "NOT FOUND"
        except PageNotFoundException:
            res.code, res.status = 404, "NOT FOUND"
        except MethodNotAllowedException:
            res.code, res.status = 405, "METHOD NOT ALLOWED"
        logger.info(f"{addr} {req.url} {res.code}")
        res.send(conn)
        conn.close()
    except EmptyRequest:
        pass


if __name__ == '__main__':
    sock = init_connection()
    controller = Controller()

    @controller.mapping("/")
    def root_mapping(req: Request, res: Response):
        res.code = 301
        res.headers["Location"] = "/public/index.html"
        res.headers["Connection"] = "keep-alive"

    while True:
        conn, addr = sock.accept()
        Thread(target=process_request, args=[conn, addr]).start()
