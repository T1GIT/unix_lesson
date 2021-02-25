import errno
import socket
import logging


def get_logger():
    logger = logging.getLogger("server")
    logger.setLevel(logging.INFO)
    file_hanlder = logging.FileHandler("server.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_hanlder.setFormatter(formatter)
    logger.addHandler(file_hanlder)
    return logger


def normalise_port(sock, port):
    while port < 65535:
        if port > 65535:
            raise AssertionError("All ports are in used")
        try:
            sock.bind(("", int(port)))
            break
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                port += 1
    if port == 65535:
        raise AssertionError("All ports are in used")
    else:
        return port


users = dict()
logger = get_logger()

sock = socket.socket()
logger.info("Server started")

while True:
    port = input("Type port: ")
    if port == "": port = 8080
    if port.isdigit() and 0 < int(port) < 65535:
        break
    else:
        print("Incorrect port number")

normalise_port(sock, int(port))

is_running = True

while is_running:
    sock.listen(10)
    logger.info("Server is listening on port " + str(port))
    conn, addr = sock.accept()
    logger.info("Client connected " + str(addr))
    is_connected = True

    user_port = addr[1]
    if user_port in users:
        conn.send("Hello, " + users[user_port])
    else:
        name = conn.recv(1024).decode('utf-8')
        users.update({addr[1], name})

    while is_connected:
        data = conn.recv(1024)
        if not data:
            break
        logger.info("Data received " + str(data))
        if data.decode('utf-8') == "close":
            is_running = False
            is_connected = False
        elif data.decode('utf-8') == "exit":
            is_connected = False
        conn.send(data.decode("utf-8").upper().encode("utf-8"))
        logger.info("Data sent " + str(data.decode("utf-8").upper().encode("utf-8")))

    logger.info("Client disconnected")
    sock.close()
    logger.info("Socket was closed")

logger.info("Server is shutting down")





