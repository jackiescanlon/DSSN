import os
import datetime

def parse_output(output, mac_address):
    words = output.split(' ')
    start = words.index(mac_address)
    if start != -1:
        # output looks like 00:15:83:EA:57:78 type LE Public rssi -46 
        rssi = words[start + 4]
    else:
        rssi = 'None found'
    return rssi
    
    
if __name__ == "__main__":

    date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    filepath = 'rssi_' + date + '.txt'
    mac_address = 'A4:34:D9:FF:7A:6B'
    scan_cmd = 'sudo btmgmt find'
    
    while(True):
        output = os.popen(scan_cmd).read()
        rssi = parse_output(output, mac_address)
        
        print('RSSI for ' + mac_address + ' = '  + rssi)
        with open(filepath, 'a') as file:
            file.write(rssi + '\n')

