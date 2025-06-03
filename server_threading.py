import socket
import threading
import os
import sys
from datetime import datetime

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 1009
BUFFER_SIZE = 4096

MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif'
}

class WebServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.running = False

    def start(self):
        self.server_socket.listen(5)
        self.running = True
        print(f"[*] Server berjalan di http://localhost:{self.port}")
        
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        self.server_socket.close()

    def handle_client(self, client_socket, address):
        try:
            request_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not request_data:
                return
            
            method, path, _, _ = self.parse_request(request_data)
            
            if method != "GET":
                self.send_response(client_socket, 501, "Not Implemented", "Metode HTTP tidak didukung.")
                return
            
            if path == "/" or path == "":
                path = "/page.html"
            
            if "?" in path:
                path = path.split("?")[0]
            
            file_path = os.path.join(os.getcwd(), path[1:])
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_404_page(client_socket)
                return
            
            file_extension = os.path.splitext(file_path)[1].lower()
            content_type = MIME_TYPES.get(file_extension, 'application/octet-stream')
            
            with open(file_path, 'rb') as file:
                content = file.read()
            self.send_response(client_socket, 200, "OK", content, content_type, is_binary=True)
        
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client_socket.close()

    def parse_request(self, request_data):
        lines = request_data.split('\r\n')
        request_line = lines[0].split()
        
        if len(request_line) < 3:
            return "INVALID", "/", "HTTP/1.1", {}
        
        method, path, version = request_line
        
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        
        return method, path, version, headers

    def send_404_page(self, client_socket):
        custom_404_path = os.path.join(os.getcwd(), "404.html")
        
        if os.path.exists(custom_404_path):
            with open(custom_404_path, 'rb') as file:
                content = file.read()
            self.send_response(client_socket, 404, "Not Found", content, 'text/html', is_binary=True)
        else:
            content = "<h1>404 Not Found</h1><p>File tidak ditemukan.</p>"
            self.send_response(client_socket, 404, "Not Found", content)

    def send_response(self, client_socket, status_code, status_text, content, 
                      content_type='text/html', is_binary=False):
        if not is_binary and isinstance(content, str):
            content = content.encode('utf-8')
        
        headers = [
            f"HTTP/1.1 {status_code} {status_text}",
            f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
            "Server: Python-SocketServer",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(content)}",
            "Connection: close"
        ]
        
        response_headers = "\r\n".join(headers) + "\r\n\r\n"
        client_socket.sendall(response_headers.encode('utf-8'))
        client_socket.sendall(content)

def main():
    port = SERVER_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = SERVER_PORT

    server = WebServer(SERVER_HOST, port)
    server.start()

if __name__ == "__main__":
    main()
