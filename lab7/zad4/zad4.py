import telnetlib
import sys
import email
from email.header import decode_header


def find_and_display_largest_message(server, port, username, password):
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

        if message_count == 0:
            print("Skrzynka jest pusta")
            return None

        print(f"Liczba wiadomości w skrzynce: {message_count}")

        tn.write(b"LIST\r\n")
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nie można pobrać listy wiadomości")
            return None

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

        largest_msg = max(messages_info, key=lambda x: x[1])
        largest_msg_num, largest_msg_size = largest_msg

        print(f"Największa wiadomość: numer {largest_msg_num}, rozmiar {largest_msg_size} bajtów")
        print("-" * 60)

        tn.write(f"RETR {largest_msg_num}\r\n".encode('utf-8'))
        response = tn.read_until(b"\r\n", timeout=5)

        if not response.startswith(b"+OK"):
            print("Błąd: Nie można pobrać wiadomości")
            return None

        message_content = b""
        while True:
            line = tn.read_until(b"\r\n", timeout=10)
            if line.strip() == b".":
                break

            if line.startswith(b".."):
                line = line[1:]

            message_content += line

        try:
            msg = email.message_from_bytes(message_content)

            print("NAGŁÓWKI WIADOMOŚCI:")
            print("=" * 60)

            headers_to_show = ['From', 'To', 'Subject', 'Date', 'Content-Type']

            for header in headers_to_show:
                if header in msg:
                    value = msg[header]
                    if header in ['Subject', 'From', 'To']:
                        decoded_parts = decode_header(value)
                        decoded_value = ""
                        for part, encoding in decoded_parts:
                            if isinstance(part, bytes):
                                if encoding:
                                    decoded_value += part.decode(encoding)
                                else:
                                    decoded_value += part.decode('utf-8', errors='ignore')
                            else:
                                decoded_value += part
                        value = decoded_value

                    print(f"{header}: {value}")

            print("\nTREŚĆ WIADOMOŚCI:")
            print("=" * 60)

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            charset = part.get_content_charset() or 'utf-8'
                            try:
                                text = payload.decode(charset)
                                print(text)
                            except UnicodeDecodeError:
                                print(payload.decode('utf-8', errors='ignore'))
                        break
                else:
                    for part in msg.walk():
                        if part.get_content_type().startswith("text/"):
                            payload = part.get_payload(decode=True)
                            if payload:
                                charset = part.get_content_charset() or 'utf-8'
                                try:
                                    text = payload.decode(charset)
                                    print(f"[{part.get_content_type()}]")
                                    print(text[:1000] + "..." if len(text) > 1000 else text)
                                except UnicodeDecodeError:
                                    print("[Nie można zdekodować zawartości]")
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    try:
                        text = payload.decode(charset)
                        print(text)
                    except UnicodeDecodeError:
                        print(payload.decode('utf-8', errors='ignore'))

        except Exception as e:
            print(f"Błąd podczas parsowania wiadomości: {e}")
            print("\nSurowa treść wiadomości:")
            print(message_content.decode('utf-8', errors='ignore'))

        tn.write(b"QUIT\r\n")
        tn.read_until(b"\r\n", timeout=5)
        tn.close()

        return largest_msg_num, largest_msg_size

    except Exception as e:
        print(f"Błąd podczas połączenia: {e}")
        return None



if __name__ == "__main__":
    server = "poczta.interia.pl"
    port = 110
    username = input("Podaj nazwę użytkownika: ")
    password = input("Podaj hasło: ")

    print(f"Łączenie z serwerem {server}:{port}...")
    result = find_and_display_largest_message(server, port, username, password)

    if result:
        msg_num, msg_size = result
        print(f"\nWyświetlono największą wiadomość (nr {msg_num}, {msg_size} bajtów)")
    else:
        print("\nNie udało się pobrać największej wiadomości")