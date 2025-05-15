import socket
import threading
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 1009

MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png'
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
        print(f"Server berjalan di port {self.port}")
        
        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                client_socket.close()
                return
            
            method, path, _ = self.parse_request(request_data)
            
            if method != "GET":
                self.send_response(client_socket, 501, "Not Implemented", 
                                  "Method HTTP tidak didukung.")
                return
            
            if path == "/" or path == "":
                path = "/index.html"
            
            file_path = os.path.join(os.getcwd(), path[1:])
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_404(client_socket)
                return
            
            file_extension = os.path.splitext(file_path)[1].lower()
            content_type = MIME_TYPES.get(file_extension, 'application/octet-stream')
            
            with open(file_path, 'rb') as file:
                content = file.read()
            self.send_response(client_socket, 200, "OK", content, content_type)
            
        except Exception:
            pass
        finally:
            client_socket.close()

    def parse_request(self, request_data):
        lines = request_data.split('\r\n')
        request_line = lines[0].split()
        
        if len(request_line) < 3:
            return "INVALID", "/", "HTTP/1.1"
        
        return request_line[0], request_line[1], request_line[2]

    def send_404(self, client_socket):
        try:
            custom_404 = os.path.join(os.getcwd(), "404.html")
            if os.path.exists(custom_404):
                with open(custom_404, 'rb') as file:
                    content = file.read()
                self.send_response(client_socket, 404, "Not Found", content, 'text/html')
            else:
                content = "<h1>404 Not Found</h1><p>File tidak ditemukan.</p>"
                self.send_response(client_socket, 404, "Not Found", content)
        except Exception:
            content = "<h1>404 Not Found</h1>"
            self.send_response(client_socket, 404, "Not Found", content)

    def send_response(self, client_socket, status_code, status_text, content, 
                      content_type='text/html'):
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        headers = f"HTTP/1.1 {status_code} {status_text}\r\n"
        headers += f"Content-Type: {content_type}\r\n"
        headers += f"Content-Length: {len(content)}\r\n"
        headers += "Connection: close\r\n\r\n"
        
        client_socket.sendall(headers.encode('utf-8'))
        client_socket.sendall(content)

def main():
    server = WebServer(SERVER_HOST, SERVER_PORT)
    server.start()

if __name__ == "__main__":
    main()