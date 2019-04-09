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
import sys
import datetime

# For talking to the camera
import socket

# Debugging
import time
import random


def getPower(rssi):
    # Calculate power for each anchor

    power = np.exp(rssi/10)
    
    # Clip as appropriate
    for i in range(0,3):
	if(power[i] <= .0031):
	   power[i] = .0031

    return power


def getRSSI(anchors, address, count_original):
    # Extract RSSI values for each anchor and average them

    print('\nTaking RSSI measurements - ' + str(count_original) + ' total.')
    # Will keep a running total of each of the rssi values, so that we can 
    # average later
    total = np.zeros(shape=(anchors,1))

    # Will use to throw out values that don't exist
    count = np.repeat(count_original, anchors)

    # Measurement count_original times each RSSI
    for i in range (0,count_original):

        # Display progress bar
        sys.stdout.write('\r' + str(i+1))
        sys.stdout.flush()
        time.sleep(.5)
        
        # Get the string output from the command line
        output = os.popen('sudo btmgmt find').read()
        words = output.split(' ')
        

        for j in range(0,anchors):
            rssi = int(parseOutput(words, address[j]))
            #rssi = int(random.randrange(-52, -30))

            # If none was found
            if rssi == 0:
                count[j] = count[j] - 1

            # Add onto total
            total[j] = total[j] + rssi

    print
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
        
    # Return the rssi values
    return rssi


def parseOutput(words, address):
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
    return distance
    

def getXAndY(anchors, distance, location):
    # use trilateration to get x,y coordinates

    # Get b
    b = np.zeros(shape=(anchors,1))

    for j in range(0, anchors):
        b[j] = math.pow(distance[j],2) - math.pow(location[j,0], 2) - math.pow(location[j,1],2)

    # Get A
    A = np.ones(shape=(anchors, 3))
    A[:,1:3] = -2*location

    # Perform pseudoinverse to get x and y locations (Az = b)
    z = np.matmul(np.linalg.pinv(A),b)

    # Send back
    return float(z[1]), float(z[2])


def sendToCamera(x,y):
    # Send the x and y location to the camera

    try:
        sock.sendall(str(x) + ',' + str(y))
        print('\nSent the coordinates to the camera.\n')
    finally:
        pass

def saveToFile(filepath, rssi, count_original,true_x, true_y, x,y):
    # Save the information to a csv file

    date = datetime.datetime.now()
    s = '\n' + date.strftime('%A %B %d %Y at %H:%M:%S') + ', '
    s = s + str(rssi[0,0]) + ', ' + str(rssi[1,0]) + ', ' + str(rssi[2,0]) + ', '
    s = s + str(count_original) + ', '
    s = s + str(true_x) + ', ' + str(true_y) + ', '
    s = s + str(x) + ', ' + str(y)

    with open(filepath, 'a') as file:
        file.write(s)


if __name__ == "__main__":

    #----- Parameters to be set-------

    # Set number of anchors
    anchors = 3

    # Set MAC addresses for each of the bluetooth anchors
    # These correspond to Jackie, Paul, Jeremy (I think)
    address = ['70:1C:E7:38:FC:E2', '10:4A:7D:9D:E7:EC', '5C:E0:C5:96:89:57']
    
    # Set anchor locations
    location = np.zeros(shape=(anchors, 2))
    location[0,] = [0,0]
    location[1,] = [50,0]
    location[2,] = [0,50]

    # Set the IP address of the camera 
    camera_ip = '192.168.0.18'
    #camera_ip = '129.161.221.4'

    # How many times do we want to take a measurement
    count_original = 25

    #---------------------------------

    # Save information to a file
    date = datetime.datetime.now()
    datestr = date.strftime('%Y_%m_%d_%H_%M_%S')
    filepath = 'experiment_' + datestr + '.csv'

    with open(filepath, 'a') as file:
        file.write('DSSN Project Experiment on ' + date.strftime('%A %B %d, %Y at %H:%M:%S'))
        file.write('\n\nTime, RSSI #1, RSSI #2, RSSI #3, Measurements, True X, True Y, X, Y')
    # Set up wifi communication with the camera

    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to camera
    camera_address = (camera_ip, 10001)
    sock.connect(camera_address)

    while(True):

        # Get the actual locations
        print('Enter the true x-location of the sensor node: ')
        true_x = input()
        print('\nEnter the true y-location of the sensor node: ')
        true_y = input()

        # Read in RSSIs
        rssi = getRSSI(anchors, address, count_original)
        #rssi = np.array([[-54],[-42], [-45]])
        #time.sleep(5)

        print('\nRSSIs: \n' + str(rssi))

        # If we were able to get readings to all anchors
        if rssi is not None:
            # Calculate power values
            power = getPower(rssi)
            print('\nPowers: \n' + str(power))

            # Get distances from power values
            distance = getDistance(power)
            print('\nDistances: \n' + str(distance))

            # Use trilateration to get x,y coordinates
            x, y = getXAndY(anchors, distance, location)
            print('\nX and Y coordinates: \n' + str(x) + '  ' + str(y))

            # Send x,y coordinate to camera
            sendToCamera(x,y)

            # Save to file
            saveToFile(filepath, rssi, count_original,true_x, true_y, x,y)

        # If we weren't able to get readings to all anchors
        else:
            print('Cannot find anchors. Trying again.')
                
    #except(KeyboardInterrupt):
    #    print('\n\nProgram Done.')

