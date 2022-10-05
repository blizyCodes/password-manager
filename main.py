from tkinter import *
import random
from tkinter import messagebox
from pyperclip import copy
import json


# ---------------------------- Search ------------------------------- #
def find_password():
    try:
        with open("db.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(
            message="No Data File Found")
    else:
        website = website_entry.get()
        if website in data:
            messagebox.showinfo(
                message=f"Username: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(
                message="No details found for requested website")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    copy(password)
    copied_label.config(text="Copied to Clipboard", fg="green")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_entry = {website: {
        "email": email,
        "password": password,
    }}

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(
            message="An empty field is like an empty existence. Go fill that up man"
        )
    else:
        try:
            with open("db.json", "r") as file:
                data = json.load(file)
                data.update(new_entry)
        except FileNotFoundError:
            with open("db.json", "w") as file:
                json.dump(new_entry, file, indent=4)
        else:
            with open("db.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            copied_label.config(text="")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, bg="black")
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)

website_label = Label(
    text="Website:",
).grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, sticky="EW")

email_label = Label(
    text="Email/Username:",
).grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
password_label = Label(
    text="Password: ",
).grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")
generate_button = Button(text="Generate", command=generate_password)
generate_button.grid(column=2, row=3)
copied_label = Label(text="")
copied_label.grid(column=1, row=4, sticky="W")
add_button = Button(text="Add", width=36, command=save).grid(
    column=1, row=5, columnspan=2
)

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1)


canvas.grid(column=1, row=0)


window.mainloop()
