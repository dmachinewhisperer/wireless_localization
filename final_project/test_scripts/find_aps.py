import pyshark

def print_access_points(packet):
    try:
        if packet.layers[3].wlan_radio.signal_dbm:  # Checking if signal strength (RSSI) is available
            ssid = packet.layers[3].ssid
            bssid = packet.layers[2].wlan.ta
            rssi = packet.layers[3].wlan_radio.signal_dbm

            # You can add other relevant fields here if needed
            channel = packet.layers[2].wlan_radio.channel

            print(f"SSID: {ssid}, BSSID: {bssid}, RSSI: {rssi} dBm, Channel: {channel}")
    except AttributeError:
        pass

def main():
    # Set the interface in monitor mode before running the script.
    # Use Wireshark or other tools to put your Wi-Fi interface in monitor mode.
    capture = pyshark.LiveCapture(interface='wlp1s0mon', display_filter='wlan')

    print("Scanning for Access Points... Press Ctrl+C to stop.")

    try:
        for packet in capture.sniff_continuously():
            if "wlan_mgt" in packet and "wlan_radio" in packet:  # Filter management frames with signal strength info
            print_access_points(packet)
    except KeyboardInterrupt:
        print("Scan stopped.")

if __name__ == "__main__":
    main()
