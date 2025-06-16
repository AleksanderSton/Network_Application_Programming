#Napisz program, który z serwera ntp.task.gda.pl pobierze aktualną datę i czas, a następnie wyświetli je
#na konsoli. Serwer działa na porcie 13.
import socket


serwer = 'ntp.task.gda.pl'
port = 13

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serwer, port))
    dane = sock.recv(1024)
    czas = dane.decode('utf-8').strip()
    print(f"Aktualna data i czas: {czas}")

except Exception as e:
    print(f"Wystąpił błąd: {e}")
finally:
    sock.close()

