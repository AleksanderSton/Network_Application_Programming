import poplib
import email
from email.header import decode_header
import sys


def decode_mime_words(s):
    if s is None:
        return ""

    decoded_fragments = decode_header(s)
    decoded_string = ""

    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            if encoding:
                try:
                    decoded_string += fragment.decode(encoding)
                except (UnicodeDecodeError, LookupError):
                    decoded_string += fragment.decode('utf-8', errors='ignore')
            else:
                decoded_string += fragment.decode('utf-8', errors='ignore')
        else:
            decoded_string += fragment

    return decoded_string


def connect_to_pop3_server(server, port, username, password, use_ssl=True):
    try:
        if use_ssl:
            print(f"Łączenie z serwerem POP3S: {server}:{port}")
            pop3_server = poplib.POP3_SSL(server, port)
        else:
            print(f"Łączenie z serwerem POP3: {server}:{port}")
            pop3_server = poplib.POP3(server, port)

        pop3_server.user(username)
        pop3_server.pass_(password)

        print("Pomyślnie połączono z serwerem POP3")
        return pop3_server

    except poplib.error_proto as e:
        print(f"Błąd protokołu POP3: {e}")
        return None
    except Exception as e:
        print(f"Błąd połączenia: {e}")
        return None


def display_all_messages(pop3_server):
    try:
        messages_info = pop3_server.list()
        num_messages = len(messages_info[1])

        print(f"\nLiczba wiadomości w skrzynce: {num_messages}")

        if num_messages == 0:
            print("Brak wiadomości w skrzynce.")
            return

        print("\n" + "=" * 80)
        print("WSZYSTKIE WIADOMOŚCI")
        print("=" * 80)

        for i in range(1, num_messages + 1):
            print(f"\n--- WIADOMOŚĆ {i} ---")

            try:
                raw_email = pop3_server.retr(i)
                email_content = b'\n'.join(raw_email[1])

                msg = email.message_from_bytes(email_content)

                print(f"Od: {decode_mime_words(msg.get('From', 'Nieznany'))}")
                print(f"Do: {decode_mime_words(msg.get('To', 'Nieznany'))}")
                print(f"Temat: {decode_mime_words(msg.get('Subject', 'Bez tematu'))}")
                print(f"Data: {msg.get('Date', 'Nieznana')}")

                print("\nTreść:")
                print("-" * 40)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = part.get_payload(decode=True)
                                if body:
                                    charset = part.get_content_charset() or 'utf-8'
                                    decoded_body = body.decode(charset, errors='ignore')
                                    print(decoded_body[:500])  # Pierwsze 500 znaków
                                    if len(decoded_body) > 500:
                                        print("... (treść skrócona)")
                                break
                            except Exception as e:
                                print(f"Błąd dekodowania treści: {e}")
                else:
                    try:
                        body = msg.get_payload(decode=True)
                        if body:
                            charset = msg.get_content_charset() or 'utf-8'
                            decoded_body = body.decode(charset, errors='ignore')
                            print(decoded_body[:500])  # Pierwsze 500 znaków
                            if len(decoded_body) > 500:
                                print("... (treść skrócona)")
                    except Exception as e:
                        print(f"Błąd dekodowania treści: {e}")

                print("-" * 40)

            except Exception as e:
                print(f"Błąd podczas pobierania wiadomości {i}: {e}")

        print(f"\nWyświetlono wszystkie {num_messages} wiadomości.")

    except Exception as e:
        print(f"Błąd podczas wyświetlania wiadomości: {e}")

if __name__ == "__main__":
    print("=== KLIENT POP3 - WYŚWIETLANIE WSZYSTKICH WIADOMOŚCI ===\n")

    server_configs = [
        {
            'name': 'Gmail',
            'server': 'pop.gmail.com',
            'port': 995,
            'ssl': True
        },
        {
            'name': 'Outlook/Hotmail',
            'server': 'outlook.office365.com',
            'port': 995,
            'ssl': True
        },
        {
            'name': 'Yahoo',
            'server': 'pop.mail.yahoo.com',
            'port': 995,
            'ssl': True
        },
        {
            'name': 'Własna konfiguracja',
            'server': None,
            'port': None,
            'ssl': True
        }
    ]

    print("Dostępne konfiguracje serwerów:")
    for i, config in enumerate(server_configs, 1):
        print(f"{i}. {config['name']}")

    try:
        choice = int(input("\nWybierz konfigurację serwera (1-4): "))
        if choice < 1 or choice > 4:
            raise ValueError("Nieprawidłowy wybór")

        config = server_configs[choice - 1]

        if config['server'] is None:
            # Własna konfiguracja
            server = input("Adres serwera POP3: ")
            port = int(input("Port (domyślnie 995): ") or "995")
            use_ssl = input("Używać SSL? (t/n, domyślnie t): ").lower() != 'n'
        else:
            server = config['server']
            port = config['port']
            use_ssl = config['ssl']

        username = input("Nazwa użytkownika (email): ")
        password = input("Hasło: ")

        pop3_server = connect_to_pop3_server(server, port, username, password, use_ssl)

        if pop3_server:
            try:
                display_all_messages(pop3_server)

            finally:
                pop3_server.quit()
                print("\nPołączenie zamknięte.")

    except KeyboardInterrupt:
        print("\n\nPrzerwano przez użytkownika.")
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")