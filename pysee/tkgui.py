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
        self.root.geometry("520x250")
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
        self.image_host = tk.StringVar()
        self.image_host.set("Select Image Host")
        self.optn_imghost = tk.OptionMenu(self.f_imghost,
                                          self.image_host, "Imgur", "Minus",
                                          "Photobucket", "PostImage")
        self.btn_editconfig = tk.Button(self.f_config,
                                        text="Edit Configuration File")
        self.btn_takescreenshot = tk.Button(self.f_master,
                                            text="Take a Screenshot")

        # packing
        self.lbl_maintitle.pack(fill="y")       # PySee title

        self.lbl_configtitle.pack()             # Config title
        self.btn_editconfig.pack(fill="both")   # Edit Config button

        self.lbl_imghosttitle.pack()            # Image Host title
        self.optn_imghost.pack(fill="both")     # Image Host dropdown menu

        self.f_title.pack()                     # Title frame
        self.btn_takescreenshot.pack()          # Take screenshot button

        self.f_imghost.pack(side='right')       # Image Host frame
        self.f_config.pack(side='left')         # Edit Config frame
        self.f_master.pack()                    # Master (atop root) frame

        self.root.mainloop()                    # init main loop


def create_gui():
    pysee_gui = Application()


if __name__ == '__main__':
    create_gui()
