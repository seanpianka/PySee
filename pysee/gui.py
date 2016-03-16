#!/usr/bin/python3
"""
gui
~~~~~

Create the graphical user interface for the
user to take screenshots with and choose image
host to upload to.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

"""
import tkinter as tk
import pysee


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)

    def createWidgets(self, master):
        self.take_screenshot = tk.Button(self)
        self.take_screenshot["text"] = "Take Screenshot"
        self.take_screenshot["command"] = pysee.run() 
        self.take_screenshot.pack(side="top")

        self.quit = tk.Button(self, text="Quit", fg="red", command=master.destroy)
        self.quit.pack(side="bottom")


def main():
    root = tk.Tk()
    root.geometry("640x480+8000+750")
    root.title("PySee - Lightweight Screenshot Tool")

    app = Application(master=root)

    root.mainloop()


if __name__ == '__main__':
    main()
