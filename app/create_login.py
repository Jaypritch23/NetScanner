#Allows users to generate username from entering first and last name which is stored within a csv file

from tkinter import *
from tkinter import messagebox
import random
import csv
            
def name_checker(first: str, last: str, window: Tk):
    """Check if user already has username. 
       If new user, generates username from
       first and last name."""
    exist = False
    filename = "usernames.csv"
    try: 
        with open(filename, "r",) as user_file:
            csv_reader = csv.reader(user_file)

            for row in csv_reader:
                if row[0] == first:
                    if row[1] == last:
                        messagebox.showinfo(message=f"You already have a username: {row[2]}")
                        exist = True #exist is true, if already in csv file
                        
                        break
            
    except FileNotFoundError:
        with open(filename, "w", newline="") as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow(["FirstName", "LastName", "Username"])  

    while not exist:       
        username = ""
        if (first == ""):
            messagebox.showinfo(title="INVALID ENTRY", message="Please enter a valid first name")
        if (last == ""):
            messagebox.showinfo(title="INVALID ENTRY", message="Please enter a valid last name")
        else:
            username += first[0].lower()
            username += last[0].lower()
        while len(username) < 5:
            username += str(random.randint(0,9))

        with open(filename, "a", newline="") as user_file:
            csv_writer = csv.writer(user_file)
            csv_writer.writerow([first, last, username])

        messagebox.showinfo(message=f"Your username is: {username}")
        exist = True 
        
    if exist == True:
        window.destroy()
    

         

def user_detail_UI():
    """Widget that allows user to enter first and last name to obtain a personal username."""

    credential_window = Tk()
    credential_window.geometry("300x100")
    credential_window.eval('tk::PlaceWindow . center') #center window
    credential_window.title("Login Page")
    credential_window.config(background="#f2e2c9")


    Label(credential_window, 
              text="First Name", 
              font=('Arial',20),
              relief='raised', 
              background="#bdad97",
              foreground="#000000",).grid(row=0, column=0)

    first_name = Entry(credential_window, 
                       foreground="#000000",
                       background="white")
    first_name.grid(row=0, column=1)

    Label(credential_window, 
              text="Last Name", 
              font=('Arial',20),
              relief='raised', 
              background="#bdad97",
              foreground="#000000",).grid(row=1, column=0)

    last_name = Entry(credential_window, 
                      foreground="#000000",
                      background="white")
    last_name.grid(row=1, column=1)

    Button(credential_window,
                text="Submit",
                font=('Arial',20),
                relief='raised', command=lambda: name_checker(first_name.get().replace(" ", ""), last_name.get().replace(" ", ""), credential_window)).grid(row=2,columnspan=2)

    credential_window.mainloop()




