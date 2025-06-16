import socket
import time

HOST = '127.0.0.1'
PORT = 65432
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Serwer TCP nasłuchuje na {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Połączono z {addr}")
            start_time = time.time()
            data_received = 0
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data_received += len(data)
            end_time = time.time()
            print(f"Odebrano {data_received} bajtów od klienta TCP.")
            print(f"Całkowity czas odbioru TCP: {end_time - start_time:.6f} sekund.")
            conn.sendall(b"ACK_TCP")