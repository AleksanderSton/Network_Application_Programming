import socket

HOST = '127.0.0.1'
PORT = 65435

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Serwer Rozpoznawania IP (z Hostname) UDP nasłuchuje na {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(1024)
            hostname_to_lookup = data.decode('utf-8').strip()
            print(f"Odebrano od {addr} hostname: '{hostname_to_lookup}'")

            ip_address = "Nie znaleziono adresu IP dla podanej nazwy hosta."
            try:
                ip_address = socket.gethostbyname(hostname_to_lookup)
            except socket.gaierror:
                ip_address = "Błąd: Nie można rozpoznać adresu IP dla podanej nazwy hosta."
            except Exception as e:
                ip_address = f"Wystąpił błąd serwera: {e}"

            s.sendto(ip_address.encode('utf-8'), addr)
            print(f"Odesłano do {addr} adres IP: '{ip_address}'")