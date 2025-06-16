import socket
import time

TARGET_IP = '212.182.24.27'
TARGET_TCP_PORT = 2913
UDP_PORTS_TO_KNOCK = [12345, 54321, 65534, 666]

def send_udp_knock(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(b'KNOCK', (ip, port))
            print(f"Wysłano pakiet UDP na {ip}:{port}")
    except socket.error as e:
        print(f"Błąd wysyłania UDP na {ip}:{port}: {e}")


if __name__ == "__main__":
    print(f"Rozpoczynanie sekwencji port-knocking dla {TARGET_IP}:{TARGET_TCP_PORT}")

    print("Symulacja szukania portów UDP (dla uproszczenia, używamy stałej sekwencji)...")
    for udp_port in UDP_PORTS_TO_KNOCK:
        send_udp_knock(TARGET_IP, udp_port)
        time.sleep(0.5)

    print(f"\nPróba połączenia TCP z {TARGET_IP}:{TARGET_TCP_PORT} po sekwencji...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.connect((TARGET_IP, TARGET_TCP_PORT))
            print(f"Pomyślnie połączono z serwerem TCP na {TARGET_IP}:{TARGET_TCP_PORT}")

            data = tcp_sock.recv(1024)
            print(f"Otrzymano wiadomość od serwera: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print(
            f"Połączenie TCP odrzucone. Prawdopodobnie sekwencja port-knocking była błędna lub port nie został otwarty.")
    except socket.timeout:
        print(f"Timeout połączenia TCP. Serwer nie odpowiedział na czas.")
    except socket.error as e:
        print(f"Wystąpił błąd podczas łączenia TCP: {e}")