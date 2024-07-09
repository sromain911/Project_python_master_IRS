import socket
import json

HOST = "localhost"
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

while True:
    data, address = server.recvfrom(1024)
    message = data.decode()
    print(f"Message reçu de {address}: {message}")
