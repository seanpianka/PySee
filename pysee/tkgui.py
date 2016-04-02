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
        self.root.geometry("520x480")
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

        # option menu
        self.var = ""
        self.optn_imghost = tk.OptionMenu(self.f_imghost,
                                          self.var, "Select Image Host",
                                          "Imgur", "Minus",
                                          "Photobucket", "PostImage")
        self.btn_editconfig = tk.Button(self.f_config,
                                        text="Edit Configuration File")
        self.btn_takescreenshot = tk.Button(self.f_master,
                                            text="Take a Screenshot")

        # packing
        self.lbl_maintitle.pack(fill="y")

        self.lbl_configtitle.pack()
        self.btn_editconfig.pack(fill="both", expand=True)

        self.lbl_imghosttitle.pack()
        self.optn_imghost.pack(fill="both", expand=True)


        self.f_title.pack()
        self.btn_takescreenshot.pack()

        self.f_imghost.pack()
        self.f_config.pack(side='left')
        self.f_master.pack()

        # init main loop
        self.root.mainloop()


def create_gui():
    pysee_gui = Application()


if __name__ == '__main__':
    create_gui()
