import socket

HOST = '127.0.0.1'
PORT = 65432



if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            message = input("Wpisz wiadomość do wysłania do serwera echo UDP: ")

            s.sendto(message.encode('utf-8'), (HOST, PORT))
            print(f"Wysłano do serwera: '{message}'")

            data, server_addr = s.recvfrom(1024)
            print(f"Odebrano od {server_addr}: {data.decode('utf-8')}")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")