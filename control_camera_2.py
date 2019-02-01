import socket
import sys
import datetime
from time import sleep
from picamera import PiCamera

# Create a TCP/IP socket for sensor message
sock_sensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a TCP/IP socket for camera image
sock_image = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Raspberry Pi IP address
my_ip = '192.168.1.198'

# IP Address of the laptop we are sending image to
laptop_ip = '192.168.1.192'

# Bind the socket to the port for sensor message
sensor_address = (my_ip, 10001)
print('Listening for sensor message on {} port {}'.format(*sensor_address))
sock_sensor.bind(sensor_address)

# Bind the socket to the port for image message
image_address = (laptop_ip, 10002)
print('Ready to send image on {} port {}'.format(*image_address))
sock_sensor.bind(image_address)

# Listen for incoming connections
sock_sensor.listen(1)

# Setup the camera
camera = PiCamera()

# Listen continuously
while True:

    # Wait for a connection
    print('Waiting for a sensor connection')
    connection, client_address = sock_sensor.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if data:
                #print('received {!r}'.format(data))
                print('Taking a picture')
                camera.start_preview()
                sleep(2) # Camera warm up time
                date = datetime.datetime.now()
                file_name = '/home/pi/Documents/DSSN/Pictures/' + date.strftime("%m_%d_%Y_%H_%M_%S"+ '.jpg')
                camera.capture(file_name)
                print('Done taking picture: sending it')
		try:

	            #Get the image file 
        	    image = open(file_name, 'rb')
		    bytes = image.read()
		    size = len(bytes)

		    sock.sendall("SIZE %s" % size)
		    answer = sock.recv(4096)

		    if answer == 'GOT SIZE':
			sock.sendall(bytes)

			answer = sock.recv(4096)
			if answer == 'GOT IMAGE' :
			    print('Image sent successfully')

		    image.close()

    		finally:
                    print('closing socket')
                    sock.close()

            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
