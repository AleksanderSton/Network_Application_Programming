import socket

HOST = '127.0.0.1'
PORT = 2900
MAX_EXPECTED_LENGTH = 20


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Połączono z serwerem Echo (limit znaków) {HOST}:{PORT}")

            message = input(f"Wpisz wiadomość do wysłania (maks. {MAX_EXPECTED_LENGTH} znaków będzie przetworzone): ")

            s.sendall(message.encode('utf-8'))
            print(f"Klient: Wysłano do serwera: '{message}' (długość: {len(message)})")

            data = s.recv(1024)
            received_message = data.decode('utf-8')
            received_length = len(received_message)

            print(f"Klient: Odebrano od serwera echo: '{received_message}' (długość: {received_length})")

            if received_length <= MAX_EXPECTED_LENGTH:
                print(
                    f"Klient: Potwierdzono! Odebrana wiadomość ma oczekiwaną długość ({received_length} <= {MAX_EXPECTED_LENGTH} znaków).")
                if len(message) > MAX_EXPECTED_LENGTH:
                    if received_message == message[:MAX_EXPECTED_LENGTH]:
                        print("Klient: Wiadomość została poprawnie obcięta przez serwer.")
                    else:
                        print("Klient: UWAGA! Wiadomość została obcięta, ale nie do oczekiwanej wartości.")
            else:
                print(
                    f"Klient: BŁĄD! Odebrana wiadomość ({received_length} znaków) przekracza oczekiwaną maksymalną długość ({MAX_EXPECTED_LENGTH} znaków).")

        except ConnectionRefusedError:
            print(f"Błąd: Połączenie odrzucone. Upewnij się, że serwer działa na {HOST}:{PORT}.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")