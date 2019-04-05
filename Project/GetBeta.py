# For panning

from adafruit_servokit import ServoKit

# For taking the picture
from picamera import PiCamera

# Create the camera and servokit objects and initialize
camera = PiCamera()
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 180 # Default

# Get the camera ready
camera.start_preview(fullscreen=False,window=(100,200,300,400))

print('Enter beta (0-180)')
while True:
	beta = input()
	kit.servo[0].angle = int(beta)