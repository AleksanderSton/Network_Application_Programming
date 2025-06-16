import poplib
import ssl
from getpass import getpass


def connect_pop3_server():

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

        print("\n" + "=" * 50)
        print("INFORMACJE O SKRZYNCE POCZTOWEJ")
        print("=" * 50)

        mail_info = mail_server.stat()
        num_messages = mail_info[0]
        total_size = mail_info[1]

        print(f"Liczba wiadomości: {num_messages}")
        print(f"Całkowity rozmiar skrzynki: {total_size} bajtów ({total_size / 1024:.2f} KB)")

        if num_messages > 0:
            print(f"Średni rozmiar wiadomości: {total_size / num_messages:.2f} bajtów")

            print(f"\nLista wiadomości:")
            print("-" * 40)

            messages_info = mail_server.list()

            for msg_info in messages_info[1]:
                msg_data = msg_info.decode('utf-8').split()
                msg_num = msg_data[0]
                msg_size = msg_data[1]
                print(f"Wiadomość {msg_num}: {msg_size} bajtów ({int(msg_size) / 1024:.2f} KB)")
        else:
            print("Skrzynka jest pusta.")

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
    print("Program klienta POP3 - wyświetlanie informacji o wiadomościach")
    print("=" * 60)

    try:
        connect_pop3_server()
    except KeyboardInterrupt:
        print("\n\nProgram został przerwany przez użytkownika.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")