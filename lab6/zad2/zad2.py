import socket
import ssl
import base64

if __name__ == "__main__":
    port = 587
    smtp_server = "poczta.interia.pl"
    sender_email = "pas2025inf2@interia.pl"
    password = "V*ij8Hk%xqLq&Q5MaW3Bh3v%4X"

    receiver_emails = [
        "pas2025inf@interia.pl",
        "pas2025inf3@interia.pl",
    ]

    client_socket = socket.create_connection((smtp_server, port))
    recv = client_socket.recv(1024).decode()
    print(recv)

    client_socket.send(b"EHLO interia.pl\r\n")
    recv = client_socket.recv(1024).decode()
    print(recv)

    client_socket.send(b"STARTTLS\r\n")
    recv = client_socket.recv(1024).decode()
    print(recv)

    context = ssl.create_default_context()
    socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

    socket.send(b"EHLO interia.pl\r\n")
    recv = socket.recv(1024).decode()
    print(recv)

    login_b64 = base64.b64encode(sender_email.encode()).decode()
    password_b64 = base64.b64encode(password.encode()).decode()

    socket.send(b"AUTH LOGIN\r\n")
    recv = socket.recv(1024).decode()
    print(recv)

    socket.send((login_b64 + "\r\n").encode())
    recv = socket.recv(1024).decode()
    print(recv)

    socket.send((password_b64 + "\r\n").encode())
    recv = socket.recv(1024).decode()
    print(recv)

    socket.send(f"MAIL FROM:<{sender_email}>\r\n".encode())
    recv = socket.recv(1024).decode()
    print(recv)

    for receiver_email in receiver_emails:
        socket.send(f"RCPT TO:<{receiver_email}>\r\n".encode())
        recv = socket.recv(1024).decode()
        print(recv)

    socket.send(b"DATA\r\n")
    recv = socket.recv(1024).decode()

    print(recv)
    message = f"""\
    From: {sender_email}
    To: {', '.join(receiver_emails)}
    Subject: Test ESMTP przez Telnet

    Ta wiadomość została wysłana przez ESMTP na serwerze Interia.
    .
    """
    socket.send(message.encode())
    socket.send(b"\r\n.\r\n")
    recv = socket.recv(1024).decode()
    print(recv)
    socket.send(b"QUIT\r\n")
    recv = socket.recv(1024).decode()
    print(recv)

    socket.close()

