import socket
from crypt import *


def get_server_key_and_port(sock: socket.socket, public: PublicKey):
    sock.send(public.get_bytes())
    server_public = PublicKey.parse_bytes(sock.recv(1024))
    port = int(sock.recv(1024).decode(ENCODING))
    sock.detach()
    return server_public, port


if __name__ == '__main__':
    private = PrivateKey.generate()
    public = PublicKey.generate(private)
    sock = socket.socket()
    sock.connect(("localhost", 8080))
    server_public, port = get_server_key_and_port(sock, public)
    sock = socket.socket()
    sock.connect(("localhost", port))
    while True:
        data = input("Type text to crypt: ")
        req_msg = Message(data.encode(ENCODING))
        req_msg.encrypt(server_public)
        sock.send(req_msg.get_bytes())
        res_msg = Message.parse_bytes(sock.recv(1024))
        res_msg.decrypt(private, public)
        print(res_msg.data.decode(ENCODING))
