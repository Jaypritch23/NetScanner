#Homepage of the app, where users have the option to access network troubleshooting tools.

from tkinter import *
from device_finder import scan
from view_unknown import unkown_dev
from network_health import network_health_gui

def scan_gui():

    import ast
    import requests
    from bs4 import BeautifulSoup
    from tkinter import Tk, Label, Button
    from tkinter import ttk

    """
    Output table of devices that are currently on
    the same network as this device.
    """

    scan_page = Tk()
    scan_page.geometry("1300x1000")
    scan_page.eval('tk::PlaceWindow . center')
    scan_page.title("Scan Page")
    scan_page.config(background="#DED1A6")

    Label(
        scan_page,
        text="Current devices on your network!",
        font=('Helvetica', 20),
        relief='raised',
        width=350,
        background="#bdad97",
        foreground="#000000"
    ).pack()

    devices = scan()

    Label(
        scan_page,
        text=devices.get("Time", ""),
        background="#DED1A6",
        foreground="black"
    ).pack()

    tree = ttk.Treeview(
        scan_page,
        columns=("hostname", "ipv4", "mac", "assignment", "mac_type", "org"),
        show="headings"
    )

    style = ttk.Style()
    style.configure(
        "Treeview",
        borderwidth=2,
        rowheight=35
    )

    tree.pack(fill="both", expand=True)

    tree.heading("hostname", text="Hostname")
    tree.heading("ipv4", text="IPv4 Address")
    tree.heading("mac", text="MAC Address")
    tree.heading("assignment", text="LAA | UAA")
    tree.heading("mac_type", text="MAC type")
    tree.heading("org", text="Organisation")

    tree.column("hostname", width=120)
    tree.column("ipv4", width=120, anchor="center")
    tree.column("mac", width=160, anchor="center")
    tree.column("assignment", width=100, anchor="center")
    tree.column("mac_type", width=100, anchor="center")
    tree.column("org", width=200, anchor="center")

    #if last binary digit is 1 (0001), then multicast. 
    #if second to last binary digit is 1 (0010), then LAA
    mac_values = {
        'UAA': {'0': 1, '1': 2, '4': 4, '5': 5, '8': 8, '9': 9, 'c': 12, 'd': 13},
        'LAA': {'2': 2, '3': 3, '6': 6, '7': 7, 'a': 10, 'b': 11, 'e': 14, 'f': 15}
    }

    for hostname, raw_data in devices.items():

        if hostname == "Time":
            continue

        #Convert CSV string to dict
        if isinstance(raw_data, str):
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

        #Standardises MAC
        parts = mac.split(":")
        parts = [p.zfill(2) for p in parts]
        mac = ":".join(parts)

        mac_char = mac[1].lower()

        #OUI and MAC type 
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

            mac_type = (
                "Unicast"
                if mac_values["UAA"][mac_char] % 2 == 0
                else "Multicast"
            )

        elif mac_char in mac_values["LAA"]:
            assignment_type = "LAA"
            organisation = "Unavailable"
            mac_type = (
                "Unicast"
                if mac_values["LAA"][mac_char] % 2 == 0
                else "Multicast"
            )

        else:
            assignment_type = "Unknown"
            organisation = "Unknown"
            mac_type = "Unknown"

        tree.insert(
            "",
            "end",
            values=(hostname, ipv4, mac, assignment_type, mac_type, organisation)
        )

    Button(
        scan_page,
        text="Return to menu",
        anchor="center",
        command=scan_page.destroy
    ).pack()



def rootGUI(first_name: str):
    """

    Menu with different tasks that can be run.

    """

    homepage = Tk()
    homepage.geometry("400x300")
    homepage.eval('tk::PlaceWindow . center') #center window
    homepage.title("Homepage")
    homepage.config(background="#DED1A6")


    Label(homepage, text=f"WELCOME {first_name}".upper(),
          font=('Helvetica',30, "bold", "italic"),
          relief='raised',
          width=350,
          background="#bdad97",
          foreground="#000000").pack()

    Label(homepage, text="", background="#DED1A6").pack()  

    scan_button = Button(homepage, 
                     text="Scan Your Network",
                     font=('Arial',20),
                     relief='raised',
                     highlightbackground="#000000",
                    command= lambda: scan_gui())
    scan_button.pack()

    Label(homepage, text="", background="#DED1A6").pack() 

    unknown_button = Button(homepage,
                     text="View Unknown Devices",
                     font=('Arial',20),
                     relief='raised',
                     highlightbackground="#000000",
                     command= lambda: unkown_dev())
    unknown_button.pack()
    
    Label(homepage, text="", background="#DED1A6").pack() 

    hello = Button(homepage,
                     text="Test Network Health",
                     font=('Arial',20),
                     relief='raised',
                     highlightbackground="#000000",
                     command= lambda: network_health_gui())
    hello.pack()






