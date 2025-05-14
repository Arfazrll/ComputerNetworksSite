import socket
import threading
import os
import time
import sys
from datetime import datetime

# Konfigurasi Server
SERVER_HOST = '0.0.0.0'  # Terima koneksi dari semua interface
SERVER_PORT = 6789       # Port default sesuai contoh dalam spesifikasi
BUFFER_SIZE = 4096       # Ukuran buffer untuk menerima data

# Definisi jenis MIME untuk berbagai jenis file
MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml'
}

class WebServer:
    def __init__(self, host, port):
        """Inisialisasi server dengan host dan port."""
        self.host = host
        self.port = port
        # Buat socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Opsi untuk menggunakan kembali alamat/port
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Binding socket ke host dan port
        self.server_socket.bind((self.host, self.port))
        # Flag untuk menentukan apakah server sedang berjalan
        self.running = False

    def start(self):
        """Memulai server dan menerima koneksi."""
        # Mulai mendengarkan koneksi
        self.server_socket.listen(5)
        self.running = True
        print(f"[*] Server berjalan di http://{self.host if self.host != '0.0.0.0' else 'localhost'}:{self.port}")
        
        try:
            # Loop utama server
            while self.running:
                try:
                    # Menerima koneksi dari client
                    client_socket, client_address = self.server_socket.accept()
                    print(f"[*] Koneksi diterima dari {client_address[0]}:{client_address[1]}")
                    
                    # Buat thread baru untuk menangani request
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except Exception as e:
                    print(f"[!] Error saat menerima koneksi: {e}")
        
        except KeyboardInterrupt:
            # Menangani penghentian server dengan Ctrl+C
            print("\n[*] Server dihentikan oleh pengguna")
        
        finally:
            # Pastikan socket server ditutup
            self.stop()

    def stop(self):
        """Menghentikan server."""
        self.running = False
        self.server_socket.close()
        print("[*] Server berhenti")

    def handle_client(self, client_socket, address):
        """Menangani request dari client dalam thread terpisah."""
        try:
            # Terima data dari client
            request_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            
            # Jika tidak ada data, tutup koneksi
            if not request_data:
                client_socket.close()
                return
            
            # Parse request HTTP
            method, path, version, headers = self.parse_request(request_data)
            
            # Hanya mendukung metode GET
            if method != "GET":
                self.send_response(client_socket, 501, "Not Implemented", 
                                  "Metode HTTP tidak didukung.")
                return
            
            # Jika path adalah root, gunakan page.html sebagai default
            if path == "/" or path == "":
                path = "/page.html"
            
            # Hapus query string jika ada
            if "?" in path:
                path = path.split("?")[0]
            
            # Ubah path menjadi path lokal
            file_path = os.path.join(os.getcwd(), path[1:])
            
            # Cek apakah file ada
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                # Gunakan halaman 404.html kustom
                self.send_404_page(client_socket)
                return
            
            # Tentukan jenis MIME berdasarkan ekstensi file
            file_extension = os.path.splitext(file_path)[1].lower()
            content_type = MIME_TYPES.get(file_extension, 'application/octet-stream')
            
            # Baca file dan kirim sebagai respons
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                self.send_response(client_socket, 200, "OK", content, content_type, is_binary=True)
            except Exception as e:
                print(f"[!] Error saat membaca file {file_path}: {e}")
                self.send_response(client_socket, 500, "Internal Server Error", 
                                  "<h1>500 Internal Server Error</h1><p>Terjadi kesalahan saat membaca file.</p>")
        
        except Exception as e:
            print(f"[!] Error saat menangani request dari {address}: {e}")
        
        finally:
            # Pastikan socket client ditutup
            client_socket.close()

    def parse_request(self, request_data):
        """Parse HTTP request."""
        # Pisahkan baris-baris request
        lines = request_data.split('\r\n')
        # Ambil baris pertama (request line)
        request_line = lines[0].split()
        
        # Jika request line tidak valid
        if len(request_line) < 3:
            return "INVALID", "/", "HTTP/1.1", {}
        
        # Parse method, path, dan HTTP version
        method, path, version = request_line
        
        # Parse headers
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        
        return method, path, version, headers

    def send_404_page(self, client_socket):
        """Mengirim halaman 404 kustom."""
        try:
            # Cek jika halaman 404 kustom ada
            custom_404_path = os.path.join(os.getcwd(), "404.html")
            
            if os.path.exists(custom_404_path) and os.path.isfile(custom_404_path):
                # Gunakan halaman 404 kustom
                with open(custom_404_path, 'rb') as file:
                    content = file.read()
                self.send_response(client_socket, 404, "Not Found", content, 'text/html', is_binary=True)
            else:
                # Jika halaman 404 kustom tidak ada, gunakan fallback
                fallback_404 = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>404 Not Found</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                        h1 { color: #333; }
                        p { color: #666; }
                    </style>
                </head>
                <body>
                    <h1>404 Not Found</h1>
                    <p>File yang diminta tidak ditemukan.</p>
                    <p><a href="/">Kembali ke Beranda</a></p>
                </body>
                </html>
                """
                self.send_response(client_socket, 404, "Not Found", fallback_404)
                
        except Exception as e:
            print(f"[!] Error saat mengirim halaman 404: {e}")
            # Fallback paling sederhana jika terjadi error
            self.send_response(client_socket, 404, "Not Found", "<h1>404 Not Found</h1><p>File yang diminta tidak ditemukan.</p>")

    def send_response(self, client_socket, status_code, status_text, content, 
                      content_type='text/html', is_binary=False):
        """Mengirim HTTP response ke client."""
        # Konversi content menjadi bytes jika perlu
        if not is_binary and isinstance(content, str):
            content = content.encode('utf-8')
        
        # Buat header response
        current_time = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        headers = [
            f"HTTP/1.1 {status_code} {status_text}",
            f"Date: {current_time}",
            "Server: Python-SocketServer",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(content)}",
            "Connection: close"
        ]
        
        # Gabungkan headers dan akhiri dengan baris kosong
        response_headers = "\r\n".join(headers) + "\r\n\r\n"
        
        # Kirim headers
        client_socket.sendall(response_headers.encode('utf-8'))
        
        # Kirim content
        client_socket.sendall(content)

def main():
    """Fungsi utama untuk menjalankan server."""
    # Default port 6789 sesuai spesifikasi
    port = SERVER_PORT
    
    # Jika ada argumen command line untuk port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"[!] Port tidak valid: {sys.argv[1]}")
            print(f"[*] Menggunakan port default: {SERVER_PORT}")
            port = SERVER_PORT
    
    # Buat dan jalankan server
    server = WebServer(SERVER_HOST, port)
    server.start()

if __name__ == "__main__":
    main()