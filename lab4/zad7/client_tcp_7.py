import socket

HOST = '127.0.0.1'
PORT = 2900

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Połączono z serwerem Echo (limit znaków) {HOST}:{PORT}")

            message = input("Wpisz wiadomość do wysłania (spróbuj dłuższą niż 20 znaków): ")
            s.sendall(message.encode('utf-8'))
            print(f"Wysłano do serwera: '{message}' (długość: {len(message)})")

            data = s.recv(1024)
            received_message = data.decode('utf-8')
            print(f"Odebrano od serwera echo: '{received_message}' (długość: {len(received_message)})")

        except ConnectionRefusedError:
            print(f"Błąd: Połączenie odrzucone. Upewnij się, że serwer działa na {HOST}:{PORT}.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")