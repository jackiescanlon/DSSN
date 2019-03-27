# This is the main code to be run on the Raspberry Pi Zero.
# It will read in messages from the trip sensor and PIR sensor,
# and tell the Pi to take a picture.

# Imports for the sensors
import RPi.GPIO as GPIO
import time

# Imports for the TCP/IP Connection
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# Should have IP address of the Raspberry Pi (NOT the Zero)
server_address = ('192.168.1.73', 10001)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Configure the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

PIRPin = 7
TripPin = 5
TripPinLED = 11
GPIO.setup(PIRPin, GPIO.IN)
GPIO.setup(TripPin,GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(TripPinLED, GPIO.OUT)

def sendMessage(pin):

    try:
        print('Motion detected. Sending message to Raspberry Pi')
        
        # Send data
        message = 'Take a picture!'
        sock.sendall(message)
    finally:
	print('Sent message to Raspberry Pi')

print("Motion Sensor Alarm (CTRL+C to exit)")
time.sleep(1)
print("Ready")

try:
    GPIO.add_event_detect(PIRPin, GPIO.RISING, callback=sendMessage)
    while(True):
        GPIO.output(TripPinLED, GPIO.HIGH)
        if(GPIO.input(TripPin) == GPIO.LOW):
	    sendMessage(TripPin)

        time.sleep(2)
finally:
    print('Closing socket')
    sock.close()
    GPIO.cleanup()
