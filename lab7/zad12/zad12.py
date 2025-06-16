import socket
import time


def connect_to_smtp_server():


    server_address = '127.0.0.1'
    server_port = 25

    try:
        print(f"Próba połączenia z serwerem pocztowym {server_address}:{server_port}")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)

        client_socket.connect((server_address, server_port))
        print(f"✓ Pomyślnie połączono z serwerem {server_address}:{server_port}")

        try:
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Odpowiedź serwera: {response.strip()}")
        except socket.timeout:
            print("Brak odpowiedzi od serwera w określonym czasie")

        smtp_commands = [
            "HELO localhost",
            "MAIL FROM:<test@example.com>",
            "RCPT TO:<recipient@example.com>",
            "DATA",
            "QUIT"
        ]

        print("\n--- Symulacja dialogu SMTP ---")
        print("UWAGA: To jest tylko demonstracja - nie wysyłamy faktycznych e-maili")

        for command in smtp_commands:
            print(f"Klient wysłałby: {command}")
            time.sleep(0.5)

            # W rzeczywistej implementacji tutaj byłoby:
            # client_socket.send((command + "\r\n").encode('utf-8'))
            # response = client_socket.recv(1024).decode('utf-8')
            # print(f"Serwer odpowiedziałby: {response.strip()}")

        print("\n--- Koniec symulacji ---")

    except ConnectionRefusedError:
        print(f"✗ Błąd: Nie można połączyć się z serwerem {server_address}:{server_port}")
        print("  Serwer może być wyłączony lub port może być zablokowany")

    except socket.timeout:
        print("✗ Błąd: Przekroczono limit czasu połączenia")

    except Exception as e:
        print(f"✗ Nieoczekiwany błąd: {e}")

    finally:
        try:
            client_socket.close()
            print("Połączenie zamknięte")
        except:
            pass



if __name__ == "__main__":
    print("=== KLIENT POCZTOWY ===")
    print("Program łączący się z serwerem pocztowym")
    print("Adres serwera: 127.0.0.1 (localhost)")
    print()

    connect_to_smtp_server()

    print("\n=== INFORMACJE DODATKOWE ===")
    print("Dla pełnej funkcjonalności klienta pocztowego należałoby zaimplementować:")
    print("1. Pełny dialog SMTP z obsługą odpowiedzi serwera")
    print("2. Uwierzytelnianie użytkownika (AUTH)")
    print("3. Szyfrowanie połączenia (STARTTLS)")
    print("4. Obsługę załączników (MIME)")
    print("5. Walidację adresów e-mail")
    print("6. Obsługę błędów i ponownych prób wysyłania")