import poplib
import email
from email.header import decode_header
import os
import sys
import mimetypes


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


def is_image_file(filename, content_type):
    if not filename:
        return content_type and content_type.startswith('image/')

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']
    ext = os.path.splitext(filename.lower())[1]

    if ext in image_extensions:
        return True

    return content_type and content_type.startswith('image/')


def safe_filename(filename):
    if not filename:
        return "unnamed_image"

    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')

    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext

    return filename


def save_image_attachment(part, download_dir, message_num, attachment_num):
    try:
        filename = part.get_filename()
        if filename:
            filename = decode_mime_words(filename)
            filename = safe_filename(filename)
        else:
            content_type = part.get_content_type()
            ext = mimetypes.guess_extension(content_type) or '.bin'
            filename = f"attachment_{message_num}_{attachment_num}{ext}"

        filepath = os.path.join(download_dir, filename)

        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1

        payload = part.get_payload(decode=True)
        if payload:
            with open(filepath, 'wb') as f:
                f.write(payload)

            file_size = len(payload)
            print(f"  ✓ Zapisano: {filename} ({file_size} bajtów)")
            return True
        else:
            print(f"  ✗ Brak danych dla załącznika: {filename}")
            return False

    except Exception as e:
        print(f"  ✗ Błąd podczas zapisywania załącznika: {e}")
        return False


def process_message_attachments(pop3_server, message_num, download_dir):
    try:
        raw_email = pop3_server.retr(message_num)
        email_content = b'\n'.join(raw_email[1])

        msg = email.message_from_bytes(email_content)

        print(f"\n--- WIADOMOŚĆ {message_num} ---")
        print(f"Od: {decode_mime_words(msg.get('From', 'Nieznany'))}")
        print(f"Temat: {decode_mime_words(msg.get('Subject', 'Bez tematu'))}")
        print(f"Data: {msg.get('Date', 'Nieznana')}")

        if not msg.is_multipart():
            print("Wiadomość nie ma załączników.")
            return False

        attachment_count = 0
        image_count = 0

        for part_num, part in enumerate(msg.walk(), 1):
            if part.get_content_maintype() == 'multipart':
                continue

            content_disposition = part.get('Content-Disposition', '')
            filename = part.get_filename()
            content_type = part.get_content_type()

            if 'attachment' in content_disposition or filename:
                attachment_count += 1
                print(f"\nZałącznik {attachment_count}:")
                print(f"  Nazwa: {decode_mime_words(filename) if filename else 'Brak nazwy'}")
                print(f"  Typ: {content_type}")

                if is_image_file(filename, content_type):
                    print(f"  Typ: OBRAZEK - zapisywanie...")
                    if save_image_attachment(part, download_dir, message_num, attachment_count):
                        image_count += 1
                else:
                    print(f"  Typ: Inny plik - pomijanie")

        if attachment_count == 0:
            print("Brak załączników w wiadomości.")
            return False
        else:
            print(f"\nPodsumowanie: znaleziono {attachment_count} załączników, zapisano {image_count} obrazków.")
            return image_count > 0

    except Exception as e:
        print(f"Błąd podczas przetwarzania wiadomości {message_num}: {e}")
        return False


def find_and_download_images(pop3_server, download_dir):
    try:
        messages_info = pop3_server.list()
        num_messages = len(messages_info[1])

        print(f"\nLiczba wiadomości w skrzynce: {num_messages}")

        if num_messages == 0:
            print("Brak wiadomości w skrzynce.")
            return

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print(f"Utworzono katalog: {download_dir}")

        print(f"Katalog pobierania: {download_dir}")
        print("\n" + "=" * 80)
        print("PRZETWARZANIE WIADOMOŚCI Z ZAŁĄCZNIKAMI")
        print("=" * 80)

        total_images = 0
        messages_with_images = 0

        for i in range(1, num_messages + 1):
            if process_message_attachments(pop3_server, i, download_dir):
                messages_with_images += 1

        print(f"\n" + "=" * 80)
        print(f"PODSUMOWANIE:")
        print(f"Przeszukano wiadomości: {num_messages}")
        print(f"Wiadomości z obrazkami: {messages_with_images}")
        print(f"Pobrane obrazki zapisano w: {download_dir}")
        print("=" * 80)

    except Exception as e:
        print(f"Błąd podczas przetwarzania wiadomości: {e}")


if __name__ == "__main__":
    print("=== KLIENT POP3 - POBIERANIE OBRAZKÓW Z ZAŁĄCZNIKÓW ===\n")

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
            server = input("Adres serwera POP3: ")
            port = int(input("Port (domyślnie 995): ") or "995")
            use_ssl = input("Używać SSL? (t/n, domyślnie t): ").lower() != 'n'
        else:
            server = config['server']
            port = config['port']
            use_ssl = config['ssl']

        username = input("Nazwa użytkownika (email): ")
        password = input("Hasło: ")

        download_dir = input("Katalog pobierania (domyślnie 'downloads'): ") or "downloads"

        pop3_server = connect_to_pop3_server(server, port, username, password, use_ssl)

        if pop3_server:
            try:
                find_and_download_images(pop3_server, download_dir)

            finally:
                pop3_server.quit()
                print("\nPołączenie zamknięte.")

    except KeyboardInterrupt:
        print("\n\nPrzerwano przez użytkownika.")
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")