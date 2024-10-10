import sys
import random
from socket import *

def handle_request(data):
    try:
        segments = data.split()
        if len(segments) != 3:
            return "630 -1"
        
        oc, num1, num2 = segments
        if oc not in ['+', '-', '*', '/']:
            return "620 -1"
        
        num1 = int(num1)
        num2 = int(num2)
        
        if oc == '/' and num2 == 0:
            return "630 -1"

        if oc == '+':
            result = num1 + num2
        elif oc == '-':
            result = num1 - num2
        elif oc == '*':
            result = num1 * num2
        elif oc == '/':
            result = num1 / num2
        
        return f"200 {result}"
    except ValueError:
        return "630 -1"

if len(sys.argv) != 3:
    print("Usage: python UDP_Server-Unreliable.py <probability> <seed>")
    sys.exit(1)

p = float(sys.argv[1])
random.seed(sys.argv[2])

server_port = 54321
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print(f'The server is ready to receive on port {server_port}')

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)
        received_line = data.decode().strip()

        if random.random() <= p:
            print(f"{received_line} -> dropped")
            continue

        response = handle_request(received_line)
        print(f"{received_line} -> {response}")
        server_socket.sendto(response.encode(), client_address)
except KeyboardInterrupt:
    server_socket.close()
