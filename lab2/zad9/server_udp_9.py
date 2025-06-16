import socket

HOST = "127.0.0.1"
PORT = 2906

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"Serwer UDP nasłuchuje na {HOST}:{PORT}")
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Odebrano od {addr}: {data.decode()}")
            odpowiedz = f"Odebrano: {data.decode()}".encode()
            sock.sendto(odpowiedz, addr)