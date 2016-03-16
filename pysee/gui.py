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
        #self.root.geometry("520x480+8000+750")
        self.root.title("PySee, a Lightweight Screenshot Tool")
        
        # f_master: frame atop of root
        self.f_master = tk.Frame(self.root,
                                 bg = 'white',
                                 width = 520,
                                 height = 400)
        self.f_master.pack(fill="both", expand=True)
        # f_imghost: frame for right side/img host selection
        self.f_imghost = tk.Frame(self.f_master,
                                  bg = 'lightsalmon', 
                                  height=200,
                                  width=260).grid(row=0,
                                                  column=0)
        # f_config: frame for left side/config editor
        self.f_config = tk.Frame(self.f_master,
                                 bg = 'purple',
                                 height=200,
                                 width=260).grid(row=0,
                                                 column=1)

        # label creation
        self.lbl_maintitle = tk.Label(self.f_master, \
                                      text="PySee")
        self.lbl_imghosttitle = tk.Label(self.f_imghost, \
                                         text="Select your image host:")
        self.lbl_configtitle = tk.Label(self.f_config, \
                                        text = "Edit your config:")
        self.lbl_maintitle.config(bg='lightgreen',
                                  font=('Monospace', 24),
                                  pady=10,
                                  padx=50)
        self.lbl_maintitle.pack()
        self.lbl_imghosttitle.config(bg='lightgreen',
                                  font=('Monospace', 24),
                                  pady=10,
                                  padx=50)
        self.lbl_imghosttitle.place(in_=self.f_imghost)

        self.lbl_configtitle.config(bg='lightgreen',
                                  font=('Monospace', 24),
                                  pady=10,
                                  padx=50)
        self.lbl_configtitle.place(in_=self.f_config)

        # init main loop
        self.root.mainloop()


def main():
    pysee_gui = Application()


if __name__ == '__main__':
    main()
