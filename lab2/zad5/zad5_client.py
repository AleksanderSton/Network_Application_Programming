#!/usr/bin/env python

import socket

HOST = '127.0.0.1'
PORT = 2901

sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UDP Client is ready to send messages to the server at %s:%d" % (HOST, PORT))

try:
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")

        if message.lower() == 'exit':
            print("Exiting the client.")
            break

        sockIPv4.sendto(message.encode('utf-8'), (HOST, PORT))

        data, server_address = sockIPv4.recvfrom(4096)
        print("Received response from server %s: %s" % (server_address, data.decode('utf-8')))

finally:
    sockIPv4.close()