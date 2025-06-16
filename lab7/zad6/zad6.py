import socket
import ssl
import re
import sys
from datetime import datetime


class POP3InfoClient:
    def __init__(self, server, port=995, use_ssl=True):
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if self.use_ssl:
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(self.socket, server_hostname=self.server)

            self.socket.connect((self.server, self.port))
            response = self.socket.recv(1024).decode('utf-8')
            print(f"Połączono z serwerem: {response.strip()}")

            return response.startswith('+OK')

        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return False

    def send_command(self, command):
        try:
            self.socket.send(f"{command}\r\n".encode('utf-8'))
            response = self.socket.recv(4096).decode('utf-8')
            return response
        except Exception as e:
            print(f"Błąd wysyłania komendy: {e}")
            return None

    def login(self, username, password):
        user_response = self.send_command(f"USER {username}")
        if not user_response or not user_response.startswith('+OK'):
            print(f"Błąd USER: {user_response}")
            return False

        pass_response = self.send_command(f"PASS {password}")
        if not pass_response or not pass_response.startswith('+OK'):
            print(f"Błąd PASS: {pass_response}")
            return False

        return True

    def get_mailbox_info(self):
        response = self.send_command("STAT")
        if not response or not response.startswith('+OK'):
            return None, None

        parts = response.split()
        if len(parts) >= 3:
            try:
                msg_count = int(parts[1])
                total_size = int(parts[2])
                return msg_count, total_size
            except ValueError:
                pass

        return None, None

    def get_message_list(self):
        response = self.send_command("LIST")
        if not response or not response.startswith('+OK'):
            return []

        messages = []
        lines = response.split('\r\n')[1:]

        for line in lines:
            if line == '.' or line == '':
                break
            parts = line.split()
            if len(parts) >= 2:
                try:
                    msg_num = int(parts[0])
                    msg_size = int(parts[1])
                    messages.append((msg_num, msg_size))
                except ValueError:
                    continue

        return messages

    def get_message_headers(self, msg_num, lines=10):
        response = self.send_command(f"TOP {msg_num} {lines}")
        if not response or not response.startswith('+OK'):
            return None

        headers = {}
        lines = response.split('\r\n')[1:]

        current_header = None
        for line in lines:
            if line == '.':
                break

            if line.startswith(' ') or line.startswith('\t'):
                if current_header:
                    headers[current_header] += ' ' + line.strip()
            else:
                if ':' in line:
                    header_name, header_value = line.split(':', 1)
                    header_name = header_name.strip().lower()
                    header_value = header_value.strip()
                    headers[header_name] = header_value
                    current_header = header_name

        return headers

    def format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def display_mailbox_info(self, username):
        print("\n" + "=" * 60)
        print(f"INFORMACJE O SKRZYNCE POCZTOWEJ")
        print("=" * 60)
        print(f"Serwer: {self.server}:{self.port}")
        print(f"Użytkownik: {username}")
        print(f"Data sprawdzenia: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)

        msg_count, total_size = self.get_mailbox_info()
        if msg_count is not None:
            print(f"Liczba wiadomości: {msg_count}")
            print(f"Całkowity rozmiar: {self.format_size(total_size)}")

            if msg_count > 0:
                print(f"Średni rozmiar wiadomości: {self.format_size(total_size // msg_count)}")
        else:
            print("Nie udało się pobrać informacji o skrzynce.")
            return

        if msg_count == 0:
            print("\nSkrzynka jest pusta.")
            return

        messages = self.get_message_list()
        if messages:
            print("\n" + "-" * 60)
            print("SZCZEGÓŁOWE INFORMACJE O WIADOMOŚCIACH")
            print("-" * 60)

            sizes = [size for _, size in messages]
            min_size = min(sizes)
            max_size = max(sizes)

            print(f"Najmniejsza wiadomość: {self.format_size(min_size)}")
            print(f"Największa wiadomość: {self.format_size(max_size)}")

            print(f"\n{'Nr':<4} {'Rozmiar':<10} {'Od':<30} {'Temat':<30}")
            print("-" * 80)

            for i, (msg_num, msg_size) in enumerate(messages[:10]):
                headers = self.get_message_headers(msg_num)

                from_addr = "Nieznany"
                subject = "Brak tematu"

                if headers:
                    from_addr = headers.get('from', 'Nieznany')[:29]
                    subject = headers.get('subject', 'Brak tematu')[:29]

                print(f"{msg_num:<4} {self.format_size(msg_size):<10} {from_addr:<30} {subject:<30}")

            if len(messages) > 10:
                print(f"\n... i {len(messages) - 10} więcej wiadomości")

        print("\n" + "=" * 60)

    def quit(self):
        if self.socket:
            self.send_command("QUIT")
            self.socket.close()



if __name__ == "__main__":
    print("=== Zadanie 6: Informacje o skrzynce POP3 ===\n")

    print("Wybierz serwer POP3:")
    print("1. Gmail (pop.gmail.com)")
    print("2. Outlook (outlook.office365.com)")
    print("3. Yahoo (pop.mail.yahoo.com)")
    print("4. Własny serwer")

    choice = input("Wybór (1-4): ").strip()

    if choice == "1":
        server = "pop.gmail.com"
        port = 995
    elif choice == "2":
        server = "outlook.office365.com"
        port = 995
    elif choice == "3":
        server = "pop.mail.yahoo.com"
        port = 995
    elif choice == "4":
        server = input("Podaj adres serwera: ").strip()
        port = int(input("Podaj port (domyślnie 995): ").strip() or "995")
    else:
        print("Nieprawidłowy wybór. Używam Gmail.")
        server = "pop.gmail.com"
        port = 995

    username = input("Podaj nazwę użytkownika (email): ").strip()
    password = input("Podaj hasło: ").strip()

    client = POP3InfoClient(server, port, use_ssl=True)

    try:
        if not client.connect():
            print("Nie udało się nawiązać połączenia.")
            sys.exit(1)

        if not client.login(username, password):
            print("Logowanie nieudane.")
            client.quit()
            sys.exit(1)

        client.display_mailbox_info(username)

        client.quit()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        if client.socket:
            client.quit()