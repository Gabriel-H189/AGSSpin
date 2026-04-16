# main.pyw
# -*- coding: utf-8 -*-
from tkinter import Tk, Button, Label, Entry, Toplevel, PhotoImage
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno, showinfo
from random import randint, sample, seed
from threading import Thread
from time import sleep, time
from winsound import PlaySound, SND_ASYNC
from PIL import Image

print("INIT: program started")
names: list[str] = []


def load_names() -> None:
    global names
    filename: str = askopenfilename(title="Open", defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    print("INFO: file dialog launched")
    file_label.config(text=f"File: {filename!s}")
    print(f"DEBUG: filename = {filename!s}")

    # Read filenames from text file and remove \n
    with open(filename, "r") as file:
        names = [line.rstrip("\n") for line in file.readlines()]
        print("INFO: file loaded!")
        print(f"DEBUG: {names!s}")


def spin_in_bg() -> None:
    global names
    notify_label.config(text="spinning wheel...")
    root1: Toplevel = Toplevel()
    root1.title("spinning wheel...")
    root1.attributes("-topmost", 1)
    wheel_image: PhotoImage = PhotoImage(file=r"wheel.png")
    gif_label: Label = Label(master=root1, image=wheel_image)
    gif_label.pack()
    
    wheel_path: str = r"wheel_anim.gif"
    wheel = Image.open(wheel_path)
    frames = wheel.n_frames # type: ignore
    
    gif_label.config(image="")
        
    photoimage_objects = []
    for i in range(frames):
        obj: PhotoImage = PhotoImage(file=wheel_path, format=f"gif -index {i}")
        photoimage_objects.append(obj)
        
    def animation(current_frame: int=0) -> None:
        global loop
        image = photoimage_objects[current_frame]

        gif_label.configure(image=image)
        current_frame += 1

        if current_frame == frames:
            current_frame = 0

        loop = root.after(50, lambda: animation(current_frame))


    def stop_animation() -> None:
        root.after_cancel(loop)
        
    print("INFO: spinning wheel...")
    
    def spin_sound() -> None:
        Thread(target=lambda: PlaySound(r"spin.wav", SND_ASYNC)).start()

    # Get number of names and convert to int - default 1
    number_of_names: int | str = names_entry.get()
    if number_of_names == "":
        number_of_names = 1
    else:
        number_of_names = int(number_of_names)
    print(f"DEBUG: number_of_names = {number_of_names:,}")

    # Get spin time and convert to int - default 10
    spin_time: int | str = time_entry.get()
    if spin_time == "":
        spin_time = 10
    else:
        spin_time = int(spin_time)
    print(f"DEBUG: spin_time = {spin_time:,}")

    # Seed and choose winner (s)
    seed(randint(a=1, b=round(time())))
    print("INFO: seeded successfully")
    name_list: list[str] = sample(names, number_of_names)
    name: str = ", ".join(name_list)
    
    print("INFO: name chosen!")
    print(f"DEBUG: waiting for {spin_time:,} seconds")
    spin_sound()
    print("INFO: playing sound")
    animation()
    print("INFO: playing animation")
    sleep(spin_time)
    stop_animation()
    root1.title("We have a winner!")
    notify_label.config(text="We have a winner!")
    
    print("INFO: We have a winner!")
    PlaySound("win.wav", SND_ASYNC)
    showinfo(title="We have a winner!", message=f"The winner is {name!s}")
    
    print(f"DEBUG: The winner is {name!s}")
    sure: bool = askyesno(title="Remove?", message="Remove winners?")
    print(f"DEBUG: name_list = {name_list!s}")
    if sure:
        for name_to_remove in name_list:
            names.remove(name_to_remove)
    root1.destroy()


def spin() -> None:
    # Use a thread to prevent freezing
    thread: Thread = Thread(target=spin_in_bg)
    print("INFO: thread started")
    thread.start()


root: Tk = Tk()
root.title("AGS Spin The Wheel")
root.geometry("300x300+200+200")
root.resizable(width=False, height=False)
print("INIT: window created")

title: Label = Label(master=root, text="AGS Spin The Wheel")
title.pack()
print("INIT: title label created")

file_label: Label = Label(master=root, text="File: <no file loaded>")
file_label.pack(pady=10)
print("INIT: file label created")

button: Button = Button(master=root, text="Load names from file", command=load_names)
button.pack(pady=5)
print("INIT: load button created")

Label(master=root, text="Enter number of names: ").pack()
print("INIT: label created")
names_entry: Entry = Entry(master=root)
names_entry.pack()
print("INIT: names entry created")

Label(master=root, text="Spin time (seconds): ").pack(pady=2)
print("INIT: spin time label created")
time_entry: Entry = Entry(master=root)
time_entry.pack()
print("INIT: time entry created")

notify_label: Label = Label(master=root, text="No winners yet!")
notify_label.pack(pady=2)
print("INIT: notify label created")

btn2: Button = Button(master=root, text="Spin!", command=spin)
btn2.pack()
print("INIT: spin button created")

about: Button = Button(master=root, text="i", command= lambda: showinfo(title="About", message="Program made by Gabriel Alonso-Holt"))
about.place(x=275, y=265)
print("INIT: about button created")

if __name__ == "__main__":
    print("INIT: main loop started")
    root.mainloop()
