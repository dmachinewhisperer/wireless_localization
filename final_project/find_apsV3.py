import pandas as pd
import subprocess
import re

#This script scans and finds available APs 

output_file = "output.txt"

target_ssid = "GITAM"
aps = []

bssid = signal_strength = band = channel = detected_aps = None

index = 1

def execute_netsh_cmd():

    netsh_command = ["netsh", "wlan", "show", "network", "mode=BSSID"]

    with open(output_file, "w") as f:
        subprocess.run(netsh_command, stdout=f, text=True)


def detect_aps():

    #parses the output of the netsh cmd

    execute_netsh_cmd()

    global index, aps, target_ssid, bssid, signal_strength, band, channel, detected_aps

    aps = []

    with open(output_file, "r") as f:
        target_ssid_found = False 
        for line in f:
            if target_ssid in line.split():
                target_ssid_found = True
                continue

            if target_ssid_found:

                if "SSID" in line.split() and "GITAM" not in line.split():
                    break
                
                line = line.strip()

                if line.startswith("BSSID"):
                    bssid = ":".join(line.split(":")[1:]).strip()

                if line.startswith("Signal"):
                    signal_strength = float(line.split(":")[1].strip().strip('%'))

                if line.startswith("Band"):
                    band = line.split(":")[1].strip()

                if line.startswith("Channel") and ("Utilization:" not in line):
                    channel = line.split(":")[1].strip()

                    aps.append({
                        "index": index,
                        "bssid": bssid,
                        "dBm_signal": signal_strength,
                        "channel": channel,
                        "band": band
                    })
                    index = index + 1    

                    detected_aps = pd.DataFrame(aps)
