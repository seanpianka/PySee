# $Id$
#
# a fancier listbox widget.  this version supports scrolling, and also
# tracks associated data via separate list.
#
# Copyright (c) 2006-2008 by Secret Labs AB.  All rights reserved.

from Tkinter import *

##
# Enhanced scrolled listbox widget.  Use {@link List.setdata} to add
# data, {@link List.getselection} to fetch selected items.

class List(Frame):

    def __init__(self, master, **options):

        # used to map list item index to associated value
        self.data = []

        Frame.__init__(self, master, bd=2, relief=SUNKEN)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        options["bd"] = 0
        options["bg"] = "white"
        options["yscrollcommand"] = scrollbar.set
        self.listbox = apply(Listbox, (self,), options)
        self.listbox.pack(fill=BOTH, expand=1)

        scrollbar.config(command=self.listbox.yview)

    ##
    # Sets the listbox data.
    #
    # @param data A sequence of list items.
    # @param render An optional renderer.  If given, the items in the
    #     sequence will be passed to this function, and the result is
    #     displayed in the listbox.  If omitted, the items are used as
    #     is.

    def setdata(self, data, render=None):
        selection = map(self.listbox.get, self.curselection())
        self.listbox.delete(0, END)
        self.data[:] = data
        for index, item in enumerate(data):
            if render:
                value = render(item)
            else:
                value = item
            self.listbox.insert(END, value)
            if value in selection:
                self.listbox.select_set(index)

    ##
    # Gets the current listbox data.
    #
    # @return A list of data items.

    def getdata(self):
        return self.data

    ##
    # Gets the current selection, as a list of items.
    # <p>
    # To get a list of indices instead, use <b>curselection</b>.
    #
    # @return A list of selected data items.

    def getselection(self):
        # get current selection
        selection = []
        for item in self.curselection():
            selection.append(self.data[item])
        return selection

    def insert(self, start, *items):
        # prevent direct calls to insert
        raise NotImplementedError("Use setdata method instead")

    def delete(self, start, end=None):
        if end is None:
            end = start
        del self.data[int(start):int(end)+1]
        self.listbox.delete(start, end)

    def curselection(self):
        # convenience: get current selection as list of integer indexes
        return map(int, self.listbox.curselection())

    def size(self):
        # override Grid manager version of this method
        return self.listbox.size()

    def __getattr__(self, attr):
        # delegate other widget operations to listbox widget
        if attr[:2] != "__":
            return getattr(self.listbox, attr)
        raise AttributeError(attr)

if __name__ == "__main__":

    import string

    root = Tk()
    root.title("tkList")

    w = List(root)
    w.pack()

    def get():
        print w.getdata()
    def set():
        w.setdata(["line 1", "line 2", "line 3"], string.upper)
    def sel():
        print w.getselection()

    Button(root, text="get", command=get).pack()
    Button(root, text="set", command=set).pack()
    Button(root, text="del", command=lambda w=w: w.delete(0)).pack()
    Button(root, text="sel", command=sel).pack()

    mainloop()
