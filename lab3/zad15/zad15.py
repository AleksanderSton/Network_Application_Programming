import socket
from lab3.zad13.zad13 import parse_udp
from lab3.zad14.zad14 import parse_tcp

if __name__ == "__main__":
    data = [0x45, 0x00, 0x00, 0x4e, 0xf7, 0xfa, 0x40, 0x00, 0x38, 0x06, 0x9d, 0x33, 0xd4, 0xb6, 0x18, 0x1b, 0xc0, 0xa8,
            0x00, 0x02, 0x0b, 0x54, 0xb9, 0xa6, 0xfb, 0xf9, 0x3c, 0x57, 0xc1, 0x0a, 0x06, 0xc1, 0x80, 0x18, 0x00, 0xe3,
            0xce, 0x9c, 0x00, 0x00, 0x01, 0x01, 0x08, 0x0a, 0x03, 0xa6, 0xeb, 0x01, 0x00, 0x0b, 0xf8, 0xe5, 0x6e, 0x65,
            0x74, 0x77, 0x6f, 0x72, 0x6b, 0x20, 0x70, 0x72, 0x6f, 0x67, 0x72, 0x61, 0x6d, 0x6d, 0x69, 0x6e, 0x67, 0x20,
            0x69, 0x73, 0x20, 0x66, 0x75, 0x6e]

    proto_version = int(data[0] >> 4)
    src_ip = '.'.join([str(x) for x in data[12:16]])
    dst_ip = '.'.join([str(x) for x in data[16:20]])
    protocol = int(data[9])

    src_port = 0
    dst_port = 0
    data_str = ""

    if protocol == 6:  # TCP
        src_port, dst_port, data_str = parse_tcp(data[20:])
    elif protocol == 17:  # UDP
        src_port, dst_port, data_str = parse_udp(data[20:])

    msg = (f"zad15odpA;\n"
           f"ver:{proto_version};\n"
           f"srcip:{src_ip};\n"
           f"dstip:{dst_ip};\n"
           f"type:{protocol}")
    print(msg)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), ('127.0.0.1', 2911))
    resp = sock.recv(1024)
    print(resp)

    if resp.decode() == "TAK":
        msg = (f"zad15odpB;srcport:{src_port};\n"
               f"dstport:{dst_port};\n"
               f"data:{data_str}")
        print(msg)
        sock.sendto(msg.encode(), ('127.0.0.1', 2911))
        print(sock.recv(1024))