from scapy.all import *
from threading import Thread
import pandas
import time
import os

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")

        #print("Hello world")

         #Redirect the standard output to the file
        with open('out.txt', 'w') as file:
    
            sys.stdout = file
            print(bssid," ", ssid, " ", channel, " ", crypto)
            sys.stdout = sys.__stdout__

        #networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

def sniff_on_channel(interface, channel):
    os.system(f"iwconfig {interface} channel {channel}")
    sniff(prn=callback, iface=interface, timeout = 10)


if __name__ == "__main__":
    interface = "wlp1s0mon"
    threads = []

    #2.4GHz band have a total of 11 channels
    for channel in range(1, 12):
        #print(channel)
        thread = Thread(target=sniff_on_channel, args=(interface, channel))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    try:
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Exiting...")