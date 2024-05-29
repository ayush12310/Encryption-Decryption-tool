import sqlite3
from tkinter import *
from tkinter import messagebox
import os
import csv
import base64
from PIL import Image
from tkinter import filedialog


def create_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)


if __name__ == "__main__":
    name = "Outputs"
    create_folder(name)


def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) + ord(key_c)) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string.encode()).decode()


def decode(key, string):
    string = base64.urlsafe_b64decode(string).decode()
    decoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        decoded_c = chr((256 + ord(string[i]) - ord(key_c)) % 256)
        decoded_chars.append(decoded_c)
    decoded_string = ''.join(decoded_chars)
    return decoded_string


def create_database():
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                        id INTEGER PRIMARY KEY,
                        website TEXT,
                        username TEXT,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()


def add_login_info():
    create_database()
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if len(website) == 0:
        messagebox.showwarning(title="Crypt says", message="Please enter website name")
    elif len(username) == 0:
        messagebox.showwarning(title="Crypt says", message="Please enter username")
    elif len(password) == 0:
        messagebox.showwarning(title="Crypt says", message="Please enter password")
    else:
        encoded_password = encode("mysecretkey", password)
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO credentials (website, username, password) VALUES (?, ?, ?)", (website, username, encoded_password))
        conn.commit()
        conn.close()

    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)


def view_login_info():
    logins_window = Toplevel()
    logins_window.title("Saved Data")

    scrollbar = Scrollbar(logins_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    logins_listbox = Listbox(logins_window, yscrollcommand=scrollbar.set)
    logins_listbox.pack(fill=BOTH, expand=True)

    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials")
    rows = cursor.fetchall()
    for row in rows:
        logins_listbox.insert(END, "Website: " + row[1])
        logins_listbox.insert(END, "Username: " + row[2])
        logins_listbox.insert(END, "Password: " + decode("mysecretkey", row[3]))
        logins_listbox.insert(END, "")

    conn.close()
    scrollbar.config(command=logins_listbox.yview)


def encrypt_image():
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                r ^= 255
                g ^= 255
                b ^= 255
                pixels[i, j] = (r, g, b)
        save_path = filedialog.asksaveasfilename(filetypes=[("PNG Files", "*.png")], defaultextension=".png", initialdir='Outputs')
        image.save(save_path)


def decrypt_image():
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)
        pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                r ^= 255
                g ^= 255
                b ^= 255
                pixels[i, j] = (r, g, b)
        save_path = filedialog.asksaveasfilename(filetypes=[("PNG Files", "*.png")], defaultextension=".png", initialdir='Outputs')
        image.save(save_path)


root = Tk()
root.title("Cryptor: By Crypt4007")

website_label = Label(root, text="Website:")
website_label.grid(row=0, column=0, padx=5, pady=5)

website_entry = Entry(root, width=30)
website_entry.grid(row=0, column=1, padx=5, pady=5)

username_label = Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=5, pady=5)

username_entry = Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=5, pady=5)

password_label = Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=5, pady=5)

password_entry = Entry(root, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = Button(root, text="Add", command=add_login_info)
add_button.grid(row=3, column=0, padx=5, pady=5)

view_button = Button(root, text="View", command=view_login_info)
view_button.grid(row=3, column=1, padx=5, pady=5)

encrypt_button = Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.grid(row=4, column=0, padx=5, pady=5)

decrypt_button = Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.grid(row=4, column=1, padx=5, pady=5)

status_label = Label(root, text="")
status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
