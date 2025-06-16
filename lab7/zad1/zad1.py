import telnetlib
import sys


def connect_pop3_telnet(server, port, username, password):

    try:
        tn = telnetlib.Telnet(server, port, timeout=10)

        response = tn.read_until(b"\r\n", timeout=5)
        print(f"Powitanie serwera: {response.decode('utf-8').strip()}")

        if not response.startswith(b"+OK"):
            print("Błąd: Serwer nie odpowiedział pozytywnie")
            return None

        tn.write(f"USER {username}\r\n".encode('utf-8'))
        response = tn.read_until(b"\r\n", timeout=5)
        print(f"Odpowiedź na USER: {response.decode('utf-8').strip()}")

        if not response.startswith(b"+OK"):
            print("Błąd: Nieprawidłowa nazwa użytkownika")
            return None

        tn.write(f"PASS {password}\r\n".encode('utf-8'))
        response = tn.read_until(b"\r\n", timeout=5)
        print(f"Odpowiedź na PASS: {response.decode('utf-8').strip()}")

        if not response.startswith(b"+OK"):
            print("Błąd: Nieprawidłowe hasło")
            return None

        tn.write(b"STAT\r\n")
        response = tn.read_until(b"\r\n", timeout=5)
        print(f"Odpowiedź na STAT: {response.decode('utf-8').strip()}")

        if response.startswith(b"+OK"):
            parts = response.decode('utf-8').split()
            if len(parts) >= 3:
                message_count = int(parts[1])
                mailbox_size = int(parts[2])
                print(f"Liczba wiadomości w skrzynce: {message_count}")
                print(f"Rozmiar skrzynki: {mailbox_size} bajtów")

                tn.write(b"QUIT\r\n")
                tn.read_until(b"\r\n", timeout=5)
                tn.close()

                return message_count

        return None

    except Exception as e:
        print(f"Błąd podczas połączenia: {e}")
        return None


if __name__ == "__main__":
    server = "poczta.interia.pl"
    port = 110
    username = input("Podaj nazwę użytkownika: ")
    password = input("Podaj hasło: ")

    print(f"Łączenie z serwerem {server}:{port}...")
    message_count = connect_pop3_telnet(server, port, username, password)

    if message_count is not None:
        print(f"\nWynik: W skrzynce znajduje się {message_count} wiadomości")
    else:
        print("\nNie udało się pobrać informacji o skrzynce")