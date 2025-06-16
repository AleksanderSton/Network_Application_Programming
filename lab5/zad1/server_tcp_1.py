import socket
import random

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2912

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"Serwer nasłuchuje na {SERVER_IP}:{SERVER_PORT}")

    secret_number = random.randint(1, 100)
    print(f"Wylosowana liczba: {secret_number}")

    while True:
        conn, addr = server.accept()
        with conn:
            print(f"Połączenie od {addr}")

            data = conn.recv(1024).decode()
            if not data:
                continue

            try:
                guess = int(data)
                if guess < secret_number:
                    response = "mniejsza od wylosowanej przez serwer"
                elif guess > secret_number:
                    response = "większa od wylosowanej przez serwer"
                else:
                    response = "równa wylosowanej przez serwer"
                    conn.sendall(response.encode())
                    print("Serwer zamyka się...")
                    break

            except ValueError:
                response = "Niepoprawny format liczby. Podaj liczbę całkowitą."

            conn.sendall(response.encode())
