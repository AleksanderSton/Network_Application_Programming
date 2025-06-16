import socket


# SERVER_IP = "212.182.24.27"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2912

while True:
    try:
        number = input("Podaj liczbę do odgadnięcia (lub 'exit' aby zakończyć): ")
        if number.lower() == 'exit':
            print("Zamykanie klienta...")
            break

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_IP, SERVER_PORT))

            sock.sendall(number.encode())
            response = sock.recv(1024).decode()
            print(f"Odpowiedź serwera: {response}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        break
