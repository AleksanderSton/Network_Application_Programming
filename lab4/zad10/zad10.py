import socket

HOST_SERVER_ZAD10 = '127.0.0.1'
PORT_SERVER_ZAD10 = 2909


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST_SERVER_ZAD10, PORT_SERVER_ZAD10))
        print(f"Serwer ZAD10 (Walidacja TCP) nasłuchuje na {HOST_SERVER_ZAD10}:{PORT_SERVER_ZAD10}")

        expected_src_port = 2900
        expected_dst_port = 35211
        expected_data_hex = "68656c6c6f203a29"
        expected_data_bytes = bytes.fromhex(expected_data_hex)

        while True:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8').strip()
            print(f"ZAD10: Odebrano od {addr}: '{message}'")

            response = "BAD SYNTAX"
            try:
                parts = message.split(';')
                if len(parts) == 7 and parts[0] == "zad14odp" and \
                        parts[1] == "src" and parts[3] == "dst" and parts[5] == "data":

                    client_src_port = int(parts[2])
                    client_dst_port = int(parts[4])
                    client_data_hex = parts[6]
                    client_data_bytes = bytes.fromhex(client_data_hex)

                    if client_src_port == expected_src_port and \
                            client_dst_port == expected_dst_port and \
                            client_data_bytes == expected_data_bytes:
                        response = "TAK"
                    else:
                        response = "NIE"
                else:
                    response = "BAD SYNTAX"
            except (ValueError, IndexError):
                response = "BAD SYNTAX"
            except Exception as e:
                response = f"Błąd serwera: {e}"

            s.sendto(response.encode('utf-8'), addr)
            print(f"ZAD10: Odesłano do {addr}: '{response}'")