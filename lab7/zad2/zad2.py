import telnetlib
import sys


def check_mailbox_size_telnet(server, port, username, password):

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
                total_size = int(parts[2])

                print(f"Liczba wiadomości: {message_count}")
                print(f"Całkowity rozmiar skrzynki: {total_size} bajtów")

                if message_count > 0:
                    print("\nRozmiary poszczególnych wiadomości:")
                    tn.write(b"LIST\r\n")
                    response = tn.read_until(b"\r\n", timeout=5)

                    if response.startswith(b"+OK"):
                        messages_info = []
                        while True:
                            line = tn.read_until(b"\r\n", timeout=5)
                            if line.strip() == b".":
                                break
                            parts = line.decode('utf-8').strip().split()
                            if len(parts) >= 2:
                                msg_num = int(parts[0])
                                msg_size = int(parts[1])
                                messages_info.append((msg_num, msg_size))
                                print(f"  Wiadomość {msg_num}: {msg_size} bajtów")

                        calculated_total = sum(size for _, size in messages_info)
                        print(f"\nSuma rozmiarów wiadomości: {calculated_total} bajtów")
                        print(f"Rozmiar podany przez STAT: {total_size} bajtów")

                tn.write(b"QUIT\r\n")
                tn.read_until(b"\r\n", timeout=5)
                tn.close()

                return total_size

        return None

    except Exception as e:
        print(f"Błąd podczas połączenia: {e}")
        return None


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


if __name__ == "__main__":
    server = "poczta.interia.pl"
    port = 110
    username = input("Podaj nazwę użytkownika: ")
    password = input("Podaj hasło: ")

    print(f"Łączenie z serwerem {server}:{port}...")
    total_size = check_mailbox_size_telnet(server, port, username, password)

    if total_size is not None:
        print(f"\nWynik: Wiadomości w skrzynce zajmują łącznie {total_size} bajtów")
        print(f"To jest {format_size(total_size)}")
    else:
        print("\nNie udało się pobrać informacji o rozmiarze skrzynki")