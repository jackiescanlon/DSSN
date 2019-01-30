import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('129.161.136.200', 20001)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Put the sensor detection code here
# while loop of some sort
# if sensor is triggered
if True:
    try:

        # Send data
        message = 'Take a picture!'
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response, which is "Pos" or "Neg"
        amount_received = 0
        amount_expected = 3

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()