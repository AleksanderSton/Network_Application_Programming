import poplib
import ssl
import email
from getpass import getpass
from email.header import decode_header
import re
from datetime import datetime


def decode_mime_words(s):
    try:
        decoded_fragments = decode_header(s)
        decoded_string = ''
        for fragment, encoding in decoded_fragments:
            if isinstance(fragment, bytes):
                if encoding:
                    decoded_string += fragment.decode(encoding)
                else:
                    decoded_string += fragment.decode('utf-8', errors='ignore')
            else:
                decoded_string += fragment
        return decoded_string
    except:
        return s


def parse_date(date_str):
    try:
        date_str = re.sub(r'^[A-Za-z]{3},?\s*', '', date_str.strip())

        date_formats = [
            '%d %b %Y %H:%M:%S %z',
            '%d %b %Y %H:%M:%S',
            '%d %b %Y %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str[:len(fmt)], fmt)
            except ValueError:
                continue

        return None
    except:
        return None


def get_email_body(msg):
    body_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        body_parts.append(payload.decode(charset, errors='ignore'))
                    except:
                        body_parts.append(payload.decode('utf-8', errors='ignore'))
            elif content_type == "text/html" and not body_parts:
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        html_content = payload.decode(charset, errors='ignore')
                        # Usuń podstawowe tagi HTML
                        clean_text = re.sub(r'<[^>]+>', '', html_content)
                        body_parts.append(clean_text)
                    except:
                        pass
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                charset = msg.get_content_charset() or 'utf-8'
                body_parts.append(payload.decode(charset, errors='ignore'))
            except:
                body_parts.append(payload.decode('utf-8', errors='ignore'))

    return '\n'.join(body_parts)


def find_newest_message():

    server_host = input("Podaj adres serwera POP3 (np. pop.gmail.com): ").strip()
    if not server_host:
        server_host = "pop.gmail.com"

    port = input("Podaj port (domyślnie 995 dla SSL): ").strip()
    if not port:
        port = 995
    else:
        port = int(port)

    use_ssl = input("Użyć SSL? (t/n, domyślnie t): ").strip().lower()
    if use_ssl != 'n':
        use_ssl = True
    else:
        use_ssl = False

    username = input("Nazwa użytkownika: ").strip()
    password = getpass("Hasło: ")

    try:
        print(f"\nŁączenie z serwerem {server_host}:{port}...")

        if use_ssl:
            mail_server = poplib.POP3_SSL(server_host, port)
        else:
            mail_server = poplib.POP3(server_host, port)

        print("Połączenie nawiązane pomyślnie!")

        print("Logowanie...")
        mail_server.user(username)
        mail_server.pass_(password)
        print("Zalogowano pomyślnie!")

        mail_info = mail_server.stat()
        num_messages = mail_info[0]

        print(f"\nLiczba wiadomości w skrzynce: {num_messages}")

        if num_messages == 0:
            print("Skrzynka jest pusta.")
            mail_server.quit()
            return

        print("Szukam najnowszej wiadomości...")

        newest_message = None
        newest_date = None
        newest_msg_num = None

        for msg_num in range(1, num_messages + 1):
            try:
                header_response = mail_server.top(msg_num, 0)
                header_lines = header_response[1]
                header_text = b'\n'.join(header_lines).decode('utf-8', errors='ignore')

                msg = email.message_from_string(header_text)
                date_str = msg.get('Date', '')

                if date_str:
                    parsed_date = parse_date(date_str)
                    if parsed_date:
                        if newest_date is None or parsed_date > newest_date:
                            newest_date = parsed_date
                            newest_msg_num = msg_num
                            newest_message = msg

            except Exception as e:
                print(f"Błąd podczas analizowania wiadomości {msg_num}: {e}")
                continue

        if newest_msg_num is None:
            print("Nie można określić najnowszej wiadomości na podstawie dat.")
            print("Wybieram ostatnią wiadomość w skrzynce...")
            newest_msg_num = num_messages

        print(f"Pobieranie treści wiadomości #{newest_msg_num}...")

        full_response = mail_server.retr(newest_msg_num)
        full_lines = full_response[1]
        full_message = b'\n'.join(full_lines).decode('utf-8', errors='ignore')

        full_msg = email.message_from_string(full_message)

        message_size = sum(len(line) + 2 for line in full_lines)

        print(f"\n" + "=" * 70)
        print("NAJNOWSZA WIADOMOŚĆ")
        print("=" * 70)

        subject = decode_mime_words(full_msg.get('Subject', 'Brak tematu'))
        sender = decode_mime_words(full_msg.get('From', 'Nieznany nadawca'))
        date = full_msg.get('Date', 'Nieznana data')
        to_addr = decode_mime_words(full_msg.get('To', 'Nieznany odbiorca'))

        print(f"Numer wiadomości: {newest_msg_num}")
        print(f"Rozmiar: {message_size} bajtów ({message_size / 1024:.2f} KB)")
        print(f"Od: {sender}")
        print(f"Do: {to_addr}")
        print(f"Temat: {subject}")
        print(f"Data: {date}")
        print(f"Typ zawartości: {full_msg.get_content_type()}")

        print(f"\n" + "-" * 50)
        print("TREŚĆ WIADOMOŚCI:")
        print("-" * 50)

        body = get_email_body(full_msg)
        if body.strip():
            max_chars = 2000
            if len(body) > max_chars:
                print(body[:max_chars])
                print(f"\n[...treść skrócona, wyświetlono {max_chars} z {len(body)} znaków...]")
            else:
                print(body)
        else:
            print("Nie można wyodrębnić treści tekstowej z tej wiadomości.")

            if full_msg.is_multipart():
                print("\nWiadomość zawiera następujące części:")
                for i, part in enumerate(full_msg.get_payload()):
                    print(f"  Część {i + 1}: {part.get_content_type()}")
            else:
                raw_payload = full_msg.get_payload()
                if isinstance(raw_payload, str) and raw_payload.strip():
                    print("\nSurowa treść:")
                    print(raw_payload[:1000])
                    if len(raw_payload) > 1000:
                        print("[...treść skrócona...]")

        mail_server.quit()
        print(f"\n{'=' * 70}")
        print(f"Połączenie z serwerem {server_host} zostało zamknięte.")

    except poplib.error_proto as e:
        print(f"Błąd protokołu POP3: {e}")
    except ssl.SSLError as e:
        print(f"Błąd SSL: {e}")
    except ConnectionRefusedError:
        print(f"Nie można połączyć się z serwerem {server_host}:{port}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    print("Program klienta POP3 - wyświetlanie najnowszej wiadomości")
    print("=" * 60)

    try:
        find_newest_message()
    except KeyboardInterrupt:
        print("\n\nProgram został przerwany przez użytkownika.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")