import socket

sock = socket.socket()
print("Server is created")
sock.bind(('', 9090))
sock.listen(1)
print("Server is listening on port 9090")
conn, addr = sock.accept()
print("Client connected " + str(addr))

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Data received " + str(data))
    conn.send(data.decode("utf-8").upper().encode("utf-8"))
    print("Data sent " + str(data.decode("utf-8").upper().encode("utf-8")))

print("Client disconnected")
sock.close()
print("Socket was closed")
