import socket
import ssl
import base64

if __name__ == "__main__":
    sender_email = "pas2025inf2@interia.pl"
    receiver_email = "pas2025inf@interia.pl"
    password = "V*ij8Hk%xqLq&Q5MaW3Bh3v%4X"
    subject = input("Podaj temat wiadomości: ")
    body = input("Podaj treść wiadomości (HTML): ")
    # sender_email = input("Podaj adres e-mail nadawcy: ")
    # receiver_email = input("Podaj adres e-mail odbiorcy: ")
    # password = input("Podaj hasło do swojego konta e-mail: ")

    smtp_server = "poczta.interia.pl"
    port = 587

    boundary = "----=_Boundary_123456789"

    message = f"""\
    From: {sender_email}
    To: {receiver_email}
    Subject: {subject}
    MIME-Version: 1.0
    Content-Type: multipart/alternative; boundary="{boundary}"
    
    --{boundary}
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    
    Ta wiadomość została wysłana przez ESMTP na serwerze Interia. Jeśli nie widzisz wersji HTML, to znaczy, że Twoja poczta nie obsługuje HTML.
    
    --{boundary}
    Content-Type: text/html; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    
    <html>
        <head>
            <title>{subject}</title>
        </head>
        <body>
            <h1>{subject}</h1>
            <p><b>{body}</b></p>
            <p><i>{body}</i></p>
            <p><u>{body}.</u></p>
            <p>Przykład <a href="http://www.example.com">linku</a> w treści wiadomości.</p>
            <p>Możesz dodać inne tagi HTML do wiadomości, jak <span style="color: red;">kolorowany tekst</span>, <code>kod</code>, itd.</p>
        </body>
    </html>
    
    --{boundary}--
    """

    client_socket = socket.create_connection((smtp_server, port))
    print(client_socket.recv(1024).decode())

    client_socket.send(b"EHLO interia.pl\r\n")
    print(client_socket.recv(1024).decode())

    client_socket.send(b"STARTTLS\r\n")
    print(client_socket.recv(1024).decode())

    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

    secure_socket.send(b"EHLO interia.pl\r\n")
    print(secure_socket.recv(1024).decode())

    login_b64 = base64.b64encode(sender_email.encode()).decode()
    password_b64 = base64.b64encode(password.encode()).decode()

    secure_socket.send(b"AUTH LOGIN\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send((login_b64 + "\r\n").encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send((password_b64 + "\r\n").encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(f"MAIL FROM:<{sender_email}>\r\n".encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(f"RCPT TO:<{receiver_email}>\r\n".encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(b"DATA\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send((message + "\r\n.\r\n").encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(b"QUIT\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.close()

