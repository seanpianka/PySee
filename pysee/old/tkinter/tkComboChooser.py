#
# Instant Python
# $Id$
#
# simple combobox chooser
#
# written by Fredrik Lundh, June 1997
#

from Tkinter import *

import os, string

ARROW = """
#define im_width 10
#define im_height 10
static char im_bits[] = {
0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0x00,0x7c,0x00,0x38,0x00,0x10,0x00,0x00,
0x00,0x00,0x00,0x00,0x00
};
"""

##
# Creates a combobox chooser widget.
#
# @def __init__(master, data, **options)
# @param master Parent widget.
# @param data A sequence containing (text, data, ...) tuples.  By default,
#     the first item in each tuple is displayed; the rest of the tuple can
#     contain one or more associated values.  You can override the
#     {@link render_item} method to change this.
# @keyparam current Index of initial selection, if any.
# @keyparam command Callback.  If given, this should be a callable object
#     taking an index and a data item.  It is called whenever the selection
#     is changed by the user.
# @keyparam width Width of text field, in character units.

class Chooser(Frame):

    def __init__(self, master, data, current=None,
        command=None, width=20,
        Listbox=Listbox, **kw):

        Frame.__init__(self, master, bd=2, relief=SUNKEN)

        global ARROW

        if type(ARROW) == type(""):
            ARROW = BitmapImage(data=ARROW)

        self.button = Button(self, image=ARROW, command=self._listdisplay)
        self.button.pack(side=RIGHT, fill=BOTH)

        self.entry = Entry(self, bd=0, width=width)
        self.entry.pack(side=LEFT, expand=1, fill=X)

        self.command = command
        self.data = data

        self.setitem(current)

        # create and hide list window
        self.top = Toplevel(bg="black", bd=1)
        self.top.overrideredirect(1)
        self.top.withdraw()

        self.list = Listbox(self.top, bd=0, bg="white")
        self.list.bind("<Any-ButtonRelease>", self._listremove)
        self.list.pack(fill=BOTH)

        self.setdata(data)

    def _listdisplay(self, event = None):

        # calculate list position and size
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()
        w, h = self.winfo_width(), self.top.winfo_reqheight()

        if os.name == "nt":
            # Geometry doesn't work on iconified windows in Tk 8.0b2
            # for Windows.  Sun will fix this for 8.0 final.
            self.top.deiconify()

        self.top.lift()
        self.top.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.top.deiconify()

        self.list.grab_set()

    def _listremove(self, event = None):

        self.list.grab_release()

        self.top.withdraw()

        sel, item = self.getselection()
        if sel is not None:
            # update entry widget
            self.entry.config(state=NORMAL)
            self.entry.delete(0, END)
            self.entry.insert(END, item[0])
            self.entry.config(state=DISABLED)
            self.current = sel
            if callable(self.command):
                self.command(sel, item)

    ##
    # Loads the widget with data from a sequence.
    #
    # @param data A sequence containing (text, data, ...) tuples.  The first
    #     item in each tuple is displayed; the rest of the tuple can contain
    #     one or more associated values.

    def setdata(self, data):

        self.list.delete(0, END)
        index = 0
        for item in data:
            self.list.insert(END, self.render_item(index, item))
            index = index + 1
        self.list.config(height=len(data))
        self.data = data

    ##
    # (Hook) Renders a sequence item.

    def render_item(self, index, item):
        return item[0]

    ##
    # Gets the current selection from the internal list widget.  To get the
    # selected chooser value, use {@link getitem} instead.
    #
    # @return A 2-tuple containing the selected index, and the corresponding
    #     item from the data sequence.

    def getselection(self):

        sel = self.list.curselection()
        try:
            sel = map(int, sel) # Tkinter 1.63
        except ValueError: pass
        if sel:
            return sel[0], self.data[sel[0]]
        return None, None

    #
    # chooser interface

    ##
    # Gets a reference to the data sequence.

    def getdata(self):
        return self.data

    ##
    # Gets the currently selected item.
    ##
    # @return A 2-tuple containing the selected index, and the corresponding
    #     item from the data sequence.  Both items are set to None if nothing
    #     was selected.

    def getitem(self):
        if self.current is not None:
            return self.current, self.data[self.current]
        return None, None

    ##
    # Sets the current selection.
    #
    # @param index The data sequence index for the new selection.

    def setitem(self, index):
        self.entry.config(state=NORMAL)
        self.entry.delete(0, END)
        if index is not None:
            self.entry.insert(END, self.render_item(index, self.data[index]))
        self.current = index
        self.entry.config(state=DISABLED)


# --------------------------------------------------------------------
# test stuff

if __name__ == "__main__":

    root = Tk()

    root.title("tkComboChooser")

    data = [
        ("Spam", "A", "#e07070"),
        ("Egg", "B", "#60c060"),
        ("Bacon", "C", "#8080ff"),
        ]

    def hook(ix, value):
        print ix, value
        box.button.config(bg=value[2])

    box = Chooser(root, data=data, current=0, command=hook)
    box.pack(fill=X)

    box1 = Chooser(root, data=data, current=0)
    box1.pack(fill=X)

    box2 = Chooser(root, data=data, current=0)
    box2.pack(fill=X)

    mainloop()
