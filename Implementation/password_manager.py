import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import string

window = tk.Tk()
window.title("Password Manager")
window.geometry("500x400")
window.config(padx=20, pady=20)


# Labels
empty_label = tk.Label(text="")
empty_label.grid(column=0,row=0)

label_website = tk.Label(text="Website:")
label_website.grid(column=0,row=2, sticky="E")

label_username = tk.Label(text="Username / Email:")
label_username.grid(column=0,row=3, sticky="E")

label_pass = tk.Label(text="Password:")
label_pass.grid(column=0,row=4, sticky="E")

warning_label = tk.Label(text = " ")
warning_label.grid(column= 1, row= 8)


def disappear_warning_message():
    warning_label.config(text="")


# image_label 
image = Image.open("Password_Manager\password_manager.png")
image = image.resize((180, 180))
photo = ImageTk.PhotoImage(image) 
image_label = tk.Label(window, image= photo)
image_label.grid(column= 1, row= 9)


# Inputs from user (Entry Fields):
entry_website = tk.Entry(width= 40)
entry_website.grid(column=1, row=2, sticky="W")

entry_username = tk.Entry(width=40, )
entry_username.grid(column=1, row=3, sticky="W")

entry_password = tk.Entry(width=20 )
entry_password.grid(column=1, row=4, sticky="W")


# Memorizing the input info to a txt file:
password_info = []


def memorize_the_info():
    password_info = {}

    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    # Check for empty input boxes
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title = "Error Message", message = "Don't leave empty boxes")
        return

    password_info["website"] = website
    password_info["username/email"] = username
    password_info["password"] = password

    # Read how many lines are already written in the file, if the file exists:
    file_path = "Password_Vault.txt"

    if os.path.exists(file_path):
        with open("Password_Vault.txt", "r") as file:
            lines = file.readlines()
    else:
        lines = [] # empty list, as the file doesn't exist, so has no inputs yet

    #Determine the next entry-number based on the content:
    if len(lines) > 0:
        # Find the last used number by checking the last "username/email" entry
        last_number = 0 
        for line in lines:
            if "username" in line:
                last_number +=1
    else:
        last_number = 0 


    # Append the new entry to the file
    with open("Password_Vault.txt", "a") as file:
        for (key, value) in password_info.items():

            if key == "website" and last_number > 0:
                file.write("\n" + f"{last_number + 1}. "  + key + ": " + value)   

            elif key == "website" and last_number == 0:
                file.write("----------- My Passwords ---------\n")
                file.write(f"{last_number+1}. "  + key + ": " + value)  

            elif key == "username/email":
                file.write("\n   " + "username" + ": " + value+", ")   

            else:
                file.write(key + ": " + value + "\n")  
        
        warning_label.config(text = "Successful save")
        window.after(1200, func= disappear_warning_message)


def open_file():
    file_path = "Password_Vault.txt"

    if os.path.exists(file_path):
        os.startfile(file_path)
    else:
        warning_label.config(text = "There is no Passwrod-Vault made yet")


# Generate a random strong password
def generate_password():
    '''
    1) Length of at least 12-16 characters.
    2) Start with Uppercase letter
    3) Contain at least one number
    4) Contain at least one special character from [! @ # $ % &]
    '''

    special_char = ['!', '@', '#', '$', '%', '&']
    random_uppercase_letter = string.ascii_uppercase
    random_lowcase_letter = string.ascii_lowercase
    random_integer = string.digits

    new_password = ""
    for index in range(random.randint(11,15)):
        if index == 0:
            new_password += random.choice(string.ascii_uppercase)
        else:
            random_choice_list = random.choice([special_char, random_lowcase_letter, 
                                                random_integer, random_uppercase_letter])
            new_password += random.choice(random_choice_list)


    entry_password.delete(0, tk.END)  # This clears any existing content in the Entry.
    entry_password.insert(0, string = new_password) #The 0 means the content is inserted at the beginning of the Entry


# Buttons 
generate_button = tk.Button(text="Generate Password", width=15, command=generate_password)
generate_button.grid(column=1, row=4, sticky="E", )

add_button =  tk.Button(text="Memorize Password to Password-Vault", width= 30, command=memorize_the_info, bg="Gold")
add_button.grid(column=1, row=5, sticky="WE", columnspan=2, pady=(5,10))

open_button =  tk.Button(text="Open Vault (txt file)", width= 30, command=open_file, 
                         bg="grey", font=("Helvetica", 10, "bold"))
open_button.grid(column=1, row=7, sticky="WE", columnspan=2)

window.mainloop()
