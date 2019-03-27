import pandas as pd
import numpy as np
import os
import time

def file_len(filepath):
    # Counts the number of lines of text are in the file
    with open(filepath) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def parse_data(filepath):
    # parses desired data from a text file
    # used for the known location data parsing
    # Could be run in a different file, and then stored as data to be input in the future
    numLines = file_len(filepath)
    tm = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
    quality = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
    essid = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
    signalstr = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)

    with open(filepath, 'r') as file:
        i =0
        for i in range(numLines):
            line = file.readline()
            if 'Time' in line:
                idx = line.find('Time')
                idx = idx+7
                time_i = line[idx:idx+15].strip()
                tm = np.append(tm,time_i)
            if 'Quality' in line:
                idx = line.find('Quality')
                idx = idx+8
                qual_i = line[idx:idx+5].strip()
                quality = np.append(quality,qual_i)
                if len(tm)!=len(quality):
                    tm = np.append(tm,time_i)
            if 'ESSID' in line:
                idx = line.find('ESSID')
                idx = idx+7
                essid_i = line[idx::]
                essid_i = essid_i.replace('"', ' ').strip()
                essid = np.append(essid,essid_i)
            if 'Signal level' in line:
                idx = line.find('Signal level')
                idx = idx+13
                str_i = line[idx:idx+3].strip()
                signalstr = np.append(signalstr,str_i)
            i +=1

        d = {'Time': tm, 'Quality': quality,'ESSID':essid,'Signal level': signalstr}
        df = pd.DataFrame(data=d)

        df_sorted = df.sort_values(by=['Time','ESSID', 'Signal level'])
        df_sorted = df_sorted.reset_index(drop=True)

        df_sorted = df_sorted.drop_duplicates(subset=['ESSID', 'Time'], keep='first', inplace=False) #keep largest signal strength for each ESSID

        df_sorted = df_sorted.reset_index(drop=True)

        df_unique_names =df_sorted.drop_duplicates(subset=['ESSID'], keep='first', inplace=False).reset_index(drop=True)

        unique_essid = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
        avg_signalstr = np.array([], dtype=float, copy=True, order='K', subok=False, ndmin=0)
        summ = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)
        # Calculation of the average of the maximum signal level for each ESSID
        for i in range(len(df_unique_names)):
            for j in range(len(df_sorted)):
                if  df_sorted.loc[j,'ESSID'] == df_unique_names.loc[i,'ESSID']:
                    test = int(df_sorted.loc[j,'Signal level'])
                    summ = np.append(summ,test)
            avg = np.mean(summ)
            unique_essid = np.append(unique_essid ,df_unique_names.loc[i,'ESSID'])
            avg_signalstr = np.append(avg_signalstr,avg)
            summ = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)

        d2 = {'ESSID':unique_essid,'Signal level': avg_signalstr}
        final_df = pd.DataFrame(data=d2)
        return(final_df)

def trim_data(node,essid_used):
    # Removes data from a dataframe that  doesnt exist in essid_used
        j =0
        i =0
        check = False
        for i in range(len(node)):
           for j in range(len(essid_used)):
               if  essid_used[j] == node.loc[i,'ESSID']:
                   check = True
           if check != True:
               node = node.drop([i])
           check = False
        return node

def realtime_parsing(line):
    # Parses an entire reading input as a string, rather than a line in a text file
    essid = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
    signalstr = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)
    lis = line.split("Quality")
    for data in lis:
        smaller_data = data.strip().split('\n')
        if ( len(smaller_data) < 2):
            continue
        essid_step = smaller_data[1].strip("ESSID:").strip('"')
        essid_step = essid_step.split('"')[1]
        signal_level = smaller_data[0].split(' ')
        signal_level = int(signal_level[3].strip("level="))
        signalstr = np.append(signalstr,signal_level)
        essid = np.append(essid,essid_step)
    print(essid)
    print (signalstr)
    d = {'ESSID':essid,'Signal level': signalstr}
    df = pd.DataFrame(data=d)
    df = df.sort_values(by=['ESSID', 'Signal level'])
    df = df.reset_index(drop=True)
    rt_avg_df =rt_avg(df)
    return(rt_avg_df)
    
def rt_avg(df):
    #Calculates average of real-time data
    df_unique_names =df.drop_duplicates(subset=['ESSID'], keep='first', inplace=False).reset_index(drop=True)
    unique_essid = np.array([], dtype=str, copy=True, order='K', subok=False, ndmin=0)
    summ = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)
    avg_signalstr = np.array([], dtype=float, copy=True, order='K', subok=False, ndmin=0)
    for i in range(len(df_unique_names)):
        for j in range(len(df)):
            if  df.loc[j,'ESSID'] == df_unique_names.loc[i,'ESSID']:
                test = int(df.loc[j,'Signal level'])
                summ = np.append(summ,test)
        avg = np.mean(summ)
        unique_essid = np.append(unique_essid ,df_unique_names.loc[i,'ESSID'])
        avg_signalstr = np.append(avg_signalstr,avg)
        summ = np.array([], dtype=int, copy=True, order='K', subok=False, ndmin=0)
    d2 = {'ESSID':unique_essid,'Signal level': avg_signalstr}
    rt_df = pd.DataFrame(data=d2)
    return(rt_df)


if __name__ == "__main__":
        # Data Parsing
        filepath = 'new_location_g2.txt'
        g1 = parse_data(filepath).sort_values(by=['ESSID']).reset_index(drop=True)
        filepath = 'new_location_y1.txt'
        y2 = parse_data(filepath).sort_values(by=['ESSID']).reset_index(drop=True)
        filepath = 'new_location_r2.txt'
        r1 = parse_data(filepath).sort_values(by=['ESSID']).reset_index(drop=True)
        
        # Checks which ESSID's can be seen from all 3 locations
        xsection1= np.intersect1d(g1.loc[:,'ESSID'],r1.loc[:,'ESSID'])
        essid_used= np.intersect1d(xsection1,y2.loc[:,'ESSID'])

        # Trims data frame containing known data to only include ESSID's that are in common
        trimmed_g1 = trim_data(g1,essid_used).sort_values(by=['ESSID']).reset_index(drop=True)
        print("\nTrimmed Data from location G1: \n")
        print(trimmed_g1)
        trimmed_y2 = trim_data(y2,essid_used).sort_values(by=['ESSID']).reset_index(drop=True)
        print("\nTrimmed Data from location Y2: \n")
        print(trimmed_y2)
        trimmed_r1 = trim_data(r1,essid_used).sort_values(by=['ESSID']).reset_index(drop=True)
        print("\nTrimmed Data from location R1: \n")
        print(trimmed_r1)

        #Beginning of real time data acquisition
        WIFI_SCAN_CMD = 'sudo iwlist wlan0 scan | grep -E ESSID\|Signal\ level'
        while True:
            temp_g = trimmed_g1 # Dummy variables to account for real time data not always seeing the same signal at all times
            temp_r = trimmed_r1
            temp_y = trimmed_y2
            scan_rst = ''
            # Real time data acquisition loop
            # Takes five readings
            for t in range(5):
                string_dump = os.popen(WIFI_SCAN_CMD).read()
                scan_rst = scan_rst + string_dump
                t +=1
            rt_dat = realtime_parsing(scan_rst)
            
            # accounts for real time data not always seeing the same signal at all times
            # temporarily removes data from trimmed_g1,r1 and y2 for one cycle, then it is reset with the earlier dummy variables
            temp = np.intersect1d(temp_g.loc[:,'ESSID'],rt_dat.loc[:,'ESSID'])
            rt_test=trim_data(rt_dat,temp).sort_values(by=['ESSID']).reset_index(drop=True)
            temp_g=trim_data(temp_g,temp).sort_values(by=['ESSID']).reset_index(drop=True)
            temp_r=trim_data(temp_r,temp).sort_values(by=['ESSID']).reset_index(drop=True)
            temp_y=trim_data(temp_y,temp).sort_values(by=['ESSID']).reset_index(drop=True)
           
            print(rt_test)
            # formats data into numpy arrays raher than series so that numpy can perform a normalization
            test_data_set = rt_test.loc[:,'Signal level']
            test_data_set = test_data_set.as_matrix(columns=None)
            sub_g = temp_g.loc[:,'Signal level'].as_matrix(columns=None)
            sub_y = temp_y.loc[:,'Signal level'].as_matrix(columns=None)
            sub_r = temp_r.loc[:,'Signal level'].as_matrix(columns=None)

            # Calculate and print norm
            gnorm = np.linalg.norm(np.subtract(sub_g,test_data_set),ord = 2)
            rnorm = np.linalg.norm(np.subtract(sub_r,test_data_set),ord =2)
            ynorm = np.linalg.norm(np.subtract(sub_y,test_data_set),ord =2)
            print(gnorm)
            print(rnorm)
            print(ynorm)
            
            # Hand calculation check of norm -- it is the same value always
            print('calculated norms')
            ynorm = np.sqrt(np.sum(np.square(np.subtract(sub_y,test_data_set))))
            rnorm = np.sqrt(np.sum(np.square(np.subtract(sub_r,test_data_set))))
            gnorm = np.sqrt(np.sum(np.square(np.subtract(sub_g,test_data_set))))
            print(gnorm)
            print(rnorm)
            print(ynorm)
            
            # Tells the user which node is closest based on minimum value of gnorm,rnorm or ynorm
            if gnorm == min(gnorm,rnorm,ynorm):
                print('Raspberry Pi is closet to Node G1')
            elif rnorm == min(gnorm,rnorm,ynorm):
                print('Raspberry Pi is closet to Node R1')
            elif ynorm == min(gnorm,rnorm,ynorm):
                print('Raspberry Pi is closet to Node Y2')
            time.sleep(.5)
