import socket
import ssl
import base64

if __name__ == "__main__":
    smtp_server = "poczta.interia.pl"
    port = 587

    username = "pas2025inf2@interia.pl"
    password = "V*ij8Hk%xqLq&Q5MaW3Bh3v%4X"

    sender = username
    receiver = "pas2025inf@interia.pl"
    display_name = "fdsgffds"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((smtp_server, port))
    print(client_socket.recv(1024).decode())

    client_socket.send(b"EHLO interia.pl\r\n")
    print(client_socket.recv(1024).decode())

    client_socket.send(b"STARTTLS\r\n")
    print(client_socket.recv(1024).decode())

    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)
    secure_socket.send(b"EHLO interia.pl\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send(b"AUTH LOGIN\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send(base64.b64encode(username.encode()) + b"\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send(base64.b64encode(password.encode()) + b"\r\n")
    print(secure_socket.recv(1024).decode())
    secure_socket.send(f"MAIL FROM:<{sender}>\r\n".encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(f"RCPT TO:<{receiver}>\r\n".encode())
    print(secure_socket.recv(1024).decode())

    secure_socket.send(b"DATA\r\n")
    print(secure_socket.recv(1024).decode())

    message = f"""From: {display_name} <{sender}>
    To: {receiver}
    Subject: Test legalnej wiadomości

    To jest test. Nagłówek From jest zgodny z MAIL FROM.
    .  
    """
    secure_socket.send(message.encode())
    secure_socket.send(b"\r\n.\r\n")
    print(secure_socket.recv(1024).decode())

    secure_socket.send(b"QUIT\r\n")
    print(secure_socket.recv(1024).decode())
    secure_socket.close()

