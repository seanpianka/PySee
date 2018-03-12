import tkinter as tk
from tkinter import ttk
import pysee
import keyboard


root = tk.Tk()
root.title("PySee")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=("N", "W", "E", "S"))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Now listening for hotkeys inputs...").grid(column=2, row=2, sticky=("N", "S", "E", "W"))

keyboard.add_hotkey("ctrl+shift+2", lambda: pysee.run(mode="full"))
keyboard.add_hotkey("ctrl+shift+3", lambda: pysee.run(mode="window"))
keyboard.add_hotkey("ctrl+shift+4", lambda: pysee.run(mode="region"))

root.mainloop()
