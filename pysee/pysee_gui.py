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
import sys
import os
import subprocess
import tkinter as tk
import webbrowser
from tkinter import ttk
from collections import OrderedDict

from pysee import take_screenshot
from helpers import edit_text
from configs import paths, config_file_name


SOURCE_URL = "https://github.com/seanpianka/pysee"
LARGE_FONT = ("Helvetica", 12)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
CONFIG_FILE = paths['config_dir_path'] + config_file_name
WINDOW_WIDTH = 380
WINDOW_HEIGHT = 240
LAST_MODE = ""
LAST_HOST = ""


if sys.platform == "win32":
    source_open = lambda url: os.startfile(url)
elif sys.platform == "darwin":
    source_open = lambda url: subprocess.Popen(['open', url])
else:
    try:
        source_open = lambda url: subprocess.Popen(['xdg-open', url])
    except OSError:
        source_open = lambda url: "Open a browser on: %s" % url


def capture(image_host, mode):
    take_screenshot(image_host=image_host, mode=mode)
    LAST_MODE = mode
    LAST_HOST = image_host


def popupmsg(msg):
    popup = tk.Toplevel()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=MEDIUM_FONT)
    label.pack(side="top", fill="x", pady=10)
    b1 = ttk.Button(popup, text="Close", command=popup.destroy)
    b1.pack()
    popup.mainloop()


class PySeeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.bmp") # icon for window
        tk.Tk.wm_title(self, "PySee Client")


        container = tk.Frame(self, bg="dark green")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) # minimum size, priority


        menubar = tk.Menu(container)

        capturemenu = tk.Menu(menubar, tearoff=1)
        capturemenu.add_command(label="Fullscreen",
            command=lambda: capture("imgur", "f"))
        capturemenu.add_command(label="Region",
            command=lambda: capture("imgur", "r"))
        capturemenu.add_command(label="Window",
            command=lambda: capture("imgur", "w"))
        capturemenu.add_command(label="Monitor",
            command=lambda: popupmsg("Not supported yet."))
        capturemenu.add_separator()
        capturemenu.add_command(label="Repeat Capture",
            command=lambda: capture(LAST_HOST, LAST_MODE))
        menubar.add_cascade(label="Capture", menu=capturemenu)

        uploadmenu = tk.Menu(menubar, tearoff=1)
        uploadmenu.add_command(label="Upload file",
            command=lambda: popupmsg("Not supported yet."))
        uploadmenu.add_command(label="Upload folder",
            command=lambda: popupmsg("Not supported yet."))
        uploadmenu.add_command(label="Upload from clipboard",
            command=lambda: popupmsg("Not supported yet."))
        uploadmenu.add_command(label="Upload from url",
            command=lambda: popupmsg("Not supported yet."))
        menubar.add_cascade(label="Upload", menu=uploadmenu)

        settingsmenu = tk.Menu(menubar, tearoff=1)
        settingsmenu.add_command(label="Edit Configuration File",
            command=lambda: self.show_frame(SettingsPage))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Imgur API",
            command=lambda: popupmsg("Not supported yet."))
        settingsmenu.add_command(label="Slimg API",
            command=lambda: popupmsg("Not supported yet."))
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        aboutmenu = tk.Menu(menubar, tearoff=1)
        aboutmenu.add_command(label="About",
            command=lambda: self.show_frame(AboutPage))
        aboutmenu.add_command(label="Source Code",
            command=lambda: source_open(SOURCE_URL))
        aboutmenu.add_command(label="Donate",
            command=lambda: popupmsg("Not supported yet."))
        menubar.add_cascade(label="About", menu=aboutmenu)

        tk.Tk.config(self, menu=menubar)


        self.frames = OrderedDict()
        self.MAX_ROW = 2

        for f in (CapturePage, UploadPage, SettingsPage, AboutPage):
            frame = f(container, self)
            self.frames[f] = (frame, frame.page_title)
            frame.grid(row=0, column=0, sticky="nsew",
                       columnspan=4, rowspan=self.MAX_ROW)

        for r in range(self.MAX_ROW):
            container.rowconfigure(r, weight=1)

        # width=(int(WINDOW_WIDTH * (1/len(self.frames.items())))),
        # Calculates the percentage of the screen that each button should
        # occupy. Same value for each button, dependent on number of buttons
        i = 0
        for page, title in self.frames.items():
            container.columnconfigure(i, weight=1)
            ttk.Button(container,
                       width=(int(WINDOW_WIDTH * (1/len(self.frames.items())))),
                       command=lambda page=page: self.show_frame(page),
                       text=title[1]).grid(row=self.MAX_ROW,
                                           column=i,
                                           sticky="ew")
            i+=1
        self.show_frame(AboutPage)

    def show_frame(self, controller):
        """ Displays the frame controller from self.frames at the "front" of
            the stack of frames.

        """
        frame = self.frames[controller][0]
        frame.tkraise()


class CapturePage(tk.Frame):
    page_title = "Capture"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(2):
            self.rowconfigure(i, weight=1)
        for i in range(2):
            self.columnconfigure(i, weight=1)

        cap_region = ttk.Button(self, text="Region",
                                command=lambda: capture("imgur", "r"))
        cap_fullscreen = ttk.Button(self, text="Fullscreen",
                                    command=lambda: capture("imgur", "f"))
        cap_monitor = ttk.Button(self, text="Monitor",
                                 command=lambda: popupmsg("Monitor"))
        cap_window = ttk.Button(self, text="Window",
                                command=lambda: capture("imgur", "w"))

        cap_region.grid(row=0, column=0)
        cap_fullscreen.grid(row=0, column=1)
        cap_monitor.grid(row=1, column=0)
        cap_window.grid(row=1, column=1)


class UploadPage(tk.Frame):
    page_title = "Upload"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(2):
            self.rowconfigure(i, weight=1)
        for i in range(2):
            self.columnconfigure(i, weight=1)

        upload_file = ttk.Button(self, text="Upload file",
                                command=lambda: popupmsg("Upload file"))
        upload_folder = ttk.Button(self, text="Upload folder",
                                   command=lambda: popupmsg("Upload folder"))
        upload_clipboard = ttk.Button(self, text="Upload clipboard",
                                      command=lambda: popupmsg("Upload clipboard"))
        upload_url = ttk.Button(self, text="Upload url",
                                command=lambda: popupmsg("Upload url"))

        upload_file.grid(row=0, column=0)
        upload_folder.grid(row=0, column=1)
        upload_clipboard.grid(row=1, column=0)
        upload_url.grid(row=1, column=1)

    def upload():
        pass


class SettingsPage(tk.Frame):
    page_title = "Settings"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(1):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        def save_changes():
            contents = settings_entry.get(0.0, "end")
            with open(CONFIG_FILE, "w") as f:
                f.write(contents)

        with open(CONFIG_FILE, "r") as f:
            config_contents = f.read()

        settings_entry = tk.Text(self)
        settings_entry.insert(0.0, config_contents)
        settings_entry.grid(padx=3, pady=(3, 0), row=0, column=0)


        button = ttk.Button(self, text="Save Changes",
                            command=lambda: save_changes())
        button.grid(pady=3, row=1, column=0)






class AboutPage(tk.Frame):
    page_title = "About"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        label = ttk.Label(self,
                         text="PySee, a lightweight media sharing tool for" +
                              " Linux and Mac OS X.",
                         justify="center",
                         wraplength=WINDOW_WIDTH - 20, # account for 2*padx
                         font=LARGE_FONT)
        label.grid(pady=10, padx=10, sticky="nsew")


def _main():
    app = PySeeApp()
    # remove the window starting location dimensions when releasing
    app.geometry("{}x{}+4000+450".format(WINDOW_WIDTH, WINDOW_HEIGHT))
    app.resizable(width=False, height=False)
    app.mainloop()

if __name__ == '__main__':
    _main()
