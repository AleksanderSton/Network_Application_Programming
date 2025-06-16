import socket
import ssl
import base64
import sys


class POP3Client:
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
            print(f"Server greeting: {response.strip()}")

            return response.startswith('+OK')

        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return False

    def send_command(self, command):
        try:
            self.socket.send(f"{command}\r\n".encode('utf-8'))

            response = self.socket.recv(4096).decode('utf-8')
            print(f"Command: {command}")
            print(f"Response: {response.strip()}")

            return response

        except Exception as e:
            print(f"Błąd wysyłania komendy: {e}")
            return None

    def login(self, username, password):
        """Logowanie do serwera POP3"""
        user_response = self.send_command(f"USER {username}")
        if not user_response or not user_response.startswith('+OK'):
            return False

        pass_response = self.send_command(f"PASS {password}")
        if not pass_response or not pass_response.startswith('+OK'):
            return False

        return True

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

    def find_largest_message(self):
        messages = self.get_message_list()

        if not messages:
            print("Brak wiadomości w skrzynce.")
            return None

        messages.sort(key=lambda x: x[1], reverse=True)

        print(f"\nZnaleziono {len(messages)} wiadomości:")
        for msg_num, msg_size in messages:
            print(f"Wiadomość {msg_num}: {msg_size} bajtów")

        largest_msg = messages[0]
        print(f"\nNajwiększa wiadomość: #{largest_msg[0]} o rozmiarze {largest_msg[1]} bajtów")

        return largest_msg

    def get_message_info(self, msg_num):
        response = self.send_command(f"LIST {msg_num}")
        if response and response.startswith('+OK'):
            return response
        return None

    def quit(self):
        if self.socket:
            self.send_command("QUIT")
            self.socket.close()
            print("Połączenie zamknięte.")


if __name__ == "__main__":
    print("=== Zadanie 5: Znajdowanie największej wiadomości POP3 ===\n")

    server = "pop.gmail.com"
    port = 995

    username = input("Podaj nazwę użytkownika (email): ")
    password = input("Podaj hasło: ")

    client = POP3Client(server, port, use_ssl=True)

    try:
        if not client.connect():
            print("Nie udało się nawiązać połączenia z serwerem.")
            sys.exit(1)

        if not client.login(username, password):
            print("Logowanie nieudane. Sprawdź dane logowania.")
            client.quit()
            sys.exit(1)

        print("\nLogowanie udane!")

        largest_msg = client.find_largest_message()

        if largest_msg:
            msg_num, msg_size = largest_msg
            print(f"\n=== WYNIK ===")
            print(f"Największa wiadomość to #{msg_num} o rozmiarze {msg_size} bajtów")

            info = client.get_message_info(msg_num)
            if info:
                print(f"Szczegóły: {info.strip()}")

        client.quit()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        if client.socket:
            client.quit()