import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
print("Server connected")

while True:
    data = input("Type text: ")
    if data == "exit": break
    sock.send(data.encode('utf-8'))
    print("Data sent " + str(data.encode('utf-8')))
    receive_data = sock.recv(1024)
    print("Data received " + str(receive_data))
    print(receive_data.decode('utf-8'))

sock.close()
print("Server disconnected")
