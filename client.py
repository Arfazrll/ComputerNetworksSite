import socket
import sys

def http_client(server_host, server_port, filename):
    """Client HTTP sederhana yang mengirim request GET."""
    try:
        # Buat socket TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Tambahkan timeout untuk menghindari hang
        client_socket.settimeout(10)
        
        # Hubungkan ke server
        print(f"[*] Menghubungkan ke server {server_host}:{server_port}...")
        client_socket.connect((server_host, server_port))
        
        # Pastikan filename dimulai dengan /
        if not filename.startswith('/'):
            filename = '/' + filename
        
        # Buat request HTTP GET
        request = f"GET {filename} HTTP/1.1\r\n"
        request += f"Host: {server_host}:{server_port}\r\n"
        request += "Connection: close\r\n\r\n"
        
        # Kirim request
        print(f"[*] Mengirim request: GET {filename}")
        client_socket.sendall(request.encode('utf-8'))
        
        # Terima respons
        print("[*] Menunggu respons...")
        
        # Buffer untuk menyimpan respons
        response = b""
        
        # Terima data chunk by chunk
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                print("[!] Timeout saat menerima data")
                break
        
        # Tutup socket
        client_socket.close()
        
        # Pisahkan header dan body
        try:
            # Cari pemisah header dan body (baris kosong \r\n\r\n)
            header_end = response.find(b"\r\n\r\n")
            
            if header_end != -1:
                # Ekstrak dan decode header
                headers = response[:header_end].decode('utf-8')
                
                # Ekstrak body (data setelah \r\n\r\n)
                body = response[header_end + 4:]
                
                # Tampilkan headers
                print("\n===== RESPONSE HEADERS =====")
                print(headers)
                
                # Cek status code
                status_line = headers.split('\r\n')[0]
                status_parts = status_line.split(' ')
                
                if len(status_parts) >= 2:
                    status_code = status_parts[1]
                    print(f"\n[*] Status: {status_line}")
                    
                    # Jika status code adalah 200 OK
                    if status_code == "200":
                        # Deteksi jenis konten
                        content_type = "text/plain"  # default
                        for line in headers.split('\r\n'):
                            if line.lower().startswith("content-type:"):
                                content_type = line.split(':', 1)[1].strip()
                                break
                        
                        # Tampilkan body berdasarkan jenis konten
                        print("\n===== RESPONSE BODY =====")
                        
                        # Jika konten adalah teks
                        if content_type.startswith(("text/", "application/json", "application/javascript")):
                            try:
                                print(body.decode('utf-8'))
                            except UnicodeDecodeError:
                                print("[!] Tidak dapat menampilkan body (binary content)")
                                print(f"[*] Ukuran body: {len(body)} bytes")
                        else:
                            print(f"[*] Body berisi data {content_type}")
                            print(f"[*] Ukuran: {len(body)} bytes")
                            print("[*] (Data biner tidak ditampilkan)")
                    
                    # Jika status code 404 Not Found
                    elif status_code == "404":
                        print("\n===== ERROR MESSAGE =====")
                        # Tambahkan pesan khusus untuk 404
                        print("[!] Halaman tidak ditemukan (404)")
                        print("[*] Server mengirimkan halaman error kustom (404.html)")
                        print("[*] Ukuran body: {len(body)} bytes")
                        print("[*] Buka browser dan akses URL yang sama untuk melihat halaman error yang lebih interaktif")
                    
                    # Jika status code lainnya
                    else:
                        # Coba tampilkan pesan error jika ada
                        try:
                            print("\n===== ERROR MESSAGE =====")
                            print(body.decode('utf-8'))
                        except UnicodeDecodeError:
                            print(f"[*] Respons body: {len(body)} bytes (binary content)")
                
                else:
                    print("[!] Format status line tidak valid")
            
            else:
                print("[!] Tidak dapat menemukan pemisah header dan body")
                print(f"[*] Raw response ({len(response)} bytes):")
                print(response)
        
        except Exception as e:
            print(f"[!] Error saat memproses respons: {e}")
            print(f"[*] Raw response ({len(response)} bytes received)")
    
    except socket.error as e:
        print(f"[!] Socket error: {e}")
    except Exception as e:
        print(f"[!] Error: {e}")

def main():
    """Fungsi utama untuk menjalankan client."""
    # Cek argumen command line
    if len(sys.argv) != 4:
        print("Penggunaan: python client.py server_host server_port filename")
        print("Contoh: python client.py localhost 6789 page.html")
        sys.exit(1)
    
    # Parse argumen
    server_host = sys.argv[1]
    
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print(f"[!] Port tidak valid: {sys.argv[2]}")
        sys.exit(1)
    
    filename = sys.argv[3]
    
    # Jalankan client
    http_client(server_host, server_port, filename)

if __name__ == "__main__":
    main()