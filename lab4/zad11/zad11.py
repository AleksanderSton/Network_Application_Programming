import socket

HOST_SERVER_ZAD11 = '127.0.0.1'
PORT_SERVER_ZAD11 = 2911




if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST_SERVER_ZAD11, PORT_SERVER_ZAD11))
        print(f"Serwer ZAD11 (Walidacja IP/TCP) UDP nasłuchuje na {HOST_SERVER_ZAD11}:{PORT_SERVER_ZAD11}")

        expected_ver = 4
        expected_src_ip = "212.182.24.27"
        expected_dst_ip = "192.168.0.2"
        expected_protocol_type = 6  # TCP

        expected_tcp_src_port = 2900
        expected_tcp_dst_port = 47526
        expected_tcp_data_hex = "6e6574776f726b2070726f6772616d6d696e672069732066756e"
        expected_tcp_data_bytes = bytes.fromhex(expected_tcp_data_hex)

        while True:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8').strip()
            print(f"ZAD11: Odebrano od {addr}: '{message}'")

            response = "BAD SYNTAX"
            try:
                parts = message.split(';')
                if len(parts) > 0:
                    if parts[0] == "zad15odpA":
                        if len(parts) == 9 and parts[1] == "ver" and parts[3] == "srcip" and \
                                parts[5] == "dstip" and parts[7] == "type":

                            client_ver = int(parts[2])
                            client_src_ip = parts[4]
                            client_dst_ip = parts[6]
                            client_protocol_type = int(parts[8])

                            if client_ver == expected_ver and \
                                    client_src_ip == expected_src_ip and \
                                    client_dst_ip == expected_dst_ip and \
                                    client_protocol_type == expected_protocol_type:
                                response = "TAK"
                            else:
                                response = "NIE"
                        else:
                            response = "BAD SYNTAX"
                    elif parts[0] == "zad15odpB":
                        if len(parts) == 7 and parts[1] == "srcport" and \
                                parts[3] == "dstport" and parts[5] == "data":

                            client_src_port = int(parts[2])
                            client_dst_port = int(parts[4])
                            client_data_hex = parts[6]
                            client_data_bytes = bytes.fromhex(client_data_hex)

                            if client_src_port == expected_tcp_src_port and \
                                    client_dst_port == expected_tcp_dst_port and \
                                    client_data_bytes == expected_tcp_data_bytes:
                                response = "TAK"
                            else:
                                response = "NIE"
                        else:
                            response = "BAD SYNTAX"
                    else:
                        response = "BAD SYNTAX"
                else:
                    response = "BAD SYNTAX"
            except (ValueError, IndexError):
                response = "BAD SYNTAX"
            except Exception as e:
                response = f"Błąd serwera: {e}"

            s.sendto(response.encode('utf-8'), addr)
            print(f"ZAD11: Odesłano do {addr}: '{response}'")