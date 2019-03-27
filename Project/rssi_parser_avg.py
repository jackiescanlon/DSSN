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
    filepath = 'rssi_' + datestr + '.csv'
    
    mac_lookup = {'jezza': 'B8:27:EB:22:8C:87', 'jeremy': '10:4A:7D:9D:E7:EC', 'paul': '70:1C:E7:38:FC:E2'}
    
    print('Possible MAC Addresses:\n' + str(mac_lookup) + '\n\n')
    mac_address = raw_input('Enter the name of the MAC Address you want (0 for a new one):')
    if mac_address == '0':
        mac_address = raw_input('Enter the MAC Address: ')
    else:
        mac_address = mac_lookup.get(mac_address, '0')
        if mac_address == '0':
            mac_address = raw_input('Not found. Enter the MAC Address: ')
            
    scan_cmd = 'sudo btmgmt find'
    
    # First, write the date and mac_address to the file
    header = 'MAC Address: ' + mac_address + '\nMeasurements taken on ' + date.strftime('%A %B %d, %Y at %H:%M:%S')
    print(header + '\n')
    
    with open(filepath, 'a') as file:
            file.write(header)
            file.write('\nDistances measured in inches and RSSI measured in dB.\n\nDistance, RSSI\n')
    
    try:
        while(True):
            distance = raw_input('Enter the distance away the device is (in): ')
            total = 0.
            count_original = 2
            count = count_original
            for i in range (0,count_original):
                output = os.popen(scan_cmd).read()
                rssi = parse_output(output, mac_address)
                print('Measurement ' + str(i+1) + ': ' + rssi)
                if rssi == 'None found':
                    rssi = '0'
                    count = count - 1
                total = total + int(rssi)
                
                with open(filepath, 'a') as file:
                    string_out = distance + ', ' + rssi + '\n'
                    file.write(string_out)
                
            if count != 0:
                total = str(total/count)
            else:
                total = 'None found'
                
            print('Average RSSI: ' + total)
                
    except KeyboardInterrupt:
        print('\nData collection ended.')

