import socket

HOST = '127.0.0.1'
PORT = 65434

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Serwer Rozpoznawania Hostname (z IP) UDP nasłuchuje na {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(1024)
            ip_address = data.decode('utf-8').strip()
            print(f"Odebrano od {addr} adres IP: '{ip_address}'")

            hostname = "Nie znaleziono hostname dla podanego IP."
            try:

                hostname_info = socket.gethostbyaddr(ip_address)
                hostname = hostname_info[0]
            except socket.herror:
                hostname = "Błąd: Nie można rozpoznać hostname dla podanego IP."
            except Exception as e:
                hostname = f"Wystąpił błąd serwera: {e}"

            s.sendto(hostname.encode('utf-8'), addr)
            print(f"Odesłano do {addr} hostname: '{hostname}'")