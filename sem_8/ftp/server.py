import socket
from threading import Thread

from crypt import PublicKey, PrivateKey, Message
from file_manager import manager
from exchange import *


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


def secure_listen(port: int, private: PrivateKey, public: PublicKey, client_public: PublicKey):
    secure_sock = create_sock(port)
    conn, addr = secure_sock.accept()
    is_connected = True
    while is_connected:
        out_msg = Message((manager.pwd() + "$ ").encode())
        out_msg.encrypt(client_public)
        conn.send(out_msg.get_bytes())
        in_msg = Message.parse_bytes(conn.recv(1024))
        in_msg.decrypt(private, public)
        command = in_msg.data.decode()
        cmd = manager.split(command)
        if cmd["cmd"] == "send":
            receive_file(conn, commands.get_file(cmd["args"][0], check_exist=False))
        elif cmd["cmd"] == "receive":
            send_file(conn, commands.get_file(cmd["args"][0], check_exist=False))
        else:
            print(command)
            output = manager.execute(command)
            if output is None: output = " "
            out_msg = Message(output.encode())
            out_msg.encrypt(client_public)
            conn.send(out_msg.get_bytes())
    conn.close()


def init_listen(conn: socket.socket, private: PrivateKey, public: PublicKey, port_gen):
    PORT = next(port_gen)
    client_public = PublicKey.parse_bytes(conn.recv(1024))
    conn.send(public.get_bytes())
    conn.send(str(PORT).encode())
    conn.detach()
    Thread(target=secure_listen, args=[PORT, private, public, client_public]).start()


if __name__ =="__main__":
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


