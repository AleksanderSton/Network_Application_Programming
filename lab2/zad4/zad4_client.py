import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2901

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Klient UDP przygotowany do wysyłania wiadomości do {SERVER_IP}:{SERVER_PORT}")
try:
    while True:
        wiadomosc = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")

        if wiadomosc.lower() == 'exit':
            print("Zamykanie klienta...")
            break

        client_socket.sendto(wiadomosc.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print(f"Wysłano wiadomość do serwera: {wiadomosc}")

        odpowiedz, server_address = client_socket.recvfrom(4096)
        print(f"Otrzymana odpowiedź od serwera: {odpowiedz.decode('utf-8')}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")
finally:
    client_socket.close()
    print("Gniazdo zamknięte.")
