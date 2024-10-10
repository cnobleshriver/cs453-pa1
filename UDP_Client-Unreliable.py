from socket import *

file_name = 'input.txt'
server_name = 'localhost'
server_port = 54321

d = 0.1
max_timeout = 2.0

try:
    with open(file_name, 'r') as file:
        for i in range(7):
            line = file.readline().strip()
            if not line:
                break
            print(f"InputRequest: {line}")

            client_socket = socket(AF_INET, SOCK_DGRAM)
            client_socket.settimeout(d)

            while True:
                try:
                    client_socket.sendto(line.encode(), (server_name, server_port))

                    response, _ = client_socket.recvfrom(1024)
                    status_code, result = response.decode().split(maxsplit=1)

                    client_socket.settimeout(None)

                    if status_code == '200':
                        print(f"The result is: {result}")
                    else:
                        print(f"Error: {status_code}: {result}")
                    break
                except timeout:
                    d *= 2
                    if d > max_timeout:
                        status_code = '300'
                        print("Request timed out: the server is DEAD")
                        break
                    else:
                        print("Request timed out: resending")
                    continue
            
            client_socket.close()
except FileNotFoundError:
    print(f"Error: File {file_name} not found")
