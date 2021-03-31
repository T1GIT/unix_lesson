import socket

sock = socket.socket()
print("Socket created")

while True:
    host = input("Type host: ")
    if host == "": host = "localhost"

    while True:
        port = input("Type port: ")
        if port == "":
            port = 8080
            break
        elif port.isdigit() and 0 < int(port) < 65535:
            port = int(port)
            break
        else:
            print("Incorrect port number")

    try:
        sock.connect((host, int(port)))
        print("Server connected")
        break
    except socket.gaierror:
        print("Something went wrong")

is_running = True

init = sock.recv(1024)
if init == b"NONE":
    sock.send(input("Input name: ").encode("utf-8"))
else:
    print(init.decode("utf-8"))

while is_running:
    data = input("Type text: ")
    if data == "exit": is_running = False
    sock.send(data.encode('utf-8'))
    print("Data sent " + str(data.encode('utf-8')))
    receive_data = sock.recv(1024)
    print("Data received " + str(receive_data))
    print(receive_data.decode('utf-8'))

sock.close()
print("Server disconnected")
