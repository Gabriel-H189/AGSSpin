"""AGSSpin: A spinning wheel written in Python for my school.
By Gabriel Alonso-Holt.
"""

# main.pyw
# -*- coding: utf-8 -*-
from math import log

from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkToplevel
from tkinter import Toplevel, Label, PhotoImage
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno, showinfo
from random import randint, sample, seed
from threading import Thread
from time import sleep, time
from webbrowser import open_new
from winsound import PlaySound, SND_ASYNC
from PIL import Image
from loguru import logger

logger.info("INIT: program started")
names: list[str] = []


def load_names() -> None:
    """Open and parse the text file of names."""
    global names
    filename: str = askopenfilename(
        title="Open",
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    logger.info("file dialog launched")
    file_label.configure(text=f"File: {filename!s}")
    logger.debug(f"filename = {filename!s}")

    # Read filenames from text file and remove \n
    with open(file=filename, mode="r", encoding="utf-8") as file:
        names = [line.rstrip("\n") for line in file.readlines()]
        logger.info("file loaded!")
        logger.debug(f"{names!s}")


def spin_in_bg() -> None:
    """Perfom the wheel spinning operation in the background."""
    global names
    notify_label.configure(text="spinning wheel...")

    root_1: Toplevel = Toplevel(master=root)
    root_1.title("spinning wheel...")
    root_1.attributes("-topmost", 1)
    logger.info("spinning window created")

    wheel_image = PhotoImage(file=r"wheel.png")

    gif_label: Label = Label(master=root_1, image=wheel_image)
    gif_label.pack()
    logger.info("gif label created")

    wheel_path: str = r"wheel_anim.gif"
    wheel = Image.open(wheel_path)
    frames = wheel.n_frames  # type: ignore

    gif_label.config(image="")

    photoimage_objects: list[PhotoImage] = []
    for i in range(0, frames):
        obj: PhotoImage = PhotoImage(file=wheel_path, format=f"gif -index {i}")
        photoimage_objects.append(obj)
        logger.info(f"reading image {i}...")

    def animation(current_frame: int = 0) -> None:
        global loop
        image: PhotoImage = photoimage_objects[current_frame]
        logger.info(f"setting image {current_frame}")

        gif_label.config(image=image)
        current_frame += 1

        if current_frame == frames:
            current_frame = 0

        loop = root.after(50, lambda: animation(current_frame))

    def stop_animation() -> None:
        logger.info("stopping animation...")
        root.after_cancel(loop)

    logger.info("spinning wheel...")

    def spin_sound() -> None:
        Thread(target=lambda: PlaySound(r"spin.wav", SND_ASYNC)).start()

    # Get number of names and convert to int - default 1
    number_of_names: int | str = names_entry.get()
    if number_of_names == "":
        number_of_names = 1
    else:
        number_of_names = int(number_of_names)
    logger.debug(f"number_of_names = {number_of_names:,}")

    # Get spin time and convert to int - default 10
    spin_time: int | str = time_entry.get()
    if spin_time == "":
        spin_time = 10
    else:
        spin_time = int(spin_time)
    logger.debug(f"spin_time = {spin_time:,}")

    # Seed and choose winner (s)
    seed(randint(a=1, b=round(time())))
    logger.info("seeded successfully")
    name_list: list[str] = sample(names, number_of_names)
    name: str = ", ".join(name_list)

    logger.info("name chosen!")
    logger.debug(f"waiting for {spin_time:,} seconds")
    spin_sound()
    logger.info("playing sound")

    animation()
    logger.info("playing animation")
    sleep(spin_time)
    stop_animation()

    root_1.title("We have a winner!")
    notify_label.configure(text="We have a winner!")

    logger.info("We have a winner!")
    logger.info("playing win sound...")
    PlaySound(r"win.wav", SND_ASYNC)

    logger.info("win message box displayed")
    showinfo(title="We have a winner!", message=f"The winner is {name!s}")

    logger.debug(f"The winner is {name!s}")
    sure: bool = askyesno(title="Remove?", message="Remove winners?")
    logger.debug(f"name_list = {name_list!s}")

    if sure:
        for name_to_remove in name_list:
            logger.debug(f"{name_to_remove} removed from list")
            names.remove(name_to_remove)

    root_1.destroy()


def spin() -> None:
    """Start `spin_in_bg()`"""
    # Use a thread to prevent freezing
    thread: Thread = Thread(target=spin_in_bg)
    logger.info("thread started")
    thread.start()


def show_about() -> None:
    """Show the about window."""
    root_1: CTkToplevel = CTkToplevel(master=root)
    root_1.title("About this program")
    root_1.geometry("300x175")
    root_1.resizable(False, False)
    logger.info("about window created")

    def github() -> None:
        open_new("https://github.com/Gabriel-H189/AGSSpin")
        logger.info("project page opened")

    about_label: CTkLabel = CTkLabel(
        master=root_1,
        text="AGSSpin v1.2\nBy Gabriel Alonso-Holt",
        font=("calibri", 16, "bold"),
    )
    about_label.pack(pady=5)  # type: ignore
    logger.info("about label created")

    gh_button: CTkButton = CTkButton(
        master=root_1, text="view project page", command=github
    )
    gh_button.pack(pady=7)  # type: ignore
    logger.info("project page button created")


root: CTk = CTk()
root.title("AGS Spin The Wheel")
root.geometry(geometry_string="300x300+200+200")
root.resizable(width=False, height=False)
logger.info("INIT: window created")

title: CTkLabel = CTkLabel(master=root, text="AGS Spin The Wheel")
title.pack()
logger.info("INIT: title label created")

file_label: CTkLabel = CTkLabel(master=root, text="File: <no file loaded>")
file_label.pack(pady=10)
logger.info("INIT: file label created")

button: CTkButton = CTkButton(
    master=root, text="Load names from file", command=load_names
)
button.pack(pady=5)
logger.info("INIT: load button created")

number_names_label: CTkLabel = CTkLabel(master=root, text="Enter number of names: ")
number_names_label.pack()
logger.info("INIT: number of names label created")

names_entry: CTkEntry = CTkEntry(master=root)
names_entry.pack()
logger.info("INIT: names entry created")

spin_time_label: CTkLabel = CTkLabel(master=root, text="Spin time (seconds): ")
spin_time_label.pack(pady=2)
logger.info("INIT: spin time label created")

time_entry: CTkEntry = CTkEntry(master=root)
time_entry.pack()
logger.info("INIT: time entry created")

notify_label: CTkLabel = CTkLabel(master=root, text="No winners yet!")
notify_label.pack(pady=2)
logger.info("INIT: notify label created")

btn2: CTkButton = CTkButton(master=root, text="Spin!", command=spin)
btn2.pack()
logger.info("INIT: spin button created")

about: CTkButton = CTkButton(
    master=root,
    text="i",
    width=10,
    command=show_about,
)
about.place(x=275, y=265)
logger.info("INIT: about button created")

if __name__ == "__main__":
    logger.info("INIT: main loop started")
    root.mainloop()
    logger.info("program closed")
