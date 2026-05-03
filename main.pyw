"""AGSSpin: A spinning wheel written in Python for my school.
By Gabriel Alonso-Holt.
"""

# main.pyw
# -*- coding: utf-8 -*-
from tkinter import Tk, Button, Label, Entry, Toplevel, PhotoImage
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno, showinfo
from random import randint, sample, seed
from threading import Thread
from time import sleep, time
from webbrowser import open_new
from winsound import PlaySound, SND_ASYNC
from PIL import Image

print("INIT: program started")
names: list[str] = []


def load_names() -> None:
    """Open and parse the text file of names."""
    global names
    filename: str = askopenfilename(
        title="Open",
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    print("INFO: file dialog launched")
    file_label.config(text=f"File: {filename!s}")
    print(f"DEBUG: filename = {filename!s}")

    # Read filenames from text file and remove \n
    with open(file=filename, mode="r", encoding="utf-8") as file:
        names = [line.rstrip("\n") for line in file.readlines()]
        print("INFO: file loaded!")
        print(f"DEBUG: {names!s}")


def spin_in_bg() -> None:
    """Perfom the wheel spinning operation in the background."""
    global names
    notify_label.config(text="spinning wheel...")

    root_1: Toplevel = Toplevel(master=root)
    root_1.title("spinning wheel...")
    root_1.attributes("-topmost", 1)

    wheel_image: PhotoImage = PhotoImage(file=r"wheel.png")

    gif_label: Label = Label(master=root_1, image=wheel_image)
    gif_label.pack()

    wheel_path: str = r"wheel_anim.gif"
    wheel = Image.open(wheel_path)
    frames = wheel.n_frames  # type: ignore

    gif_label.config(image="")

    photoimage_objects: list[PhotoImage] = []
    for i in range(0, frames):
        obj: PhotoImage = PhotoImage(file=wheel_path, format=f"gif -index {i}")
        photoimage_objects.append(obj)

    def animation(current_frame: int = 0) -> None:
        global loop
        image: PhotoImage = photoimage_objects[current_frame]

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

    root_1.title("We have a winner!")
    notify_label.config(text="We have a winner!")

    print("INFO: We have a winner!")
    PlaySound(r"win.wav", SND_ASYNC)
    showinfo(title="We have a winner!", message=f"The winner is {name!s}")

    print(f"DEBUG: The winner is {name!s}")
    sure: bool = askyesno(title="Remove?", message="Remove winners?")
    print(f"DEBUG: name_list = {name_list!s}")
    if sure:
        for name_to_remove in name_list:
            names.remove(name_to_remove)
    root_1.destroy()


def spin() -> None:
    """Start `spin_in_bg()`"""
    # Use a thread to prevent freezing
    thread: Thread = Thread(target=spin_in_bg)
    print("INFO: thread started")
    thread.start()


def show_about() -> None:
    """Show the about window."""
    root_1: Toplevel = Toplevel(master=root)
    root_1.title("About this program")
    root_1.geometry("300x175")

    def github() -> None:
        open_new("https://github.com/Gabriel-H189/AGSSpin")

    about_label: Label = Label(
        master=root_1,
        text="AGSSpin v1.2\nBy Gabriel Alonso-Holt",
        font=("calibri", 16, "bold"),
    )
    about_label.pack(pady=5)  # type: ignore

    gh_button: Button = Button(master=root_1, text="view project page", command=github)
    gh_button.pack(pady=7)  # type: ignore


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

number_names_label: Label = Label(master=root, text="Enter number of names: ")
number_names_label.pack()
print("INIT: number of names label created")

names_entry: Entry = Entry(master=root)
names_entry.pack()
print("INIT: names entry created")

spin_time_label: Label = Label(master=root, text="Spin time (seconds): ")
spin_time_label.pack(pady=2)
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

about: Button = Button(
    master=root,
    text="i",
    command=show_about,
)
about.place(x=275, y=265)
print("INIT: about button created")

if __name__ == "__main__":
    print("INIT: main loop started")
    root.mainloop()
