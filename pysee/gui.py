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
from pysee import run


class Application(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        # self.root.geometry("640x480+8000+750")
        self.root.title("PySee")
        
        # label creation
        self.lbl_maintitle = tk.Label(self.root, \
                                      text="PySee, a Lightweight Screenshot Tool")
        self.lbl_imghosttitle = tk.Label(self.root, \
                                         text="Select your image host:")
        self.lbl_configtitle = tk.Label(self.root, \
                                         text = "Edit your configuration file:")

        # packing
        self.lbl_maintitle.pack()
        self.lbl_imghosttitle.pack(side="left")
        self.lbl_configtitle.pack(side="right")

        # init main loop
        self.root.mainloop()


def main():
    pysee_gui = Application()


if __name__ == '__main__':
    main()
