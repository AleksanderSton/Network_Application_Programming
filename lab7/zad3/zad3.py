import telnetlib
import sys


def check_individual_message_sizes(server, port, username, password):
    try:
        tn = telnetlib.Telnet(server, port, timeout=10)

        response = tn.read_until(b"\r\n", timeout=5)
        print(f"Powitanie serwera: {response.decode('utf-8').strip()}")

        if not response.startswith(b"+OK"):
            print("Błąd: Serwer nie odpowiedział pozytywnie")
            return None

        tn.write(f"USER {username}\r\n".encode('utf-8'))
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nieprawidłowa nazwa użytkownika")
            return None

        tn.write(f"PASS {password}\r\n".encode('utf-8'))
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nieprawidłowe hasło")
            return None

        tn.write(b"STAT\r\n")
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nie można pobrać statusu skrzynki")
            return None

        parts = response.decode('utf-8').split()
        message_count = int(parts[1])
        total_size = int(parts[2])

        print(f"Liczba wiadomości w skrzynce: {message_count}")
        print(f"Całkowity rozmiar: {total_size} bajtów\n")

        if message_count == 0:
            print("Skrzynka jest pusta")
            return []

        tn.write(b"LIST\r\n")
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nie można pobrać listy wiadomości")
            return None

        messages_info = []
        print("Rozmiary poszczególnych wiadomości:")
        print("-" * 40)

        while True:
            line = tn.read_until(b"\r\n", timeout=5)
            if line.strip() == b".":
                break

            parts = line.decode('utf-8').strip().split()
            if len(parts) >= 2:
                msg_num = int(parts[0])
                msg_size = int(parts[1])
                messages_info.append((msg_num, msg_size))

                size_str = format_size(msg_size)
                print(f"Wiadomość {msg_num:3d}: {msg_size:8d} bajtów ({size_str})")

        print("-" * 40)

        if messages_info:
            sizes = [size for _, size in messages_info]
            min_size = min(sizes)
            max_size = max(sizes)
            avg_size = sum(sizes) / len(sizes)

            print(f"Statystyki:")
            print(f"  Najmniejsza wiadomość: {min_size} bajtów ({format_size(min_size)})")
            print(f"  Największa wiadomość:  {max_size} bajtów ({format_size(max_size)})")
            print(f"  Średni rozmiar:        {avg_size:.0f} bajtów ({format_size(avg_size)})")
            print(f"  Suma kontrolna:        {sum(sizes)} bajtów")

        print("\nMożesz sprawdzić rozmiar konkretnej wiadomości:")
        try:
            msg_choice = input("Podaj numer wiadomości (Enter = pomiń): ").strip()
            if msg_choice:
                msg_num = int(msg_choice)
                if 1 <= msg_num <= message_count:
                    tn.write(f"LIST {msg_num}\r\n".encode('utf-8'))
                    response = tn.read_until(b"\r\n", timeout=5)

                    if response.startswith(b"+OK"):
                        parts = response.decode('utf-8').split()
                        if len(parts) >= 3:
                            size = int(parts[2])
                            print(f"Wiadomość {msg_num} ma rozmiar {size} bajtów ({format_size(size)})")
        except (ValueError, KeyboardInterrupt):
            pass

        tn.write(b"QUIT\r\n")
        tn.read_until(b"\r\n", timeout=5)
        tn.close()

        return messages_info

    except Exception as e:
        print(f"Błąd podczas połączenia: {e}")
        return None


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"



if __name__ == "__main__":
    server = "poczta.interia.pl"
    port = 110
    username = input("Podaj nazwę użytkownika: ")
    password = input("Podaj hasło: ")

    print(f"Łączenie z serwerem {server}:{port}...")
    messages_info = check_individual_message_sizes(server, port, username, password)

    if messages_info is not None:
        if messages_info:
            print(f"\nZnaleziono {len(messages_info)} wiadomości w skrzynce")
        else:
            print("\nSkrzynka jest pusta")
    else:
        print("\nNie udało się pobrać informacji o wiadomościach")