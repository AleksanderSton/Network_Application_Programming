import socket
import ssl
import base64

if __name__ == "__main__":
    port = 587
    smtp_server = "poczta.interia.pl"
    sender_email = "pas2025inf2@interia.pl"
    receiver_email = "pas2025inf@interia.pl"
    password = "V*ij8Hk%xqLq&Q5MaW3Bh3v%4X"

    filename = "test.jpg"
    with open(filename, "rb") as f:
        file_content_b64 = base64.b64encode(f.read()).decode()

    boundary = "----=_Boundary_123456789"

    message = f"""\
    From: {sender_email}
    To: {receiver_email}
    Subject: Test ESMTP z obrazkiem
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary="{boundary}"
    
    --{boundary}
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    
    Ta wiadomość z załącznikiem została wysłana przez ESMTP na serwerze Interia.
    
    --{boundary}
    Content-Type: image/jpeg; name="{filename}"
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename="{filename}"
    
    {file_content_b64}
    
    --{boundary}--
    """
    client_socket = socket.create_connection((smtp_server, port))
    print(client_socket.recv(1024).decode())

    client_socket.send(b"EHLO interia.pl\r\n")
    print(client_socket.recv(1024).decode())

    client_socket.send(b"STARTTLS\r\n")
    print(client_socket.recv(1024).decode())

    context = ssl.create_default_context()
    socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

    socket.send(b"EHLO interia.pl\r\n")
    print(socket.recv(1024).decode())

    login_b64 = base64.b64encode(sender_email.encode()).decode()
    password_b64 = base64.b64encode(password.encode()).decode()

    socket.send(b"AUTH LOGIN\r\n")
    print(socket.recv(1024).decode())

    socket.send((login_b64 + "\r\n").encode())
    print(socket.recv(1024).decode())

    socket.send((password_b64 + "\r\n").encode())
    print(socket.recv(1024).decode())

    socket.send(f"MAIL FROM:<{sender_email}>\r\n".encode())
    print(socket.recv(1024).decode())

    socket.send(f"RCPT TO:<{receiver_email}>\r\n".encode())
    print(socket.recv(1024).decode())

    socket.send(b"DATA\r\n")
    print(socket.recv(1024).decode())

    socket.send((message + "\r\n.\r\n").encode())
    print(socket.recv(1024).decode())

    socket.send(b"QUIT\r\n")
    print(socket.recv(1024).decode())

    socket.close()

