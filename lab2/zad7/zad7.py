import sys
import socket

if __name__ == "__main__":
    hostname_input = input("Podaj hostname lub adres IP: ")
    port_input = input("Podaj numer portu: ")

    if not port_input.isdigit():
        print("Błąd: Numer portu musi być liczbą.")
        sys.exit(1)

    hostname = hostname_input
    port = int(port_input)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5) # 5 sekund
        sock.connect((hostname, port))
        print("Połączono")
        try:
            service_name = socket.getservbyport(port)
            print("Usługa: " + service_name)
        except OSError:
            print("Usługa: Nieznana (port " + str(port) + ")")
        sock.close()
    except ConnectionRefusedError:
        print("Połączenie odrzucone (Connection refused)")
    except socket.timeout:
        print("Przekroczono czas oczekiwania na połączenie (Connection timed out)")
    except socket.gaierror:
        print("Błąd: Nie można rozwiązać nazwy hosta lub adresu IP (Hostname or IP could not be resolved)")
    except OverflowError:
        print(f"Błąd: Numer portu {port} jest poza dopuszczalnym zakresem (0-65535).")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")