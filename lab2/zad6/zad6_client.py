#!/usr/bin/env python

import socket

HOST = '212.182.24.27'
PORT = 2902
sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UDP Client is ready to send data to the server at %s:%d" % (HOST, PORT))

try:
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            operator = input("Enter the operator (+, -, *, /): ")
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        if operator not in ['+', '-', '*', '/']:
            print("Invalid operator. Please use one of: +, -, *, /")
            continue

        message = f"{num1} {operator} {num2}"
        print(f"Sending to server: {message}")

        sockIPv4.sendto(message.encode('utf-8'), (HOST, PORT))

        data, server_address = sockIPv4.recvfrom(4096)
        response = data.decode('utf-8')
        print(f"Received response from server {server_address}: {response}")

        choice = input("Do you want to perform another calculation? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("Exiting the client.")
            break

finally:
    sockIPv4.close()