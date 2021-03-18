import socket
from threading import Thread
from file_manager import manager
from exchange import *


def socket_listen(conn, addr):
    try:
        while True:
            send(conn, manager.pwd() + "$ ")
            command = receive(conn)
            cmd = manager.split(command)
            if cmd["cmd"] == "send":
                receive_file(conn, commands.get_file(cmd["args"][0], check_exist=False))
            elif cmd["cmd"] == "receive":
                send_file(conn, commands.get_file(cmd["args"][0], check_exist=False))
            else:
                output = manager.execute(command)
                if output is None:
                    send(conn, " ")
                else:
                    send(conn, output)
    except ConnectionAbortedError:
        pass


if __name__ == "__main__":
    threads = dict()
    PORT = 8080
    sock = socket.socket()
    sock.bind(("", PORT))
    sock.listen(10)

    while True:
        conn, addr = sock.accept()
        thread = Thread(target=socket_listen, args=[conn, addr])
        threads[addr[1]] = thread
        thread.start()


