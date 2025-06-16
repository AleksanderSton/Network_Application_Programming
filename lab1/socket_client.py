#!/usr/bin/env python
import socket

HOST = '127.0.0.1'
PORT = 2904
server_address = (HOST, PORT)

# TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# UDP
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(server_address)
try:
	# TCP
	sock.send("TEXT")
	# UDP
	# sock.sendto(message, server_address)
	
	# TCP
	answer = sock.recv(1024)
	# UDP
	# answer, server = sock.recvfrom(4096)

	print(answer)

except Exception as e:
	print(f"{e}")

sock.close()
