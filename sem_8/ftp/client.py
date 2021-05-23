import socket

from crypt import PrivateKey, PublicKey, Message
from file_manager import manager
from exchange import *


def get_server_key_and_port(sock: socket.socket, public: PublicKey):
    sock.send(public.get_bytes())
    server_public = PublicKey.parse_bytes(sock.recv(1024))
    port = int(sock.recv(1024).decode())
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
        out_msg = Message.parse_bytes(sock.recv(1024))
        out_msg.decrypt(private, public)
        command = input(out_msg.data.decode())
        cmd = manager.split(command)
        if cmd["cmd"] in ["send", "receive"]:
            send(sock, command)
            if len(cmd["args"]) == 0:
                print("Invalid argument")
            else:
                if cmd["cmd"] == "receive": output = receive_file(sock, cmd["args"][0])
                elif cmd["cmd"] == "send":  output = send_file(sock, cmd["args"][0])
                print(output)
        elif cmd["cmd"] == "exit":
            sock.close()
            exit()
        else:
            out_msg = Message(command.encode())
            out_msg.encrypt(server_public)
            sock.send(out_msg.get_bytes())
            in_msg = Message.parse_bytes(sock.recv(1024))
            in_msg.decrypt(private, public)
            output = in_msg.data.decode()
            if output != " ":
                print(output)
