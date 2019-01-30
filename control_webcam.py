import socket
import sys
import datetime
from time import sleep
import cv2

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('129.161.136.200', 20001)  #Port 1000 (can be changed), and the IP address can chnge
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

camera = cv2.VideoCapture(0)
cv2.namedWindow("Preview")
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print('received {!r}'.format(data))
            if data:
                print('Taking a picture')
                #camera.start_preview()
                sleep(2) # Camera warm up time
                date = datetime.datetime.now()
                date_string = date.strftime("%m_%d_%Y_%H_%M_%S")
                print(date_string)
                #camera.capture('~/camera_captures/' + date_string + '.jpg')
                return_value, image = camera.read()
                print(return_value)
                cv2.imwrite('home/jackie/camera_captures/' + date_string + '.png', image)
                print('Done taking picture')
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
        camera.release()

        cv2.destroyAllWindows()