import socket
import shutil
import re

HOST = '127.0.0.1'
PORT = 2904
server_address = (HOST, PORT)

# zad1
print(f"Zadanie 1")
source_txt = input(f"Podaj nazwę pliku tekstowego: ")
destination_txt = "lab1zad1.txt"

try:
    with open(source_txt, 'r') as source_file:
        with open(destination_txt, 'w') as destination_file:
            destination_file.write(source_file.read())
except FileNotFoundError:
    print(f"Plik '{source_txt}' nie istnieje")
except Exception as e:
    print(f"Wystąpił błąd: {e}")

# zad2
print(f"Zadanie 2")
source_png = input(f"Podaj nazwe pliku png: ")
destination_png = "lab1zad1.png"

try:
    shutil.copy(source_png, destination_png)
except Exception as e:
    print(f"Wystąpił błąd: {e}")

#zad3
print(f"Zadanie 3")
ip_address = input(f"Podaj adres IP do sprawdzenia: ")
pattern = r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"

if re.match(pattern, ip_address):
    print(f"Adres IP jest poprawny!")
else:
    print(f"Adres IP jest niepoprawny!")

#zad 4
print(f"Zadanie 4")
try:
    hostname = socket.gethostbyaddr(ip_address)[0]
    print(f"Nazwa hosta: {hostname}")
except Exception as e:
    print(f"Wystąpił błąd: {e}")

#zad 5
print(f"Zadanie 5")
hostname = input(f"Podaj nazwę hosta: ")

try:
    ip_address = socket.gethostbyname(hostname)
    print(f"Adres IP hosta: {ip_address}")
except Exception as e:
    print(f"Wystąpił błąd: {e}")

#zad 6
print(f"Zadanie 6")
hostname = input(f"Podaj nazwę hosta: ")
port = int(input(f"Podaj numer portu: "))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname,port))
        print(f"Połączono z {hostname}:{port}")
        sock.close()
except Exception as e:
    print(f"Wystąpił błąd: {e}")


#zad 7
print(f"Zadanie 7")
hostname = input(f"Podaj nazwę hosta: ")
start_port = int(input("Podaj numer portu początkowego: "))
end_port = int(input("Podaj numer portu końcowego: "))

try:
    if start_port<1 or end_port >65535 or start_port > end_port:
        raise ValueError
except ValueError:
    print(f"Porty muszą być liczbami z zakresu 1-65535, a początkowy port musi być mniejszy niż końcowy!")

for port in range(start_port, end_port+1):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((hostname,port))
        if result == 0:
            print(f"Port {port} jest otwarty")
        else:
            print(f"Port {port} jest zamknięty")
sock.close()