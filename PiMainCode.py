# This code is the main program that will run on the Raspberry Pi.
# It will listen for messages from the Zero.
# It will trigger the camera when necessary.

# Imports for talking over TCP/IP connection
import socket
import sys

# Imports for taking a picture
import datetime
from time import sleep
from picamera import PiCamera

# Imports for sending the text message
import smtplib

def send_mail(): #the texting portion
    print "Sending text"
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print header
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(GMAIL_USER,TO,msg)
    server.quit()
    time.sleep(1)
    print "Text sent"
    
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port. 
# This is the IP address of the Pi
server_address = ('192.168.1.73', 10001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Create the camera object
camera = PiCamera()

# Constants for SMS text
TO='6316556084@vtext.com'
GMAIL_USER='dssn2019@gmail.com'
PASS='ricky250'

SUBJECT = 'Alert!'
TEXT = 'Your Raspberry Pi detected an intruder!'
    
# Continue listening for connections
while True:
    # Wait for a connection
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    
    # Receive the connection from the Zero
    try:
        print('Connection from', client_address)

        # Receive the message (don't care what it is)
        while True:
            data = connection.recv(1024)
            if data:
            
                print('Taking a picture')
                
                # Get the camera ready
                camera.start_preview()
                # Camera warm up time
                sleep(2) 
                # Get the date to name the file
                date = datetime.datetime.now()
                date_string = date.strftime("%m_%d_%Y_%H_%M_%S")
                # Take the picture
                camera.capture('/home/pi/Documents/DSSN/Pictures/' + date_string + '.jpg')
                print('Done taking picture')
                
                send_mail()
            else:
                print('No data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()

