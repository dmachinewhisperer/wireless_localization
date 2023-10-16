from scapy.all import *
from threading import Thread
import pandas
import time
import os

detected_aps = None; 

    

def callback(packet):
    global detected_aps

    if packet.haslayer(Dot11Beacon) and packet[Dot11Elt].info.decode() == "GITAM":
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
        detected_aps.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    while True:
        os.system("clear")
        print(detected_aps)
        time.sleep(0.5)

def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)



def detect_aps():

    global detected_aps

    #dataframe to store packets
    detected_aps = pandas.DataFrame(columns=["bssid", "ssid", "dBm_signal", "channel", "crypto"])
    detected_aps.set_index("bssid", inplace=True)

    interface = "wlp1s0mon"
    
    #start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    #start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    
    # start sniffing
    sniff(prn=callback, iface=interface, timeout = 10)

