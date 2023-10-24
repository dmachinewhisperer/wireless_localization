from tabulate import tabulate
import pandas as pd
import numpy as np
import find_apsV3
import time
import sys
#number of readings per position
n = 30

#Number of time to appear in scan before being considered valid(%)
th = 0.75

#dictionary to hold bssids and their frequency
ap_consistency= {}

#detected_aps = None


def progress_bar(iteration, total, length=40, fill_char='█', label='Progress'):
    progress = (iteration / total)
    arrow = int(length * progress)
    spaces = length - arrow

    sys.stdout.write(f'\r{label}: [{fill_char * arrow}{" " * spaces}] {iteration}/{total} done')
    sys.stdout.flush()


def get_radio_map(show_stats = True):
    #get aps
    global detected_aps, ap_consistency
    

    for i in range(n):

        find_apsV3.detected_aps = None
        find_apsV3.detect_aps()
        detected_aps = find_apsV3.detected_aps
        #print(detected_aps)

        for bssid in detected_aps['bssid']:
            
            #compute how many times a bssid showed up in the scans
            signal_power = detected_aps[detected_aps['bssid'] == bssid]['dBm_signal'].values[0]

            if bssid in ap_consistency.keys():
                ap_consistency[bssid][0] = ap_consistency[bssid][0] + 1
                ap_consistency[bssid][1] = np.append(ap_consistency[bssid][1], signal_power)
            else:
                ap_consistency[bssid] = [1, np.array(signal_power)]


        #time.sleep(2)    
        progress_bar(i + 1, n, label = "Radio Mapping: ")
 

    #extract keys to remove if threshold is not satisfied
    invalid_bssids = []

    for key in ap_consistency.keys():

        if ap_consistency[key][0] < (th * n):
            invalid_bssids.append(key)
            continue
        
        ap_consistency[key][1] = np.mean(ap_consistency[key][1])
    
    #remove the invalid keys
    for key in invalid_bssids:
        print(ap_consistency.pop(key), " dropped")
        

    #modify detected_ap: only bssid and power retained
    detected_aps = pd.DataFrame(list(ap_consistency.items()), columns=['bssid', 'dBm_signal'])

    #show scan statistics 

    if show_stats:
        stats_table = []
        stats_table_headers = ["access point", "no. occurences", "mean signal power"]
        for key in ap_consistency.keys():

            stats_table.append([key, ap_consistency[key][0], ap_consistency[key][1]])
        
        print("\n\nScan Statistics: ")
        print(tabulate(stats_table, headers = stats_table_headers, tablefmt="grid"))
    




#get_radio_map()
