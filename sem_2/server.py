import socket
from threading import Thread


def socket_listen(conn, addr):
    while True:
        is_connected = True
        while is_connected:
            data = conn.recv(1024)
            print(str(addr) + " " + data.decode('utf-8'))
            conn.send(data.decode("utf-8").upper().encode("utf-8"))

        sock.close()


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


