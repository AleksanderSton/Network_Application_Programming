import socket
import ssl
import base64
import sys

if __name__ == "__main__":
    sender_email = input("Podaj adres e-mail nadawcy: ")
    receiver_email = input("Podaj adres e-mail odbiorcy: ")
    subject = input("Podaj temat wiadomości: ")
    body = input("Podaj treść wiadomości: ")
    filename = input("Podaj ścieżkę do pliku z obrazkiem (np. obrazek.jpg): ")
    password = input("Podaj hasło do swojego konta e-mail: ")

    smtp_server = "poczta.interia.pl"
    port = 587

    try:
        with open(filename, "rb") as f:
            file_content_b64 = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
        sys.exit(1)

    boundary = "----=_Boundary_123456789"

    message = f"""\
    From: {sender_email}
    To: {receiver_email}
    Subject: {subject}
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary="{boundary}"
    
    --{boundary}
    Content-Type: text/plain; charset="utf-8"
    Content-Transfer-Encoding: 7bit
    
    {body}
    
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


