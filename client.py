import socket
import sys

def http_client(server_host, server_port, filename):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        client_socket.connect((server_host, server_port))
        
        if not filename.startswith('/'):
            filename = '/' + filename
        
        request = f"GET {filename} HTTP/1.1\r\n"
        request += f"Host: {server_host}:{server_port}\r\n"
        request += "Connection: close\r\n\r\n"
        
        client_socket.sendall(request.encode('utf-8'))
        
        response = b""
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                break
        
        client_socket.close()
        
        header_end = response.find(b"\r\n\r\n")
        if header_end != -1:
            headers = response[:header_end].decode('utf-8')
            body = response[header_end + 4:]
            
            print(headers)
            print("\n")
            
            try:
                print(body.decode('utf-8'))
            except UnicodeDecodeError:
                print(f"Body: {len(body)} bytes (binary content)")
                
    except socket.error as e:
        print(f"Socket error: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)
    
    server_host = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print(f"Port tidak valid: {sys.argv[2]}")
        sys.exit(1)
    
    filename = sys.argv[3]
    http_client(server_host, server_port, filename)

if __name__ == "__main__":
    main()