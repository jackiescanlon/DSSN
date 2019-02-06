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
server_address = ('192.168.1.198', 10001)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Configure the GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

PIRPin = 13 
TripPin = 7

GPIO.setup(PIRPin, GPIO.IN)
GPIO.setup(TripPin,GPIO.IN, pull_up_down=GPIO.PUD_UP) 


def sendMessage(PIRpin):

    try:
        print('Motion detected. Sending message to Raspberry Pi')
        
        # Send data
        message = 'Take a picture!'
        sock.sendall(message)

        '''# Look for the response, which is "Pos" or "Neg"
        amount_received = 0
        amount_expected = 3

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print('Received {!r}'.format(data))''''

    finally:
        print('Closing socket')
        sock.close()

print("Motion Sensor Alarm (CTRL+C to exit)")
time.sleep(2)
print("Ready")

try:
    GPIO.add_event_detect(PIRpin, GPIO.RISING, callback=sendMessage)
    GPIO.add_event_detect(TripPin, GPIO.FALLING, callback=sendMessage)
    while(True):
        sleep(1)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
