from socket import *

def handle_request(data):
    try:
        segments = data.split()
        if len(segments) != 3:
            return "630 -1"
        
        oc, num1, num2 = segments
        if oc not in ['+', '-', '*', '/']:
            return "630 -1"
        num1 = int(num1)
        num2 = int(num2)

        if oc == '/' and num2 == 0:
            return "631 -1"
        
        if oc == '+':
            res = num1 + num2
        elif oc == '-':
            res = num1 - num2
        elif oc == '*':
            res = num1 * num2
        elif oc == '/':
            res = num1 / num2
        
        return f"200 {res}"
    except ValueError:
        return "630 -1"

server_port = 54321
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The server is ready to receive on port ', server_port)
while True:
    try: 
        client_socket, addr = server_socket.accept()

        data = client_socket.recv(1024).decode()
        response = handle_request(data)
        client_socket.send(response.encode())
        client_socket.close()
    except KeyboardInterrupt:
        server_socket.close()
        break