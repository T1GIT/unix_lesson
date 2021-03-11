import socket

PORT = 8080
sock = socket.socket()
sock.connect(("localhost", PORT))

while True:
    data = input("Type text: ")
    sock.send(data.encode('utf-8'))
    receive_data = sock.recv(1024)
    print(receive_data.decode('utf-8'))
