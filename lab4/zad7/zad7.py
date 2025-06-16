import socket

HOST = '127.0.0.1'
PORT = 2900
MAX_MSG_LENGTH = 20

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer Echo (limit {MAX_MSG_LENGTH} znaków) nasłuchuje na {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Połączono z {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    decoded_message = data.decode('utf-8')
                    original_length = len(decoded_message)

                    if len(decoded_message) > MAX_MSG_LENGTH:
                        truncated_message = decoded_message[:MAX_MSG_LENGTH]
                        print(
                            f"Odebrano od klienta (oryginalna dł. {original_length}): '{decoded_message}' - Wiadomość obcięta do: '{truncated_message}'")
                    else:
                        truncated_message = decoded_message
                        print(f"Odebrano od klienta: '{truncated_message}'")

                    conn.sendall(truncated_message.encode('utf-8'))
                    print(f"Odesłano do klienta: '{truncated_message}'")
            print(f"Rozłączono z {addr}")