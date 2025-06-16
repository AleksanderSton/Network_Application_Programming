import socket


if __name__ == "__main__":
    target_hostname = "google.com"
    try:
        ip_address = socket.gethostbyname(target_hostname)
        print(f"Skanowanie portów dla: {target_hostname} ({ip_address})")
        for port in range(1, 65536):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target_hostname, port))
                if result == 0:
                    try:
                        service_name = socket.getservbyport(port)
                    except OSError:
                        service_name = "Nieznana usługa"
                    print(f"Port {port} jest otwarty, usługa: {service_name}")
                sock.close()
            except socket.error as e:
                pass
            except KeyboardInterrupt:
                print("\nSkanowanie przerwane przez użytkownika.")
                break
    except socket.gaierror:
        print(f"Nie można rozpoznać nazwy hosta: {target_hostname}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    print("Skanowanie portów zakończone.")