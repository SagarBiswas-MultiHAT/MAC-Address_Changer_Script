import os
import sys
import subprocess

# Check if the script is run as root
if os.geteuid() != 0:
    print("This script must be run as root. Please use 'sudo' to run it.")
    sys.exit(1)

MAC_address = input("Enter the custom MAC address you want to set for the interface: ")

# Bring the interface down
subprocess.run(["ifconfig", "wlan0", "down"])

# Change the MAC address
subprocess.run(["macchanger", "-m", MAC_address, "wlan0"])
# Adding the prompt multiple times for safety purpose.
subprocess.run(["macchanger", "-m", MAC_address, "wlan0"]) 
subprocess.run(["macchanger", "-m", MAC_address, "wlan0"])

# Bring the interface back up
subprocess.run(["ifconfig", "wlan0", "up"])
