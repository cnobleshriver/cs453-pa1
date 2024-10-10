from socket import *

file_name = 'input.txt'
server_name = 'localhost'
server_port = 54321

try:
    with open(file_name, 'r') as file:
        for i in range(7):
            line = file.readline().strip()
            if not line:
                break
            print(f"InputRequest: {line}")

            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((server_name, server_port))
            client_socket.send(line.encode())

            response = client_socket.recv(1024).decode()
            status_code, result = response.split(maxsplit=1)
            if status_code == '200':
                print(f"The result is: {result}")
            else:
                print(f"Error: {status_code}: {result}")
            
            client_socket.close()
except FileNotFoundError:
    print(f"Error: File {file_name} not found")
