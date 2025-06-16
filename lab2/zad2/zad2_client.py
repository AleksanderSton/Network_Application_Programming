import socket


SERVER_IP = '127.0.0.1'
SERVER_PORT = 2900


sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockIPv4.settimeout(5)

try:

    result = sockIPv4.connect_ex((SERVER_IP, SERVER_PORT))
    if result ==0:
        print(f"Połączono z serwerem {SERVER_IP}:{SERVER_PORT}")
        wiadomosc = "Witaj, serwerze!"
        print(f"Wysyłanie wiadomości: {wiadomosc}")

        sockIPv4.sendall(wiadomosc.encode('utf-8'))

        odpowiedz = sockIPv4.recv(4096)
        print(f"Otrzymana odpowiedź: {odpowiedz.decode('utf-8')}")
    else:
        print(f"Nie udało się połączyc z serverem {SERVER_IP}:{SERVER_PORT}")



except Exception as e:
    print(f"Wystąpił błąd: {e}")
finally:
    sockIPv4.close()
    print("Połączenie zamknięte.")

