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
from tkinter import Button, Label, Frame, OptionMenu, StringVar

from pysee import take_screenshot
from helpers import edit_text


class Application(tk.Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("PySee, a Lightweight Screenshot Tool")

        self.f_main = Frame(master)
        self.f_imghost = Frame(master)
        self.f_config = Frame(master)

        self.lbl_main = Label(self.f_main,
                              text="PySee",
                              font=('Monospace', 24))
        self.lbl_imghost = Label(self.f_imghost,
                                 text="Select your image host:",
                                 font=('Monospace', 10))
        self.lbl_config = Label(self.f_config,
                                text="Edit Configuration File:",
                                font=('Monospace', 10))

        self.image_host = StringVar()
        self.image_host.set("Select Image Host")
        self.optn_imghost = OptionMenu(self.f_imghost,
                                       self.image_host,
                                       "Imgur.com",
                                       "Uploads.im")
        self.btn_editconfig = Button(self.f_config,
                                     text="Open in Text Editor",
                                     command=lambda:
                                      edit_text("~/.pysee/config.ini"))
        self.btn_screenshot = Button(self.f_main,
                                     text="Take a Screenshot",
                                     command=lambda:
                                      take_screenshot(root=master,
                                                      image_host="I",
                                                      clipboard=True))

        # packing
        self.lbl_main.pack(fill="x")  # PySee title

        self.lbl_config.pack()        # Config title
        self.btn_editconfig.pack()    # Edit Config button

        self.lbl_imghost.pack()       # Image Host title
        self.optn_imghost.pack()      # Image Host dropdown menu

        self.btn_screenshot.pack()    # Take screenshot button

        self.f_main.pack()            # Title frame
        self.f_imghost.pack()         # Image Host frame
        self.f_config.pack()          # Edit Config frame


def create_gui():
    root = tk.Tk()
    root.geometry("300x280")
    root.resizable(width=False, height=False)
    pysee_gui = Application(master=root)
    pysee_gui.mainloop()


if __name__ == '__main__':
    create_gui()
