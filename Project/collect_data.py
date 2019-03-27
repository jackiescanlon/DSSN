import time
import os
from datetime import datetime
WIFI_SCAN_CMD ='sudo iwlist wlan0 scan | grep -E ESSID\|Signal\ level'
file  = open('new_location_r2.txt', 'w')
for x in range(101):
    scan_rst = os.popen(WIFI_SCAN_CMD).read()
    tm = datetime.now().time()
    string_time  = 'Time = ' + str(tm) + ' \n' # Get the real-time time and convert it to string
    # writes acquired data into a text file for later operations
    file.write(string_time)
    file.write(scan_rst)
    time.sleep(0.5) #sleep for 0.5 seconds
    # Used to check progress while code was running
    print(x)
    if x == 100:
        print ('Complete')