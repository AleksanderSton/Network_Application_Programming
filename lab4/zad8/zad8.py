import socket

HOST = '127.0.0.1'
PORT = 2900
MAX_MSG_LENGTH = 20
MAX_MSG_BYTES = MAX_MSG_LENGTH * 4


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
                    data = conn.recv(MAX_MSG_BYTES)
                    if not data:
                        break

                    decoded_message = data.decode('utf-8')
                    original_received_bytes = len(data)

                    response_message = ""
                    if len(decoded_message) > MAX_MSG_LENGTH:
                        truncated_message = decoded_message[:MAX_MSG_LENGTH]
                        response_message = f"Odebrano {original_received_bytes}B. Obcięto do {MAX_MSG_LENGTH} zn.: '{truncated_message}'"
                        message_to_send = truncated_message
                        print(
                            f"Serwer: Odebrano za długą wiadomość od {addr} (oryg. dł. znaków: {len(decoded_message)}, bajtów: {original_received_bytes}). Odesłano obciętą: '{truncated_message}'")
                    else:
                        message_to_send = decoded_message
                        response_message = f"Odebrano {original_received_bytes}B. Odesłano: '{message_to_send}'"
                        print(
                            f"Serwer: Odebrano wiadomość od {addr} (dł. znaków: {len(decoded_message)}, bajtów: {original_received_bytes}). Odesłano: '{message_to_send}'")

                    conn.sendall(message_to_send.encode('utf-8'))
            print(f"Rozłączono z {addr}")