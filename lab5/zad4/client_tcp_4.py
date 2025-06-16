import socket
import time

HOST = '127.0.0.1'
PORT = 65432
MESSAGE_SIZE = 1024 * 1024 * 10
MESSAGE = b'A' * MESSAGE_SIZE

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        start_connect_time = time.time()
        s.connect((HOST, PORT))
        end_connect_time = time.time()
        print(f"Połączono z serwerem TCP w {end_connect_time - start_connect_time:.6f} sekund.")

        start_send_time = time.time()
        s.sendall(MESSAGE)
        end_send_time = time.time()
        print(f"Wysłano {MESSAGE_SIZE} bajtów do serwera TCP w {end_send_time - start_send_time:.6f} sekund.")

        # Odbiór potwierdzenia
        ack = s.recv(1024)
        print(f"Otrzymano potwierdzenie od serwera TCP: {ack.decode()}")