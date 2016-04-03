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
from helpers import edit_text 

 
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.f_main = tk.Frame(master)
        self.f_imghost = tk.Frame(master)
        self.f_config = tk.Frame(master)


        # label creation
        self.lbl_maintitle = tk.Label(self.f_main, \
                                      text="PySee",
                                      bg='lightgreen',
                                      font=('Monospace', 24),
                                      pady=10,
                                      padx=50)
        self.lbl_imghosttitle = tk.Label(self.f_imghost, \
                                         text="Select your image host:",
                                         font=('Monospace', 10))
        self.lbl_configtitle = tk.Label(self.f_config, \
                                        text="Edit your config:",
                                        font=('Monospace', 10))

        # option menu
        self.image_host = tk.StringVar()
        self.image_host.set("Select Image Host")
        self.optn_imghost = tk.OptionMenu(self.f_imghost,
                                          self.image_host, "Imgur", "Minus",
                                          "Photobucket", "PostImage")
        self.btn_editconfig = tk.Button(self.f_config,
                                        text="Edit Configuration File",
                                        command=edit_text("~/.pysee/config.ini"))
        self.btn_takescreenshot = tk.Button(self.f_main,
                                            text="Take a Screenshot",
                                            command=main)

        # packing
        self.lbl_maintitle.pack(fill="x")       # PySee title

        self.lbl_configtitle.pack()             # Config title
        self.btn_editconfig.pack()              # Edit Config button

        self.lbl_imghosttitle.pack()            # Image Host title
        self.optn_imghost.pack()                # Image Host dropdown menu

        self.btn_takescreenshot.pack()          # Take screenshot button

        self.f_main.pack()                      # Title frame
        self.f_imghost.pack()                   # Image Host frame
        self.f_config.pack()                    # Edit Config frame


def create_gui():
    root = tk.Tk()
    root.geometry("300x280")
    root.title("PySee, a Lightweight Screenshot Tool")
    pysee_gui = Application(master=root)
    pysee_gui.mainloop()


if __name__ == '__main__':
    create_gui()
