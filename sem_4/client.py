import socket
from file_manager import manager
from exchange import *

PORT = 8080
sock = socket.socket()
sock.connect(("localhost", PORT))


while True:
    label = receive(sock)
    command = input(label)
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
        send(sock, command)
        output = receive(sock)
        if output != " ":
            print(output)
