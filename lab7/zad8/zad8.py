import poplib
import ssl
import email
from getpass import getpass
from email.header import decode_header


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


def connect_pop3_and_download():

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

    max_messages = input("Maksymalna liczba wiadomości do analizy (domyślnie 10): ").strip()
    if not max_messages:
        max_messages = 10
    else:
        max_messages = int(max_messages)

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
        total_size = mail_info[1]

        print(f"\n" + "=" * 70)
        print("SZCZEGÓŁOWE INFORMACJE O WIADOMOŚCIACH")
        print("=" * 70)
        print(f"Całkowita liczba wiadomości: {num_messages}")
        print(f"Całkowity rozmiar skrzynki: {total_size} bajtów ({total_size / 1024:.2f} KB)")

        if num_messages == 0:
            print("Skrzynka jest pusta.")
            mail_server.quit()
            return

        messages_to_analyze = min(num_messages, max_messages)
        print(f"Analizuję pierwsze {messages_to_analyze} wiadomości...\n")

        total_analyzed_size = 0

        for msg_num in range(1, messages_to_analyze + 1):
            try:
                print(f"Analizuję wiadomość {msg_num}/{messages_to_analyze}...")

                header_response = mail_server.top(msg_num, 0)
                header_lines = header_response[1]

                full_response = mail_server.retr(msg_num)
                full_lines = full_response[1]

                message_size = sum(len(line) + 2 for line in full_lines)  # +2 dla CRLF
                total_analyzed_size += message_size

                header_text = b'\n'.join(header_lines).decode('utf-8', errors='ignore')
                msg = email.message_from_string(header_text)

                subject = decode_mime_words(msg.get('Subject', 'Brak tematu'))
                sender = decode_mime_words(msg.get('From', 'Nieznany nadawca'))
                date = msg.get('Date', 'Nieznana data')

                print(f"  Wiadomość #{msg_num}:")
                print(f"    Rozmiar: {message_size} bajtów ({message_size / 1024:.2f} KB)")
                print(f"    Od: {sender}")
                print(f"    Temat: {subject}")
                print(f"    Data: {date}")

                if msg.is_multipart():
                    print(f"    Typ: Wiadomość wieloczęściowa")
                else:
                    content_type = msg.get_content_type()
                    print(f"    Typ zawartości: {content_type}")

                print(f"    {'=' * 50}")

            except Exception as e:
                print(f"  Błąd podczas analizowania wiadomości {msg_num}: {e}")
                continue

        print(f"\nPODSUMOWANIE:")
        print(f"Przeanalizowano: {messages_to_analyze} wiadomości")
        print(
            f"Łączny rozmiar przeanalizowanych wiadomości: {total_analyzed_size} bajtów ({total_analyzed_size / 1024:.2f} KB)")
        if messages_to_analyze > 0:
            print(f"Średni rozmiar wiadomości: {total_analyzed_size / messages_to_analyze:.2f} bajtów")

        mail_server.quit()
        print(f"\nPołączenie z serwerem {server_host} zostało zamknięte.")

    except poplib.error_proto as e:
        print(f"Błąd protokołu POP3: {e}")
    except ssl.SSLError as e:
        print(f"Błąd SSL: {e}")
    except ConnectionRefusedError:
        print(f"Nie można połączyć się z serwerem {server_host}:{port}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")



if __name__ == "__main__":
    print("Program klienta POP3 - szczegółowa analiza wiadomości")
    print("=" * 60)
    print("UWAGA: Program pobiera pełne wiadomości w celu dokładnego")
    print("       obliczenia rozmiaru. Może to zająć czas dla dużych skrzynek.")
    print("=" * 60)

    try:
        connect_pop3_and_download()
    except KeyboardInterrupt:
        print("\n\nProgram został przerwany przez użytkownika.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")