#Login page that prompts users to sign in if they already have a username, if not then they are directed to create one.

from tkinter import *
from tkinter import messagebox
import create_login 
import csv
from scanner_menu import rootGUI


def username_check(username: str)-> None:
    """Checks if username is valid. No 
       known username, prompts users
       to create username."""
    
    exist = False
    filename = "usernames.csv"
    try:
        with open(filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in csv_reader:
                if username == i[2]:
                    first_name = i[0]
                    exist = True
                    rootGUI(first_name)
                    window.destroy()         
                    break
            
            if not exist:
                messagebox.showinfo(title="Username Not Found", message="Username Not Found:\n Proceed to create username")
                    
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Please create a username!")




window = Tk()
window.geometry("300x100")
window.eval('tk::PlaceWindow . center') #center window
window.title("Login")
window.config(background="#f2e2c9")



Label(window, 
              text="Username", 
              font=('Arial',20),
              relief='raised', 
              background="#DED1A6",
              foreground="#000000",
              ).grid(row=0, column=0)

username = Entry(window, 
                 background="White",
                 foreground="#000000")
username.grid(row=0, column=1)


no_username = Button(window,
                      text="Create Username", 
                      font=('Arial, 20'),
                      highlightbackground="#000000", command=lambda: create_login.user_detail_UI()).grid(row=3, columnspan=2)

submit = Button(window,
                text="Submit",
                font=('Arial',20),
                relief='raised',
                highlightbackground="#000000",  command=lambda: username_check(username.get().lower())).grid(row=2,columnspan=2)

window.mainloop()
