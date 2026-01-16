#Check basic network health

from tkinter import *
from tkinter import ttk
import subprocess
import socket

def network_health_check():
    results = {}

    gateway = "192.168.0.1"


    try:
        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1000", gateway],
            stderr=subprocess.DEVNULL
        )
        results["Gateway Reachable"] = "Yes"
    except subprocess.CalledProcessError:
        results["Gateway Reachable"] = "No"

    #Test internet connection
    try:
        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1000", "1.1.1.1"],
            stderr=subprocess.DEVNULL
        )
        results["Internet Reachable"] = "Yes"
    except subprocess.CalledProcessError:
        results["Internet Reachable"] = "No"

    #DNS test
    try:
        socket.gethostbyname("google.com")
        results["DNS Working"] = "Yes"
    except socket.gaierror:
        results["DNS Working"] = "No"

    #Overall status
    if results["Gateway Reachable"] == "No":
        results["Overall Status"] = "Local network issue"
    elif results["Internet Reachable"] == "No":
        results["Overall Status"] = "ISP / Internet issue"
    elif results["DNS Working"] == "No":
        results["Overall Status"] = "DNS issue"
    else:
        results["Overall Status"] = "Network OK"

    return results



def network_health_gui():
    page = Tk()
    page.geometry("600x400")
    page.eval('tk::PlaceWindow . center')
    page.title("Network Health Check")
    page.config(background="#DED1A6")

    Label(
        page,
        text="Network Health Check",
        font=('Helvetica', 20),
        relief='raised',
        width=40,
        background="#bdad97",
        foreground="#000000"
    ).pack(pady=10)

    tree = ttk.Treeview(
        page,
        columns=("check", "result"),
        show="headings",
        height=6
    )
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    tree.heading("check", text="Check")
    tree.heading("result", text="Result")

    tree.column("check", width=250, anchor="w")
    tree.column("result", width=200, anchor="center")


    style = ttk.Style()
    style.configure("Treeview", rowheight=35)

    def run_check():
        tree.delete(*tree.get_children())
        results = network_health_check()

        for key, value in results.items():
            tree.insert("", "end", values=(key, value))

    Button(
        page,
        text="Run Health Check",
        font=('Arial', 14),
        command=run_check
    ).pack(pady=10)

    Button(
        page,
        text="Return to menu",
        font=('Arial', 14),
        command=page.destroy
    ).pack(pady=5)



