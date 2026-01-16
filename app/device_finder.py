import subprocess
import re
import csv
import datetime
import json
import os
from IP_ping import ping  

KNOWN_DEVICES_FILE = "known_devices.json"

def normalize_mac(mac):
    """Normalize MAC addresses: pad single digits and make lowercase"""
    parts = mac.split(":")
    parts = [p.zfill(2) for p in parts]
    return ":".join(parts).lower()

def scan():
    """Matches IP address with MAC, from ARP table. Checking against a JSON database if the MAC is already known."""

    if os.path.exists(KNOWN_DEVICES_FILE):
        with open(KNOWN_DEVICES_FILE, "r") as f:
            raw_known = json.load(f)
        known_devices = {normalize_mac(mac): name for mac, name in raw_known.items()}
    else:
        known_devices = {}

    ping()  #populate ARP table

    try:
        command = 'arp -a | grep -v incomplete'
        arp_table = subprocess.check_output(command, shell=True).decode()
        arp_entries = arp_table.splitlines()
    except subprocess.CalledProcessError:
        print("Failed to run arp command")
        arp_entries = []

    mac_result = []
    ip_result = []

    #Clean ARP table data
    for entry in arp_entries:
        match_ip = re.search(r'\((.*?)\)', entry)
        match_mac = re.search(r'at (.*?) on', entry)
        if match_ip:
            ip_result.append(match_ip.group(1))
        if match_mac:
            mac_result.append(match_mac.group(1).strip())

    Mac_IP_pair = dict(zip(mac_result, ip_result))

    hostname = {}
    current = datetime.datetime.now()
    hostname["Time"] = current.strftime("%a-%d-%B, %H:%M")

    i = 0
    for mac, ip in Mac_IP_pair.items():
        mac = normalize_mac(mac)

        if mac in known_devices:
            host = known_devices[mac]
            hostname[host] = {'IPv4': ip, 'MAC': mac}
        elif ip == '192.168.0.1':
            hostname['Gateway_IP'] = {'IPv4': ip, 'MAC': mac}
        else:
            hostname[f"Unknown device {i}"] = {'IPv4': ip, 'MAC': mac}
            i += 1

    filename = "scan_data.csv"
    try:
        with open(filename, "a", newline='') as f:
            writer = csv.DictWriter(f, hostname.keys())
            writer.writeheader()
            writer.writerow(hostname)
    except FileNotFoundError:
        with open(filename, "w", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["It worked"])
            for row in hostname:
                csv_writer.writerow(row.get())

    return hostname
