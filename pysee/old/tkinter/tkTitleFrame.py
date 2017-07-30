# Instant Python: TitleFrame (Fredrik Lundh, June 1997)

from Tkinter import *

class TitleFrame(Frame):

    def __init__(self, master, label):

        Frame.__init__(self, master)

        frame = Frame(self, relief=GROOVE, bd=2)

        w = Label(self, text=label)
        h = w.winfo_reqheight() / 2

        w.place(x=h+h-2)

        self.inner = Frame(frame)
        self.inner.pack(padx=h, pady=h, expand=1, fill=BOTH)

        frame.pack(padx=h, pady=h, expand=1, fill=BOTH)

    def getinner(self):

        return self.inner

if __name__ == '__main__':

    root = Tk()
    root.title("PySee")

    w = TitleFrame(root, "PySee - PySee")
    w.pack(expand=1, fill=BOTH)

    frame = w.getinner()

    Button(frame, text="Capture").pack(fill=X)
    Button(frame, text="Edit").pack(fill=X)
    Button(frame, text="Select").pack(fill=X)

    root.mainloop()
