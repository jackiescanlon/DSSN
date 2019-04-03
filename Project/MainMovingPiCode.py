''' 
MainMovingPiCode.py
This code reads in bluetooth data and converts it to 
its current x, y position via RSSI signals and trilateration.
April 1st, 2019 - Jackie Scanlon
'''

# For reading in RSSI info and converting it
import os
import numpy as np
import math

# For talking to the camera
import socket
#import sys


def getPower(rssi):
    # Calculate power for each anchor

    power = np.exp(rssi/10)
    
    for i in range(0,3):
	if(power[i] <= .0031):
	   power[i] = .0031

    return power


def getRSSI(anchors):
    # Extract RSSI values for each anchor and average them

    # Set MAC addresses for each of the bluetooth anchors
    address = ['70:1C:E7:38:FC:E2', '10:4A:7D:9D:E7:EC', '5C:E0:C5:96:89:57']

    # Will keep a running total of each of the rssi values, so that we can 
    # average later
    total = np.zeros(shape=(anchors,1))

    # How many times do we want to take a measurement
    count_original = 25

    # Will use to throw out values that don't exist
    count = np.repeat(count_original, anchors)

    # Measurement count_original times each RSSI
    for i in range (0,count_original):

        # Get the string output from the command line
        output = os.popen('sudo btmgmt find').read()
        words = output.split(' ')

        for j in range(0,anchors):
            rssi = int(ParseOutput(words, address[j]))

            # If none was found
            if rssi == 0:
                count[j] = count[j] - 1

            # Add onto total
            total[j] = total[j] + rssi

    rssi = np.zeros(shape=(anchors,1))

    # Get averages
    for j in range(0, anchors):

        # If we weren't able to get a single reading from one of the anchors, quit
        if count[j] == 0:
            rssi = None
            break

        # Otherwise, get an average
        else:
            rssi[j] = total[j]/count[j]

    print('RSSI: ')
    print(rssi)
        
    # Return the rssi values
    return rssi


def ParseOutput(words, address):
    # Convert string of text into substrings of RSSI values

    try: 
        start = words.index(address)
        rssi = words[start + 4]
    except: 
        rssi = 0
    return rssi


def getDistance(power):
    # Converts power value into a distance measurement

    distance = 13 + np.sqrt(.3/(power-.003))
    print('distance')
    print(distance)
    return distance
    

def getXAndY(anchors, distance, location):
    # use trilateration to get x,y coordinates

    # Get b
    b = np.zeros(shape=(anchors,1))

    for j in range(0, anchors):
        b[j] = math.pow(distance[j],2) - math.pow(location[j,0], 2) - math.pow(location[j,1],2)
 
    print('b')
    print(b)   
    # Get A
    #A = np.ones(shape=(anchors, 3))
    A = np.matrix([[1.,0,0],[1,-100,0],[1,0,-100]])
    print('A')
    print(A)
    # Perform pseudoinverse to get x and y locations (Az = b)
    z = np.linalg.inv(A.T*A)*A.T*b

    print('z-location')
    print(z)
    # Send back
    return z[1], z[2]


def sendToCamera(x,y):
    # Send the x and y location to the camera

    try:
        sock.sendall(str(x) + ',' + str(y))
    finally:
        pass


if __name__ == "__main__":

    #----- Parameters to be set-------

    # Set number of anchors
    anchors = 3

    # Set anchor locations
    location = np.zeros(shape=(anchors, 2))
    location[0,] = [0,0]
    location[1,] = [50,0]
    location[2,] = [0,50]

    # Set the IP address of the camera 
    camera_ip = '192.168.0.18'

    #---------------------------------

    # Set up wifi communication with the camera

    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to camera
    camera_address = (camera_ip, 10001)
    sock.connect(camera_address)

    while(True):

        # Read in RSSIs
        rssi = getRSSI(anchors)

        # If we were able to get readings to all anchors
        if rssi != None:
            # Calculate power values
            power = getPower(rssi)

            # Get distances from power values
            distance = getDistance(power)

            # Use trilateration to get x,y coordinates
            x, y = getXAndY(anchors, distance, location)

            # Send x,y coordinate to camera
            sendToCamera(x,y)

        # If we weren't able to get readings to all anchors
        else:
            print('Cannot find anchors. Trying again.')
                
    #except(KeyboardInterrupt):
    #    print('\n\nProgram Done.')

