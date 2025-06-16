import socket

HOST = '127.0.0.1'
PORT = 65433



if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Serwer Kalkulatora UDP nasłuchuje na {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(1024)
            message = data.decode('utf-8').strip()
            print(f"Odebrano od {addr}: '{message}'")

            result = "Błąd: Nieprawidłowy format lub operacja."
            try:
                parts = message.split()
                if len(parts) == 3:
                    num1 = float(parts[0])
                    operator = parts[1]
                    num2 = float(parts[2])

                    if operator == '+':
                        result = str(num1 + num2)
                    elif operator == '-':
                        result = str(num1 - num2)
                    elif operator == '*':
                        result = str(num1 * num2)
                    elif operator == '/':
                        if num2 != 0:
                            result = str(num1 / num2)
                        else:
                            result = "Błąd: Dzielenie przez zero."
                    else:
                        result = "Błąd: Nieznany operator. Obsługiwane: +, -, *, /"
                else:
                    result = "Błąd: Oczekiwany format: 'liczba operator liczba'"
            except ValueError:
                result = "Błąd: Nieprawidłowe liczby."
            except Exception as e:
                result = f"Wystąpił błąd serwera: {e}"

            s.sendto(result.encode('utf-8'), addr)
            print(f"Odesłano do {addr}: '{result}'")