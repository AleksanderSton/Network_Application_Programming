import socket

HOST = '127.0.0.1'
PORT = 65435

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            hostname_to_lookup = input("Wpisz hostname, aby znaleźć jego adres IP (np. google.com): ")

            s.sendto(hostname_to_lookup.encode('utf-8'), (HOST, PORT))
            print(f"Wysłano do serwera hostname: '{hostname_to_lookup}'")

            data, server_addr = s.recvfrom(1024)
            print(f"Odebrano adres IP od {server_addr}: {data.decode('utf-8')}")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")