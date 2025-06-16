import socket

HOST = '127.0.0.1'
PORT = 65432

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Serwer Echo UDP nasłuchuje na {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(1024)
            print(f"Odebrano od {addr}: {data.decode('utf-8')}")

            s.sendto(data, addr)
            print(f"Odesłano do {addr}: {data.decode('utf-8')}")
