import os
import datetime

def parse_output(output, mac_address):
    words = output.split(' ')
    
    try: 
        start = words.index(mac_address)
        rssi = words[start + 4]
    except: 
        rssi = 'None found'
    return rssi
    
    
if __name__ == "__main__":

    date = datetime.datetime.now()
    datestr = date.strftime('%Y_%m_%d_%H_%M_%S')
    filepath = 'rssi_' + datestr + '.txt'
    mac_address = 'B8:27:EB:22:8C:87'
    scan_cmd = 'sudo btmgmt find'
    
    # First, write the date and mac_address to the file
    header = 'MAC Address: ' + mac_address + '\nMeasurements taken on ' + date.strftime('%A %B %d, %Y at %H:%M:%S')
    print(header + '\n')
    
    with open(filepath, 'a') as file:
            file.write(header)
            file.write('\nDistances measured in cm and RSSI measured in dB.\n\nDistance    RSSI\n')
    while(True):
        distance = raw_input('Enter the distance away the device is (cm): ')
        output = os.popen(scan_cmd).read()
        rssi = parse_output(output, mac_address)
        
        string_out = distance + '          ' + rssi + '\n'
        print(rssi)
        with open(filepath, 'a') as file:
            file.write(string_out)

