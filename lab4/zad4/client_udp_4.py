import socket

HOST = '127.0.0.1'
PORT = 65433


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            expression = input("Wpisz działanie (np. '5 + 3', '10 * 2'): ")

            s.sendto(expression.encode('utf-8'), (HOST, PORT))
            print(f"Wysłano do serwera: '{expression}'")

            data, server_addr = s.recvfrom(1024)
            print(f"Odebrano wynik od {server_addr}: {data.decode('utf-8')}")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")