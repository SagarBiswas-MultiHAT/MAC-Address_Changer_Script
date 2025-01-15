
---

# MAC Address Changer Script

Welcome to the **MAC Address Changer Script**, a Python-based utility designed to allow you to easily change the MAC address of a network interface. Whether you need to anonymize your device, bypass MAC filtering, or troubleshoot network issues, this tool helps you do it quickly and efficiently.

## Overview

This script provides a simple way to change the MAC address of a specified network interface. It uses `macchanger` and `ifconfig` to accomplish this task, ensuring your system is not just secure, but flexible in terms of network configurations.

## Requirements

- **Python 3.x**
- **macchanger**: A Linux tool to change MAC addresses (Install using your package manager, e.g., `sudo apt install macchanger`)
- **ifconfig**: A network management tool for Linux (usually installed by default)

Make sure these dependencies are installed on your system before running the script.

## Usage

### Running the Script

To run the script, use the following command:

```bash
python3 change_mac.py
```

The script will guide you through the following steps:

1. **Root Privileges**: The script checks if it's running with root privileges (you'll need `sudo` to change the MAC address).
2. **Enter Custom MAC Address**: Enter the new MAC address you'd like to set for the specified network interface.
3. **MAC Address Change**: The script will bring the interface down, change the MAC address, and bring it back up.

### Example Output

When you run the script, it will look like this:

```
This script must be run as root. Please use 'sudo' to run it.
Enter the custom MAC address you want to set for the interface: 00:11:22:33:44:55
MAC address for wlan0 set to 00:11:22:33:44:55.
```

If there’s any error during the process, the script will provide a helpful error message.

## Code Walkthrough

### Root Check

The script begins by checking if the user has root privileges, as modifying the MAC address requires administrative access.

### Set MAC Address

- The script takes an interface (e.g., `wlan0`) and a custom MAC address as input.
- It brings the interface down, sets the MAC address using `macchanger`, and brings the interface back up.
- If anything goes wrong during this process, the script catches the error and displays a helpful message.

### Error Handling

- The script is designed to gracefully handle errors that might occur, such as command failures or unexpected issues.

## Contributing

Feel free to contribute! If you'd like to add new features, improve existing functionality, or fix bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
