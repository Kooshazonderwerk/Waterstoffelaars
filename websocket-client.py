#pip install time
import time
#pip install socket
import socket


while True:
    time.sleep(1)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    message = 'random'.encode()
    #change to your server ip address
    addr = ("192.168.0.111", 12000)

    start = time.time()
    client_socket.sendto(message, addr)
    try:
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        #{data}
        print(f' {elapsed}')
    except socket.timeout:
        print('REQUEST TIMED OUT')
