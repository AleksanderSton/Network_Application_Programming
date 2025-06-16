import socket

HOST = '127.0.0.1'
PORT = 65432


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer Echo nasłuchuje na {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Połączono z {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Odebrano od klienta: {data.decode('utf-8')}")
                    conn.sendall(data)
                    print(f"Odesłano do klienta: {data.decode('utf-8')}")
            print(f"Rozłączono z {addr}")