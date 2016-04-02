import tkinter as tk
import sys

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=1,
                             command=quit, accelerator="Ctrl+Q")
        self.config(menu=menubar)

        self.bind_all("<Control-q>", self.quit)


    def quit(self, event):
        print("quitting...")
        sys.exit(0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
