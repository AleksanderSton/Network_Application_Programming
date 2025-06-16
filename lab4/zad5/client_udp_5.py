import socket

HOST = '127.0.0.1'
PORT = 65434


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            ip_to_lookup = input("Wpisz adres IP, aby znaleźć jego hostname (np. 8.8.8.8): ")

            s.sendto(ip_to_lookup.encode('utf-8'), (HOST, PORT))
            print(f"Wysłano do serwera IP: '{ip_to_lookup}'")

            data, server_addr = s.recvfrom(1024)
            print(f"Odebrano hostname od {server_addr}: {data.decode('utf-8')}")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")