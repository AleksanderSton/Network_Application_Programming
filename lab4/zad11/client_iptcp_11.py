import socket

SERVER_HOST_VALIDATION = '212.182.24.27'
SERVER_PORT_VALIDATION = 2911


def parse_ip_packet(hex_data):
    hex_data = hex_data.replace(" ", "")
    byte_data = bytes.fromhex(hex_data)

    if len(byte_data) < 20:
        raise ValueError("Dane są za krótkie na nagłówek IP.")

    version_ihl = byte_data[0]
    version = (version_ihl >> 4) & 0xF
    ihl_words = version_ihl & 0xF
    ip_header_length_bytes = ihl_words * 4

    if len(byte_data) < ip_header_length_bytes:
        raise ValueError("Pakiet IP jest za krótki, aby zawierać pełny nagłówek IP.")

    src_ip_bytes = byte_data[12:16]
    src_ip = socket.inet_ntoa(src_ip_bytes)

    dst_ip_bytes = byte_data[16:20]
    dst_ip = socket.inet_ntoa(dst_ip_bytes)

    protocol_type = byte_data[9]

    higher_layer_data = byte_data[ip_header_length_bytes:]

    src_port = None
    dst_port = None
    payload_data_bytes = b''

    if protocol_type == 6:
        if len(higher_layer_data) < 20:
            raise ValueError("Dane TCP są za krótkie na nagłówek TCP.")

        src_port = int.from_bytes(higher_layer_data[0:2], byteorder='big')
        dst_port = int.from_bytes(higher_layer_data[2:4], byteorder='big')

        tcp_header_length_bytes = 32

        if len(higher_layer_data) < tcp_header_length_bytes:
            raise ValueError("Segment TCP jest za krótki, aby zawierać pełny nagłówek TCP z opcjami.")

        payload_data_bytes = higher_layer_data[tcp_header_length_bytes:]
    elif protocol_type == 17:
        if len(higher_layer_data) < 8:
            raise ValueError("Dane UDP są za krótkie na nagłówek UDP.")

        src_port = int.from_bytes(higher_layer_data[0:2], byteorder='big')
        dst_port = int.from_bytes(higher_layer_data[2:4], byteorder='big')
        payload_data_bytes = higher_layer_data[8:]

    return version, src_ip, dst_ip, protocol_type, src_port, dst_port, payload_data_bytes



if __name__ == "__main__":
    hex_ip_packet = "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1 80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01 00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            version, src_ip, dst_ip, protocol_type, src_port, dst_port, payload_data_bytes = parse_ip_packet(
                hex_ip_packet)

            message_a = f"zad15odpA;ver;{version};srcip;{src_ip};dstip;{dst_ip};type;{protocol_type}"
            print(f"Klient ZAD11: Wysyłana wiadomość A: '{message_a}'")
            s.sendto(message_a.encode('utf-8'), (SERVER_HOST_VALIDATION, SERVER_PORT_VALIDATION))

            s.settimeout(5)
            try:
                data_a, server_addr_a = s.recvfrom(1024)
                response_a = data_a.decode('utf-8')
                print(f"Klient ZAD11: Odebrano odpowiedź A od {server_addr_a}: {response_a}")

                if response_a == "TAK":
                    if src_port is not None and dst_port is not None:
                        payload_data_hex = payload_data_bytes.hex()
                        message_b = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{payload_data_hex}"
                        print(f"Klient ZAD11: Wysyłana wiadomość B: '{message_b}'")
                        s.sendto(message_b.encode('utf-8'), (SERVER_HOST_VALIDATION, SERVER_PORT_VALIDATION))

                        try:
                            data_b, server_addr_b = s.recvfrom(1024)
                            response_b = data_b.decode('utf-8')
                            print(f"Klient ZAD11: Odebrano odpowiedź B od {server_addr_b}: {response_b}")
                        except socket.timeout:
                            print("Klient ZAD11: Timeout - serwer nie odpowiedział na wiadomość B.")
                        except Exception as e:
                            print(f"Klient ZAD11: Błąd podczas odbierania odpowiedzi B: {e}")
                    else:
                        print(
                            "Klient ZAD11: Brak danych portów lub payloadu do wysłania wiadomości B (protokół inny niż TCP/UDP).")
                else:
                    print("Klient ZAD11: Odpowiedź A nie była 'TAK', nie wysyłam wiadomości B.")
            except socket.timeout:
                print("Klient ZAD11: Timeout - serwer nie odpowiedział na wiadomość A.")
            except Exception as e:
                print(f"Klient ZAD11: Błąd podczas odbierania odpowiedzi A: {e}")

        except ValueError as ve:
            print(f"Klient ZAD11: Błąd parsowania pakietu IP: {ve}")
        except Exception as e:
            print(f"Klient ZAD11: Wystąpił nieoczekiwany błąd: {e}")