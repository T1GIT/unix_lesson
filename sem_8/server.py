import socket
from threading import Thread
from crypt import *


def create_sock(port: int, conn_amount: int = 1) -> socket.socket:
    sock = socket.socket()
    sock.bind(("", port))
    sock.listen(conn_amount)
    return sock


def pool_gen(start: int = 8080):
    for port in range(start, 65536):
        yield port


def get_keys():
    if PublicKey.check_exist() and PrivateKey.check_exist():
        pri_k = PrivateKey.restore()
        pub_k = PublicKey.restore()
    else:
        pri_k = PrivateKey.generate()
        pub_k = PublicKey.generate(pri_k)
        pri_k.dump()
        pub_k.dump()
    return pri_k, pub_k


def secure_listen(port: int, private: PrivateKey, public: PublicKey, client_public: PublicKey):
    secure_sock = create_sock(port)
    conn, addr = secure_sock.accept()
    is_connected = True
    while is_connected:
        req_msg = Message.parse_bytes(conn.recv(1024))
        req_msg.decrypt(private, public)
        res_msg = Message(req_msg.data.decode(ENCODING).upper().encode(ENCODING))
        res_msg.encrypt(client_public)
        conn.send(res_msg.get_bytes())
    conn.close()


def init_listen(conn: socket.socket, private: PrivateKey, public: PublicKey, port_gen):
    PORT = next(port_gen)
    client_public = PublicKey.parse_bytes(conn.recv(1024))
    conn.send(public.get_bytes())
    conn.send(str(PORT).encode(ENCODING))
    conn.detach()
    Thread(target=secure_listen, args=[PORT, private, public, client_public]).start()


if __name__ == "__main__":
    private, public = get_keys()
    threads = dict()
    accepted_keys: set = set()
    port_gen = pool_gen()
    crypt_sock = create_sock(next(port_gen), 10)
    while True:
        conn, addr = crypt_sock.accept()
        thread = Thread(target=init_listen, args=[conn, private, public, port_gen])
        threads[addr[1]] = thread
        thread.start()


