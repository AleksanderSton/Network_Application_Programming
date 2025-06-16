import socket

SERVER_HOST_VALIDATION = '212.182.24.27'
SERVER_PORT_VALIDATION = 2909


def parse_tcp_segment(hex_data):
    hex_data = hex_data.replace(" ", "")
    byte_data = bytes.fromhex(hex_data)

    if len(byte_data) < 20:
        raise ValueError("Dane są za krótkie na nagłówek TCP.")

    src_port = int.from_bytes(byte_data[0:2], byteorder='big')
    dst_port = int.from_bytes(byte_data[2:4], byteorder='big')




    header_length_bytes = 32

    if len(byte_data) < header_length_bytes:
        raise ValueError("Segment TCP jest za krótki, aby zawierać pełny nagłówek TCP z opcjami.")


    data_bytes = byte_data[header_length_bytes:]

    return src_port, dst_port, data_bytes




if __name__ == "__main__":
    hex_segment_tcp = "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee 00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"

    try:
        src_port, dst_port, data_bytes = parse_tcp_segment(hex_segment_tcp)
        data_hex = data_bytes.hex()

        message_to_server = f"zad13odp;src;{src_port};dst;{dst_port};data;{data_hex}"
        print(f"Klient ZAD10: Wydobyto - Src Port: {src_port}, Dst Port: {dst_port}, Dane (hex): {data_hex}")
        print(f"Klient ZAD10: Wysyłana wiadomość: '{message_to_server}'")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(message_to_server.encode('utf-8'), (SERVER_HOST_VALIDATION, SERVER_PORT_VALIDATION))

            s.settimeout(5)
            try:
                data, server_addr = s.recvfrom(1024)
                print(f"Klient ZAD10: Odebrano od serwera {server_addr}: {data.decode('utf-8')}")
            except socket.timeout:
                print("Klient ZAD10: Timeout - serwer nie odpowiedział.")
            except Exception as e:
                print(f"Klient ZAD10: Błąd podczas odbierania odpowiedzi: {e}")

    except ValueError as ve:
        print(f"Klient ZAD10: Błąd parsowania segmentu TCP: {ve}")
    except Exception as e:
        print(f"Klient ZAD10: Wystąpił nieoczekiwany błąd: {e}")