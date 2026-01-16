# Network Tool

Python application that helps you monitor and analyse devices on your local network. It provides tools to scan your network, 
identify devices using the ARP table and OUI lookup, check network health, manage unknown hosts.

---

## Features

- **IP Ping (`IP_ping.py`)**: Pings all 255 addresses on your local network to update the ARP table.  
- **Create Login (`create_login.py`)**: Generates a username by entering your first and last name.  
- **Device Finder (`device_finder.py`)**: Uses the ARP table to find all hosts that responded to the network ping.  
- **Login Page (`main.py`)**: Checks if a user has a username and directs them to create one if they don’t.  
- **Network Health (`network_health.py`)**: Checks basic network connectivity, DNS, and internet access.  
- **Scanner Menu (`scanner_menu.py`)**: Main homepage with three buttons:
  - Scan Network → runs `device_finder` and outputs a table including OUI lookup and MAC type.
  - View Unknown Hosts → see unknown devices on the network.
  - Check Network Health → quick network diagnostics.
- **View Unknown (`view_unknown.py`)**: Displays unknown hosts. One click copies the MAC address; double click allows adding a hostname.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/NetScanner.git
cd NetScanner
