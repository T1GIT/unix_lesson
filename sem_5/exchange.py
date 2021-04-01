import os
import commands

PACKET_SIZE = 1024


def receive(socket):
    return socket.recv(1024).decode('utf-8')


def send(socket, data):
    socket.send(data.encode('utf-8'))


def send_file(socket, file_path):
    try:
        if not os.path.exists(file_path):
            socket.send(b"NOT_FOUND")
            return "File not found"
        elif os.path.isdir(file_path):
            socket.send(b"NOT_FILE")
            return "Isn't a file"
        else:
            with open(file_path, mode="rb") as file:
                print(1)
                socket.send(b"READY")
                print(2)
                msg = socket.recv(PACKET_SIZE)
                print(msg)
                if msg == b"EXISTS":
                    return "File already exists"
                elif msg == b"READY":
                    print(1)
                    data = file.read(PACKET_SIZE)
                    print(data)
                    while data:
                        socket.send(data)
                        data = file.read(PACKET_SIZE)
                    socket.send(b"DONE")
    except commands.PassThrowRootException:
        socket.send(b"ROOT")


def receive_file(socket, file_path):
    msg = socket.recv(PACKET_SIZE)
    if msg == b"NOT_FOUND":
        return "File not found"
    elif msg == b"NOT_FILE":
        return "Isn't file"
    elif msg == b"ROOT":
        return "Can't across root directory"
    elif msg == b"READY":
        if os.path.exists(file_path) or os.path.isdir(file_path):
            socket.send(b"EXISTS")
            return "File already exists"
        else:
            print(1)
            with open(file_path, mode="wb") as file:
                print(2)
                socket.send(b"READY")
                print(3)
                data = socket.recv(PACKET_SIZE)
                print(data)
                while data != b"DONE":
                    file.write(data)
                    data = socket.recv(PACKET_SIZE)
