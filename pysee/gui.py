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
from pysee import main


class Application(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("520x480+8000+750")
        self.root.title("PySee, a Lightweight Screenshot Tool")

        # f_master: frame atop of root
        self.f_master = tk.Frame(self.root,
                                 bg='white',
                                 width=520,
                                 height=500)
        self.f_title = tk.Frame(self.f_master,
                                bg='blue',
                                width=520,
                                height=100)

        # f_imghost: frame for right side/img host selection
        self.f_imghost = tk.Frame(self.f_master,
                                  bg='lightsalmon',
                                  height=400,
                                  width=260)
        # f_config: frame for left side/config editor
        self.f_config = tk.Frame(self.f_master,
                                 bg='purple',
                                 height=400,
                                 width=260)

        # label creation
        self.lbl_maintitle = tk.Label(self.f_title, \
                                      text="PySee",
                                      bg='lightgreen',
                                      font=('Monospace', 24),
                                      pady=10,
                                      padx=50)
        self.lbl_imghosttitle = tk.Label(self.f_imghost, \
                                         text="Select your image host:",
                                         bg='lightgreen',
                                         font=('Monospace', 16),
                                         pady=10,
                                         padx=50)
        self.lbl_configtitle = tk.Label(self.f_config, \
                                        text="Edit your config:",
                                        bg='lightgreen',
                                        font=('Monospace', 16),
                                        pady=10,
                                        padx=50)

        self.lbl_maintitle.pack(expand=True, side='top')
        self.lbl_imghosttitle.pack(expand=True, side='right')
        self.lbl_configtitle.pack(expand=True, side='left')

        self.f_title.pack(expand=True, side='top')
        self.f_imghost.pack(expand=True)
        self.f_config.pack(expand=True, side='left')
        self.f_master.pack()

        # init main loop
        self.root.mainloop()


def create_gui():
    pysee_gui = Application()


if __name__ == '__main__':
    create_gui()
