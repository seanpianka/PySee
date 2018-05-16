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
from tkinter import ttk
from collections import OrderedDict
import webbrowser

import keyboard

from pysee import DEFAULTS, ImageHost, CaptureTool, PySee


LARGE_FONT = ("Helvetica", 24)
MEDIUM_FONT = ("Helvetica", 16)
SMALL_FONT = ("Helvetica", 12)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
TITLE_PADDING = (50, 0)
DEFAULT_BG = "#121212"
DEFAULT_FG = "#F7F7F7"
ABOUT_MSG = "PySee is a open-source screenshot sharing tool for Linux and macOS written in Python.\n\nWritten with love by Sean Pianka (github.com/seanpianka)."


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("PySee Pop-Up Message")

    container = tk.Frame(popup, bg=DEFAULT_BG)
    label = ttk.Label(container, background=DEFAULT_BG, foreground=DEFAULT_FG, text=msg, font=MEDIUM_FONT).pack(side="top", fill="both", pady=20, padx=35, expand=True)
    ttk.Button(container, text="Close", command=popup.destroy).pack(side="bottom", pady=(0, 15))
    container.pack(fill="both", expand=True)

    popup.mainloop()


class PySeeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.bmp") # icon for window
        tk.Tk.wm_title(self, "PySee")

        try:
            self.pysee = PySee()
        except configparser.ParserError as e:
            popupmsg(str(e))
            raise

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) # minimum size, priority

        menubar = tk.Menu(container)

        values = {
                "host_name": DEFAULTS['HOST'],
                "tool_name": DEFAULTS['TOOL'],
                "clipboard": DEFAULTS['CLIPBOARD'],
                "upload": DEFAULTS['UPLOAD'],
                "logging": DEFAULTS['LOGGING'],
                "save": DEFAULTS['SAVE'],
                "save_dir": DEFAULTS['SAVE_DIR']
        }

        capturemenu = tk.Menu(menubar, tearoff=1)
        capturemenu.add_command(label="Fullscreen", command=lambda: self.capture("full", *(values.values)))
        capturemenu.add_command(label="Region", command=lambda: self.capture("region", *(values.values())))
        capturemenu.add_command(label="Window", command=lambda: self.capture("window", *(values.values())))
        menubar.add_cascade(label="Capture", menu=capturemenu)

        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Capture Settings",
            command=lambda: self.show_frame(SettingsPage))
        settingsmenu.add_command(label="Configuration File",
            command=lambda: self.show_frame(ConfigurationPage))
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        aboutmenu.add_command(label="About",
            command=lambda: popupmsg(ABOUT_MSG))
        aboutmenu.add_command(label="Source Code",
            command=lambda: webbrowser.open("https://github.com/seanpianka/PySee/"))
        aboutmenu.add_command(label="Buy a Coffee",
            command=lambda: webbrowser.open("https://ko-fi.com/pianka"))
        menubar.add_cascade(label="About", menu=aboutmenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = OrderedDict()
        self.MAX_ROW = 2

        for f in (CapturePage, SettingsPage, ConfigurationPage):
            frame = f(container, self)
            self.frames[f] = (frame, frame.page_title)
            frame.grid(row=0, column=0, sticky="nsew",
                       columnspan=4, rowspan=self.MAX_ROW)

        for r in range(self.MAX_ROW):
            container.rowconfigure(r, weight=1)

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
        self.show_frame(CapturePage)
        PySeeApp.center_on_screen(self)

    def capture(self, mode, image_host, capture_tool, clipboard_option, upload_option, logging_option, save_option, save_dir):
        image_url = self.pysee.main(mode=mode,
                                    host_name=image_host,
                                    tool_name=capture_tool,
                                    clipboard=clipboard_option,
                                    upload=upload_option,
                                    logging=logging_option,
                                    save=save_option,
                                    save_dir=save_dir)
        popupmsg("Clipboard copy: \"{}\" has been copied to your system clipboard.".format(image_url))


    @staticmethod
    def center_on_screen(toplevel, root=True):
        if not root:
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        else:
            size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        w = (toplevel.winfo_screenwidth() - WINDOW_WIDTH) / 2
        h = (toplevel.winfo_screenheight() - WINDOW_HEIGHT) / 2
        toplevel.geometry('%dx%d+%d+%d' % (size + (w, h)))


    def show_frame(self, controller):
        """ Displays the frame controller from self.frames at the "front" of
            the stack of frames. """
        frame = self.frames[controller][0]
        frame.tkraise()


class CapturePage(tk.Frame):
    page_title = "Capture"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(2):
            self.rowconfigure(i, weight=1)
        for i in range(1):
            self.columnconfigure(i, weight=1)

        class Column(tk.Frame):
            def __init__(self, parent, title, num_rows):
                tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 3, bg="#222222")
                for i in range(2): self.rowconfigure(i, weight=1)
                for i in range(1): self.columnconfigure(i, weight=1)

                self.placed = False

                # Title
                self.title = tk.Frame(self, width=WINDOW_WIDTH / 3, bg="#121212")
                tk.Label(self.title, bg="#121212", fg="#f7f7f7", font=MEDIUM_FONT, text=title).pack(pady=TITLE_PADDING)

                # Content
                self.content = tk.Frame(self, width=WINDOW_WIDTH / 3, bg="#222222")
                for i in range(num_rows): self.content.rowconfigure(i, weight=1)
                for i in range(1): self.content.columnconfigure(i, weight=1)

            def place(self, column):
                if not self.placed:
                    self.placed = True

                self.title.pack(side="top", fill="x")
                self.content.pack(side="left", fill="x", expand=True)
                self.grid(row=0, column=column, sticky="nsew")

        ## Top frame for 3 capture settings columns (1x3)
        self.top_frame = tk.Frame(self, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT / 3) * 2, bg="#181818")
        for i in range(1): self.top_frame.rowconfigure(i, weight=1)
        for i in range(3): self.top_frame.columnconfigure(i, weight=1)

        # Image Host, column 1
        self.col_image_host = Column(self.top_frame, "Image Host", len(ImageHost.valid_hosts))

        image_host = tk.StringVar()
        for i, (host, host_upload) in enumerate(ImageHost.valid_hosts.items()):
            ttk.Radiobutton(self.col_image_host.content, text=host, value=host, var=image_host).grid(row=i, column=0, pady=10, padx=30, sticky="ew")
        image_host.set(DEFAULTS['HOST'])

        self.col_image_host.place(0)

        # Capture Tool, column 2
        self.col_capture_tool = Column(self.top_frame, "Capture Tool", len(CaptureTool.valid_tools))

        capture_tool = tk.StringVar()
        for i, (tool, tool_capture) in enumerate(CaptureTool.valid_tools.items()):
            ttk.Radiobutton(self.col_capture_tool.content, text=tool, value=tool, var=capture_tool).grid(row=i, column=0, pady=10, padx=30, sticky="ew")
        capture_tool.set(DEFAULTS['TOOL'])

        self.col_capture_tool.place(1)

        # After Capture, column 3
        self.col_after_capture = Column(self.top_frame, "After Capture", 4)

        clipboard_option = tk.BooleanVar(None, DEFAULTS['CLIPBOARD'])
        ttk.Checkbutton(self.col_after_capture.content, text="Copy to Clipboard", var=clipboard_option).grid(row=0, column=0, pady=10, padx=30, sticky="ew")

        upload_option = tk.BooleanVar(None, DEFAULTS['UPLOAD'])
        ttk.Checkbutton(self.col_after_capture.content, text="Upload to Image Host", var=upload_option).grid(row=1, column=0, pady=10, padx=30, sticky="ew")

        logging_option = tk.BooleanVar(None, DEFAULTS['LOGGING'])
        ttk.Checkbutton(self.col_after_capture.content, text="Logging to Terminal", var=logging_option).grid(row=2, column=0, pady=10, padx=30, sticky="ew")

        save_option = tk.BooleanVar(None, DEFAULTS['SAVE'])
        ttk.Checkbutton(self.col_after_capture.content, text="Save After Capture", var=save_option).grid(row=3, column=0, pady=10, padx=30, sticky="ew")

        self.col_after_capture.place(2)


        ## Bottom frame for "mode"/action buttons
        self.bottom_frame = tk.Frame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT / 3, bg="#121212")
        for i in range(1): self.bottom_frame.rowconfigure(i, weight=1)
        for i in range(3): self.bottom_frame.columnconfigure(i, weight=1)

        ttk.Button(self.bottom_frame,
                   text="Region",
                   command=lambda: controller.capture("region",
                                                      image_host.get(),
                                                      capture_tool.get(),
                                                      clipboard_option.get(),
                                                      upload_option.get(),
                                                      logging_option.get(),
                                                      save_option.get(),
                                                      DEFAULTS["SAVE_DIR"])).grid(pady=3, row=0, column=0)

        ttk.Button(self.bottom_frame,
                   text="Full",
                   command=lambda: controller.capture("full",
                                                      image_host.get(),
                                                      capture_tool.get(),
                                                      clipboard_option.get(),
                                                      upload_option.get(),
                                                      logging_option.get(),
                                                      save_option.get(),
                                                      DEFAULTS["SAVE_DIR"])).grid(pady=3, row=0, column=1)

        ttk.Button(self.bottom_frame,
                   text="Window",
                   command=lambda: controller.capture("window",
                                                      image_host.get(),
                                                      capture_tool.get(),
                                                      clipboard_option.get(),
                                                      upload_option.get(),
                                                      logging_option.get(),
                                                      save_option.get(),
                                                      DEFAULTS["SAVE_DIR"])).grid(pady=3, row=0, column=2)
        ### END

        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")


class ConfigurationPage(tk.Frame):
    page_title = "Configuration"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(1):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        def save_changes():
            contents = settings_entry.get(0.0, "end")
            with open(DEFAULTS['CONFIG_PATH'], "w") as f:
                f.write(contents)

        with open(DEFAULTS['CONFIG_PATH'], "r") as f:
            config_contents = f.read()

        settings_entry = tk.Text(self)
        settings_entry.insert(0.0, config_contents)
        settings_entry.grid(padx=3, pady=(3, 0), row=0, column=0)


        button = ttk.Button(self,
                            text="Save Changes",
                            command=lambda: save_changes())
        button.grid(pady=3, row=1, column=0)


class SettingsPage(tk.Frame):
    page_title = "Settings"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for i in range(2):
            self.rowconfigure(i, weight=1)
        for i in range(1):
            self.columnconfigure(i, weight=1)

        class Column(tk.Frame):
            def __init__(self, parent, title, num_rows):
                tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 3, bg="#222222")
                for i in range(2): self.rowconfigure(i, weight=1)
                for i in range(1): self.columnconfigure(i, weight=1)

                self.placed = False

                # Title
                self.title = tk.Frame(self, width=WINDOW_WIDTH / 3, bg="#121212")
                tk.Label(self.title, bg="#121212", fg="#f7f7f7", font=MEDIUM_FONT, text=title).pack(pady=TITLE_PADDING)

                # Content
                self.content = tk.Frame(self, width=WINDOW_WIDTH / 3, bg="#222222")
                for i in range(num_rows): self.content.rowconfigure(i, weight=1)
                for i in range(1): self.content.columnconfigure(i, weight=1)

            def place(self, column):
                if not self.placed:
                    self.placed = True

                self.title.pack(side="top", fill="x")
                self.content.pack(side="left", fill="x", expand=True)
                self.grid(row=0, column=column, sticky="nsew")

        def save_preferences(controller, image_host, capture_tool, clipboard_option, upload_option, logging_option, save_option, save_dir_option):
            values = {'HOST': image_host,
                      'TOOL': capture_tool,
                      'CLIPBOARD': clipboard_option,
                      'UPLOAD': upload_option,
                      'LOGGING': logging_option,
                      'SAVE': save_option,
                      'SAVE_DIR': save_dir_option}
            controller.pysee.cp.update_config(values)
            controller.pysee.cp.write_config()

        ## Top frame for 3 capture settings columns (1x3)
        self.top_frame = tk.Frame(self, width=WINDOW_WIDTH, height=(WINDOW_HEIGHT / 3) * 2, bg="#181818")
        for i in range(1): self.top_frame.rowconfigure(i, weight=1)
        for i in range(3): self.top_frame.columnconfigure(i, weight=1)

        # Image Host, column 1
        self.col_image_host = Column(self.top_frame, "Image Host", len(ImageHost.valid_hosts))

        image_host = tk.StringVar()
        for i, (host, host_upload) in enumerate(ImageHost.valid_hosts.items()):
            ttk.Radiobutton(self.col_image_host.content, text=host, value=host, var=image_host).grid(row=i, column=0, pady=10, padx=30, sticky="ew")
        image_host.set(DEFAULTS['HOST'])

        self.col_image_host.place(0)

        # Capture Tool, column 2
        self.col_capture_tool = Column(self.top_frame, "Capture Tool", len(CaptureTool.valid_tools))

        capture_tool = tk.StringVar()
        for i, (tool, tool_capture) in enumerate(CaptureTool.valid_tools.items()):
            ttk.Radiobutton(self.col_capture_tool.content, text=tool, value=tool, var=capture_tool).grid(row=i, column=0, pady=10, padx=30, sticky="ew")
        capture_tool.set(DEFAULTS['TOOL'])

        self.col_capture_tool.place(1)

        # After Capture, column 3
        self.col_after_capture = Column(self.top_frame, "After Capture", 5)

        clipboard_option = tk.BooleanVar(None, DEFAULTS['CLIPBOARD'])
        ttk.Checkbutton(self.col_after_capture.content, text="Copy to Clipboard", var=clipboard_option).grid(row=0, column=0, pady=10, padx=30, sticky="ew")

        upload_option = tk.BooleanVar(None, DEFAULTS['UPLOAD'])
        ttk.Checkbutton(self.col_after_capture.content, text="Upload to Image Host", var=upload_option).grid(row=1, column=0, pady=10, padx=30, sticky="ew")

        logging_option = tk.BooleanVar(None, DEFAULTS['LOGGING'])
        ttk.Checkbutton(self.col_after_capture.content, text="Logging to Terminal", var=logging_option).grid(row=2, column=0, pady=10, padx=30, sticky="ew")

        save_option = tk.BooleanVar(None, DEFAULTS['SAVE'])
        ttk.Checkbutton(self.col_after_capture.content, text="Save After Capture", var=save_option).grid(row=3, column=0, pady=10, padx=30, sticky="ew")

        save_dir_entry = ttk.Entry(self.col_after_capture.content)
        save_dir_entry.insert(0, DEFAULTS['SAVE_DIR'])
        save_dir_entry.grid(row=4, column=0, pady=10, padx=30, sticky="ew")

        self.col_after_capture.place(2)


        ## Bottom frame for "mode"/action buttons
        self.bottom_frame = tk.Frame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT / 3, bg="#121212")
        for i in range(1): self.bottom_frame.rowconfigure(i, weight=1)
        for i in range(1): self.bottom_frame.columnconfigure(i, weight=1)

        button = ttk.Button(self.bottom_frame,
                            text="Save Preferences",
                            command=lambda: save_preferences(controller,
                                                             image_host.get(),
                                                             capture_tool.get(),
                                                             clipboard_option.get(),
                                                             upload_option.get(),
                                                             logging_option.get(),
                                                             save_option.get(),
                                                             save_dir_entry.get())).grid(pady=3, row=0, column=0)
        ### END

        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")


def main():
    app = PySeeApp()
    app.resizable(width=False, height=False)

    hotkey_values = [DEFAULTS['HOST'], DEFAULTS['TOOL'], DEFAULTS['CLIPBOARD'], DEFAULTS['UPLOAD'], DEFAULTS['LOGGING'], DEFAULTS['SAVE'], DEFAULTS['SAVE_DIR']]

    try:
        keyboard.add_hotkey("ctrl+shift+2", lambda: app.capture(mode="full", *hotkey_values))
        keyboard.add_hotkey("ctrl+shift+3", lambda: app.capture(mode="window", *hotkey_values))
        keyboard.add_hotkey("ctrl+shift+4", lambda: app.capture(mode="region", *hotkey_values))
    except ImportError:
        app.bind("<Control-Shift-2>", lambda: app.capture(mode="full", *hotkey_values))
        app.bind("<Control-Shift-3>", lambda: app.capture(mode="window", *hotkey_values))
        app.bind("<Control-Shift-4>", lambda: app.capture(mode="region", *hotkey_values))
        print("GUI not started as root, unable to listen globally for capture hotkeys...")

    app.mainloop()

if __name__ == '__main__':
    main()
