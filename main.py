import sys
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

gui = Tk()

key_grabber = None
output_file = None
fernet = None

def exit_program():
    sys.exit()
def select_output():
    global output_file
    output_file = Path(askopenfilename())
    print("SELECTED FILE: " + str(output_file))
def select_key():
    global key_grabber
    key_grabber = Path(askopenfilename())
    print("SELECTED KEY: " + str(key_grabber))

def open_popup():
   popup = Toplevel(gui)
   def close_window():
       popup.destroy()
   popup.geometry("290x70")
   popup.title("Exit")
   inner_box = ttk.Frame(popup, padding="10 10 12 12")
   inner_box.grid(column=0, row=0, sticky=(N, W, E, S))
   popup.columnconfigure(0, weight=1)
   popup.rowconfigure(0, weight=1)
   ttk.Label(inner_box, text= "Are you sure you want to quit?").grid(column=2, row=1, sticky=W)
   yes_select = ttk.Button(inner_box, text="Yes", command=exit_program, width=7)
   yes_select.grid(column=1, row=2, sticky=(W, E))
   no_select = ttk.Button(inner_box, text="No", command=close_window, width=7)
   no_select.grid(column=3, row=2, sticky=(W, E))

def use_key():
    global fernet
    if key_grabber.is_file():
        with open(key_grabber, 'rb') as cryptkey:
            key = cryptkey.read()
        fernet = Fernet(key)
        print("KEY IN USE: " + str(key_grabber))
def create_key():
    global fernet
    key = Fernet.generate_key()
    with open('created.key', 'wb') as cryptkey:
        cryptkey.write(key)
    fernet = Fernet(key)
    key_grabber = Path("./created.key")
    print("KEY IN USE: " + str(key_grabber))

def encrypt_output():
    if output_file.is_file():
        with open(output_file, "rb") as file:
            original = file.read()
        encrypt_data = fernet.encrypt(original)
        with open(output_file, "wb") as encrypted_file:
            encrypted_file.write(encrypt_data)
        print("ENCRYPTED FILE: " + str(output_file))
    else:
        sys.exit()
def decrypt_output():
    if output_file.is_file():
        with open(output_file, "rb") as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(output_file, "wb") as decrypted_output_data:
            decrypted_output_data.write(decrypted)
        print("DECRYPTED FILE: " + str(output_file))
    

gui.geometry("380x150")
gui.title("Standalone File Encrypt/Decrypt")

outer_box = ttk.Frame(gui, padding="10 10 12 12")
outer_box.grid(column=0, row=0, sticky=(N, W, E, S))
gui.columnconfigure(0, weight=1)
gui.rowconfigure(0, weight=1)

# File encrypt/decrypt
ttk.Label(outer_box, text="Select a file to use.").grid(column=1, row=1, sticky=W)
output_path_select = ttk.Button(outer_box, text="Choose a file.", command=select_output, width=7)
output_path_select.grid(column=1, row=2, sticky=(W, E))
encrypt_output_button = ttk.Button(outer_box, text="ENCRYPT", command=encrypt_output, width=7)
encrypt_output_button.grid(column=1, row=3, sticky=(W, E))
decrypt_output_button = ttk.Button(outer_box, text="DECRYPT", command=decrypt_output, width=7)
decrypt_output_button.grid(column=1, row=4, sticky=(W, E))

# Key selector
ttk.Label(outer_box, text="Select a key to use.").grid(column=3, row=1, sticky=W)
key_path_select = ttk.Button(outer_box, text="Choose key.", command=select_key, width=7)
key_path_select.grid(column=3, row=2, sticky=(W, E))
use_key_file = ttk.Button(outer_box, text="Use key.", command=use_key, width=7)
use_key_file.grid(column=3, row=3, sticky=(W, E))
create_new_key = ttk.Button(outer_box, text="Create new key.", command=create_key, width=7)
create_new_key.grid(column=3, row=4, sticky=(W, E))

quit_button = ttk.Button(outer_box, text="Exit", command=open_popup, width=7)
quit_button.grid(column=2, row=5, sticky=(W, E))

ttk.Label(outer_box, text="github.com/horsellcommon").grid(column=2, row=6, sticky=W)

input()
