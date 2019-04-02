''' 
MainCameraCode.py
This code reads in an x,y location from the moving Raspberry Pi
and pans the camera to take a picture of it.
April 1st, 2019 - Jackie Scanlon
'''

# For talking to the Raspberry Pi
import socket

# For panning
import numpy as np
from adafruit_servokit import ServoKit

# For taking the picture
import datetime
from time import sleep
from picamera import PiCamera


def panCamera(x,y, xc, yc, beta, kit)
	# Calculates the angle the camera needs to pan to and pans there.

	# Calculate angle
	phi = numpy.arctan((x-xc)/(y-yc))
	theta = phi + beta

	# Pan to that angle
	kit.servo[0].angle = theta
	

def takePicture()
	# Takes the picture and saves it.

	# Get the camera ready
    camera.start_preview()
    
    # Camera warm up time
    sleep(2) 
    
    # Get the date to name the file
    date = datetime.datetime.now()
    date_string = date.strftime("%m_%d_%Y_%H_%M_%S")
    
    # Take the picture
    camera.capture('/home/pi/Documents/DSSN/Project/Pictures/' + date_string + '.jpg')
    print('Picture taken')


if __name__ == "__main__":

	# ------Parameters to be set-----

	# Set the location of the camera
	xc = 
	yc = 

	# Set the IP address of the camera
	camera_ip = ''

	# Set the angle of adjustment for camera
	# aka, how many degrees off the vertical
	# is the camera tilted
	beta = 45

	# -------------------------------

	# Create the camera and servokit objects and initialize
	camera = PiCamera()
	kit = ServoKit(channels=16)
	kit.servo[0].actuation_range = 180 # Default

	# Connect to moving Raspberry Pi
	sock = socet.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_address = (camera_ip, 10001)
	sock.bind(camera_address)
	sock.listen(1)

	# Continue listening for connections
	while True:

		# Wait for a connection
		print('Not Connected')
		connection, client_address = sock.accept()

		# Receive connection
		try:
			print('Connected')

			# Receive the message
			while True:
				data = connecton.recv(1024)

				if data:
					xy = data.split(',')
					x = xy[0]
					y = xy[1]

					# Pan to the correct angle
					panCamera(x,y,xc,yc,beta,kit)

					# Take the picture
					takePicture(camera) 

				else:
					print('No data received')
					break

		finally:
			# Clean up the connection
			connection.close()
