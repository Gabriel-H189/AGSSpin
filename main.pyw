# challenge.py
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import random
import threading
import time
import winsound

print("INIT: program started")
names = []


def load_names():
    global names
    filename = fd.askopenfilename(title="Open", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    print("INFO: file dialog launched")
    file_label.config(text=f"File: {filename}")
    print(f"DEBUG: filename = {filename}")

    # Read filenames from text file and remove \n
    with open(filename, "r") as file:
        names = [line.rstrip("\n") for line in file.readlines()]
        print("INFO: file loaded!")
        print(f"DEBUG: {names}")


# TODO: actual spin logic
def spin_in_bg():
    global names
    notify_label.config(text="spinning wheel...")
    root1 = tk.Toplevel()
    root1.title("spinning wheel...")
    root1.attributes("-topmost", 1)
    wheel = tk.PhotoImage(file="wheel.png")
    tk.Label(root1, image=wheel, width=300, height=300).pack()
    print("INFO: spinning wheel...")

    # Get number of names and convert to int - default 1
    number_of_names = names_entry.get()
    if number_of_names == "":
        number_of_names = 1
    else:
        number_of_names = int(number_of_names)
    print(f"DEBUG: number_of_names = {number_of_names}")

    # Get spin time and convert to int - default 10
    spin_time = time_entry.get()
    if spin_time == "":
        spin_time = 10
    else:
        spin_time = int(spin_time)
    print(f"DEBUG: spin_time = {spin_time}")

    # Seed and choose winner (s)
    random.seed()
    print("INFO: seeded successfully")
    name = random.sample(names, number_of_names)
    
    print("INFO: name chosen!")
    print(f"DEBUG: waiting for {spin_time} seconds")
    time.sleep(spin_time)
    notify_label.config(text="We have a winner!")
    
    print("INFO: We have a winner!")
    winsound.PlaySound("win.wav", winsound.SND_ASYNC)
    msg.showinfo(title="We have a winner!", message=f"The winner is {name}")
    
    print(f"DEBUG: The winner is {name}")
    root1.destroy()


def spin():
    # Use a thread to prevent freezing
    thread = threading.Thread(target=spin_in_bg)
    print("INFO: thread started")
    thread.start()


root = tk.Tk()
root.title("AGS Spin The Wheel")
root.geometry("300x300+200+200")
root.resizable(False, False)
print("INIT: window created")

title = tk.Label(root, text="AGS Spin The Wheel")
title.pack()
print("INIT: title label created")

file_label = tk.Label(root, text="File: <no file loaded>")
file_label.pack(pady=10)
print("INIT: file label created")

button = tk.Button(root, text="Load names from file", command=load_names)
button.pack(pady=5)
print("INIT: load button created")

tk.Label(root, text="Enter number of names: ").pack()
print("INIT: label created")
names_entry = tk.Entry(root)
names_entry.pack()
print("INIT: names entry created")

tk.Label(root, text="Spin time (seconds): ").pack(pady=2)
print("INIT: spin time label created")
time_entry = tk.Entry(root)
time_entry.pack()
print("INIT: time entry created")

notify_label = tk.Label(root, text="No winners yet!")
notify_label.pack(pady=2)
print("INIT: notify label created")

btn2 = tk.Button(root, text="Spin!", command=spin)
btn2.pack()
print("INIT: spin button created")

about = tk.Button(root, text="i", command= lambda: msg.showinfo(title="About", message="Program made by Gabriel"))
about.place(x=275, y=265)
print("INIT: about button created")

if __name__ == "__main__":
    print("INIT: main loop started")
    root.mainloop()
