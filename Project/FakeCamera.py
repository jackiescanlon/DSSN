import numpy as np 
import math

import socket

camera_ip = '129.161.139.98'

# Connect to moving Raspberry Pi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
camera_address = (camera_ip, 10001)
sock.bind(camera_address)
sock.listen(1)

while True:

	# Wait for a connection
	print('Not Connected')
	connection, client_address = sock.accept()

	# Receive connection
	try:
		print('Connected')

		# Receive the message
		while True:
			data = connection.recv(1024)

			if data:
				xy = str(data).split(',')
				x = float(xy[0])
				y = float(xy[1])

				print(x)
				print(y)

			else:
				print('No data received')
				break

	finally:
		# Clean up the connection
		connection.close()