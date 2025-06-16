import socket

HOST = "127.0.0.1"
PORT = 2911

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"Serwer UDP nasłuchuje na {HOST}:{PORT}")

        while True:
            data, addr = sock.recvfrom(1024)
            decoded_data = data.decode()
            print(f"Odebrano od {addr}: {decoded_data}")

            if decoded_data.startswith("zad15odpA"):
                response = "TAK".encode()
                sock.sendto(response, addr)
                print(f"Wysłano odpowiedź: {response.decode()} do {addr}")

                data_b, addr_b = sock.recvfrom(1024)
                decoded_data_b = data_b.decode()
                print(f"Odebrano od {addr_b}: {decoded_data_b}")
                response_b = "OK".encode()
                sock.sendto(response_b, addr_b)
                print(f"Wysłano odpowiedź: {response_b.decode()} do {addr_b}")
            else:
                response = "Nieznana komenda".encode()
                sock.sendto(response, addr)
                print(f"Wysłano odpowiedź: {response.decode()} do {addr}")