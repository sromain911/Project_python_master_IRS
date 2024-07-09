import socket
import json
import time

HOST = "localhost"
PORT = 8000

while True:
    message = f"Message {time.time()}"  # Message unique avec horodatage
    data = message.encode()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(data, (HOST, PORT))

    # Optionnel: Affichage du message envoyé dans la console du client
    print(f"Message envoyé: {message}")

    # Délai entre les envois (en secondes)
    time.sleep(2)
