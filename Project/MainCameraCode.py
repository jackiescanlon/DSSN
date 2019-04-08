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
import math

# For taking the picture
import datetime
from time import sleep
from picamera import PiCamera


def panCamera(x,y, xc, yc, beta, kit):
	# Calculates the angle the camera needs to pan to and pans there.

	# Calculate angle
	phi = np.arctan((x-xc)/(y-yc))*180/math.pi
	theta = phi + beta
	print('x: ' + str(x) + '  y:' + str(y))
	print('Panning to angle theta: ' + str(theta))

	# Pan to that angle
	kit.servo[0].angle = theta
	

def takePicture(camera):
	# Takes the picture and saves it.

	# Get the camera ready
    camera.start_preview(fullscreen=False,window=(100,200,300,400))
    
    # Camera warm up time
    sleep(2) 
    
    # Get the date to name the file
    date = datetime.datetime.now()
    date_string = date.strftime("%m_%d_%Y_%H_%M_%S")
    
    # Take the picture
    camera.capture('/home/pi/Documents/DSSN/Project/Pictures/' + date_string + '.jpg')
    print('Picture taken as ' + date_string + '.jpg')


if __name__ == "__main__":

	# ------Parameters to be set-----

	# Set the location of the camera
	xc = 50
	yc = 50

	# Set the IP address of the camera
	camera_ip = '192.168.0.14'

	# Set the angle of adjustment for camera
	# aka, how many degrees off the vertical
	# is the camera tilted
	beta = 85

	# -------------------------------

	# Create the camera and servokit objects and initialize
	camera = PiCamera()
	kit = ServoKit(channels=16)
	kit.servo[0].actuation_range = 180 # Default

	# Move the camera to 0
	kit.servo[0].angle = 0

	# Connect to moving Raspberry Pi
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_address = (camera_ip, 10003)
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
				data = connection.recv(1024)

				if data:
					xy = str(data.decode()).split(',')
					x = float(xy[0])
					y = float(xy[1])

					print('Received x,y data as: ' + str(x) + ', ' + str(y))
					
					# Pan to the correct angle
					panCamera(x,y,xc,yc,beta,kit)

					# Take the picture
					takePicture(camera) 

					# Move the camera to 0
					kit.servo[0].angle = 0

				else:
					print('No data received')
					break

		finally:
			# Clean up the connection
			connection.close()
