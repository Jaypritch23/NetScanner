#Allow users to view unkown devices. Click once to copy the MAC address, click twice to enter a hostname.

from tkinter import *
from device_finder import scan
import json
import os

KNOWN_DEVICES_FILE = "known_devices.json"

def unkown_dev():
    import ast
    import requests
    from bs4 import BeautifulSoup
    from tkinter import Tk, Label, Button
    from tkinter import ttk

    global known_devices


    mac_values = {
        'UAA': {'0': 1, '1': 2, '4': 4, '5': 5, '8': 8, '9': 9, 'c': 12, 'd': 13},
        'LAA': {'2': 2, '3': 3, '6': 6, '7': 7, 'a': 10, 'b': 11, 'e': 14, 'f': 15}
    }

    unkown_dev_window = Tk()
    unkown_dev_window.geometry("800x700")
    unkown_dev_window.eval('tk::PlaceWindow . center')
    unkown_dev_window.title("Unknown Device Page")
    unkown_dev_window.config(background="#f2e2c9")

    Label(
        unkown_dev_window,
        text="Current unknown devices on your network!",
        font=('Helvetica', 20),
        relief='raised',
        width=350,
        background="#bdad97",
        foreground="#000000"
    ).pack()

    devices = scan()

    tree = ttk.Treeview(
        unkown_dev_window,
        columns=("hostname", "ipv4", "mac", "assignment", "mac_type", "org"),
        show="headings"
    )

    style = ttk.Style()
    style.configure("Treeview", background="light grey", borderwidth=2, rowheight=35)
    tree.pack(fill="both", expand=True)

    for col in ("hostname", "ipv4", "mac", "assignment", "mac_type", "org"):
        tree.heading(col, text=col.title())
        tree.column(col, width=133, anchor="center")

    #Populate table
    for hostname, raw_data in devices.items():
        if "Unknown device" not in hostname:
            continue

        if isinstance(raw_data, str): #Ensures values are real python objects
            try:
                data = ast.literal_eval(raw_data)
            except (ValueError, SyntaxError):
                continue
        else:
            data = raw_data

        ipv4 = data.get("IPv4", "Unknown")
        mac = data.get("MAC", "Unknown")
        if mac == "Unknown":
            continue


        parts = [p.zfill(2) for p in mac.split(":")]
        mac = ":".join(parts)
        mac_char = mac[1].lower()

        if mac_char in mac_values["UAA"]:
            assignment_type = "UAA"
            try:
                url = f"https://maclookup.app/search/result?mac={mac}"
                page = requests.get(url, timeout=5)
                soup = BeautifulSoup(page.text, "html.parser")
                h1 = soup.find("div", class_="col-md-12").find("h1")
                organisation = h1.get_text(strip=True) if h1 else "Unknown"
            except Exception:
                organisation = "Unknown"
            mac_type = "Unicast" if mac_values["UAA"][mac_char] % 2 == 0 else "Multicast"
        elif mac_char in mac_values["LAA"]:
            assignment_type = "LAA"
            organisation = "Unavailable"
            mac_type = "Unicast" if mac_values["LAA"][mac_char] % 2 == 0 else "Multicast"
        else:
            assignment_type = "Unknown"
            organisation = "Unknown"
            mac_type = "Unknown"

        tree.insert("", "end", values=(hostname, ipv4, mac, assignment_type, mac_type, organisation))

    
    def copy_mac_to_clipboard(event):
        """Copy MAC, one click"""

        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")
        if not values:
            return

        mac = values[2]
        unkown_dev_window.clipboard_clear()
        unkown_dev_window.clipboard_append(mac)

        print(f"Copied MAC address: {mac}")

    tree.bind("<ButtonRelease-1>", copy_mac_to_clipboard)


    def save_hostname(mac, entry, popup):
        """Save hostname to JSON database"""
        global known_devices
        name = entry.get().strip()
        if name:
            known_devices[mac] = name
            with open(KNOWN_DEVICES_FILE, "w") as f:
                json.dump(known_devices, f, indent=4)
            popup.destroy()
            print(f"Saved device: {mac} -> {name}")


    def assign_hostname(event):
        """Double click row, prompts user to add hostname."""
        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")
        mac = values[2]

        popup = Tk()
        popup.geometry("300x140")
        popup.title("Assign Hostname")
        popup.eval('tk::PlaceWindow . center')

        Label(popup, text="Enter hostname for this device:").pack(pady=5)
        entry = ttk.Entry(popup)
        entry.pack(pady=5)
        entry.focus()

        Button(
            popup,
            text="Save",
            command=lambda m=mac: save_hostname(m, entry, popup)
        ).pack(pady=10)

    tree.bind("<Double-1>", assign_hostname)


    Button(
        unkown_dev_window,
        text="Return to menu",
        anchor="center",
        background="#f2e2c9",
        command=unkown_dev_window.destroy
    ).pack(pady=10)

    unkown_dev_window.mainloop()
