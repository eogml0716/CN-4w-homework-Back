import os
import socket

HOST = ''
PORT = 8080


def get_content_type(path):
    if path.endswith('.html'):
        return 'text/html'
    elif path.endswith('.css'):
        return 'text/css'
    elif path.endswith('.js'):
        return 'text/javascript'
    elif path.endswith('.jpg'):
        return 'image/jpeg'
    elif path.endswith('.png'):
        return 'image/png'
    else:
        return 'text/plain'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('HTTP server started on port', PORT)

    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(1500).decode('utf-8')
            method, path, protocol = request.split(' ')[0:3]

            if path == '/':
                path = 'main.html'

            path = f'.{path}'

            if not os.path.exists(path):
                header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                conn.sendall(header.encode('utf-8'))
            else:
                with open(path, 'rb') as f:
                    body = f.read()
                content_type = get_content_type(path)
                header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n\r\n'
                conn.sendall(header.encode('utf-8') + body)

        conn.close()
