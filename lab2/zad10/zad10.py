import socket

HOST = "127.0.0.1"
PORT = 2907

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto("google.com".encode(), (HOST, PORT))

    data = sock.recv(1024).decode()
    print(data)

    sock.close()