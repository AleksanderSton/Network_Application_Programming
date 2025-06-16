import socket

HOST = "127.0.0.1"
PORT = 2908
MSG_LENGTH = 20

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    msg = "Hello!"
    if len(msg) < MSG_LENGTH:
        msg = msg.ljust(MSG_LENGTH, " ")
    else:
        msg = msg[:MSG_LENGTH]

    sent = 0
    while sent < len(msg):
        sent += sock.send(msg[sent:].encode())

    received = 0
    data = ""
    while received < MSG_LENGTH:
        data += sock.recv(1024).decode()
        received += len(data)

    print(data)

    sock.close()