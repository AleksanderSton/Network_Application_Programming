import socket

SERVER_HOST_VALIDATION = '127.0.0.1'

SERVER_PORT_VALIDATION = 2910


def parse_udp_datagram(hex_data):
    hex_data = hex_data.replace(" ", "")
    byte_data = bytes.fromhex(hex_data)

    if len(byte_data) < 8:
        raise ValueError("Dane są za krótkie na nagłówek UDP.")

    src_port = int.from_bytes(byte_data[0:2], byteorder='big')
    dst_port = int.from_bytes(byte_data[2:4], byteorder='big')
    udp_length = int.from_bytes(byte_data[4:6], byteorder='big')

    data_bytes = byte_data[8:udp_length]

    return src_port, dst_port, data_bytes



if __name__ == "__main__":
    hex_datagram = "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e"

    try:
        src_port, dst_port, data_bytes = parse_udp_datagram(hex_datagram)
        data_hex = data_bytes.hex()

        message_to_server = f"zad14odp;src;{src_port};dst;{dst_port};data;{data_hex}"
        print(f"Klient ZAD9: Wydobyto - Src Port: {src_port}, Dst Port: {dst_port}, Dane (hex): {data_hex}")
        print(f"Klient ZAD9: Wysyłana wiadomość: '{message_to_server}'")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(message_to_server.encode('utf-8'), (SERVER_HOST_VALIDATION, SERVER_PORT_VALIDATION))

            s.settimeout(5)
            try:
                data, server_addr = s.recvfrom(1024)
                print(f"Klient ZAD9: Odebrano od serwera {server_addr}: {data.decode('utf-8')}")
            except socket.timeout:
                print("Klient ZAD9: Timeout - serwer nie odpowiedział.")
            except Exception as e:
                print(f"Klient ZAD9: Błąd podczas odbierania odpowiedzi: {e}")

    except ValueError as ve:
        print(f"Klient ZAD9: Błąd parsowania datagramu: {ve}")
    except Exception as e:
        print(f"Klient ZAD9: Wystąpił nieoczekiwany błąd: {e}")
