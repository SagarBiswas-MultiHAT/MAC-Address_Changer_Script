import os
import sys
import subprocess

def check_root():
    """Check if the script is run as root."""
    if os.geteuid() != 0:
        print("This script must be run as root. Please use 'sudo' to run it.")
        sys.exit(1)

def set_mac_address(interface, mac_address):
    """Set a custom MAC address for a given network interface."""
    try:
        # Bring the interface down
        subprocess.run(["ifconfig", interface, "down"], check=True)
        
        # Change the MAC address
        # The check=True argument ensures that an exception is raised if the command fails
        subprocess.run(["macchanger", "-m", mac_address, interface], check=True)
        
        # Bring the interface back up
        subprocess.run(["ifconfig", interface, "up"], check=True)
        
        print(f"MAC address for {interface} set to {mac_address}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while setting the MAC address: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    check_root()
    interface = "wlan0"
    mac_address = input("Enter the custom MAC address you want to set for the interface: ")
    
    set_mac_address(interface, mac_address)

if __name__ == "__main__":
    main()
