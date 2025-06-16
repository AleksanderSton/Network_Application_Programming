import socket

HOST = "127.0.0.1"
PORT = 2908
MESSAGE_LENGTH = 20

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Serwer TCP nasłuchuje na {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Połączono z klientem: {addr}")
            while True:
                data = conn.recv(MESSAGE_LENGTH)
                if not data:
                    break
                decoded_data = data.decode('utf-8').rstrip()
                print(f"Odebrano od klienta: '{decoded_data}'")

                response = f"Odebrano: {decoded_data}".encode('utf-8')
                if len(response) < MESSAGE_LENGTH:
                    response += b' ' * (MESSAGE_LENGTH - len(response))
                else:
                    response = response[:MESSAGE_LENGTH]
                conn.sendall(response)