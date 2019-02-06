import socket
import sys
import datetime
from time import sleep
from picamera import PiCamera

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.1.198', 10001)  #Port 1000 (can be changed), and the IP address can chnge
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

camera = PiCamera()
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if data:
                print('received {!r}'.format(data))
                print('Taking a picture')
                camera.start_preview()
                sleep(2) # Camera warm up time
                date = datetime.datetime.now()
                date_string = date.strftime("%m_%d_%Y_%H_%M_%S")
                camera.capture('/home/pi/Documents/DSSN/Pictures/' + date_string + '.jpg')
                print('Done taking picture')
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
