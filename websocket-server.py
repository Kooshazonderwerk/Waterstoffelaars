# pip install random
import random
# pip install socket
import socket
# pip install time
import time
# pip install json
import json

from flask import jsonify

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# leeg = localhost
server_socket.bind(('', 12000))

while True:
    # kiest een willekeurige nummer tussen 0 en 1 met 8 decimalen
    rand = round(random.uniform(0, 1), 8)

    message, address = server_socket.recvfrom(1024)
    print(address)

    response = json.dumps(
        {
            'value': rand,
        }, default=str)

    if rand >= 0:
        server_socket.sendto(response.encode(), address)
