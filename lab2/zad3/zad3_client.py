import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2900

sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:


    sockIPv4.connect((SERVER_IP, SERVER_PORT))
    print(f"Połączono z serwerem {SERVER_IP}:{SERVER_PORT}")

    while True:
        wiadomosc = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")

        if wiadomosc.lower() == 'exit':
            print("Zamykanie połączenia...")
            break

        sockIPv4.sendall(wiadomosc.encode('utf-8'))

        odpowiedz = sockIPv4.recv(4096)
        print(f"Otrzymana odpowiedź: {odpowiedz.decode('utf-8')}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")
finally:
    # Zamykanie gniazda
    sockIPv4.close()
    print("Połączenie zamknięte.")