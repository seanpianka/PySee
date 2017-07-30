#
# Instant Python
# $Id$
#
# menu construction kit
#
# the Menubar class creates a menubar in the "best" way on the current plat-
# form.  use the addmenu method to add pulldown menus, and addcommand et al.
# to add items to a menu.
#
# summary:
#
#     class Menubar:
#         __init__(master, getstate=None, separator=0)
#         addmenu(label) => Menu (pulldown)
#
#     master -- a root window or a toplevel window
#     getstate -- a callback is called whenever a menu is displayed.
#              it should return a list of state tokens.  the resulting
#              list is used to enable/disable the corresponding items.
#     separator -- if true, a line is drawn below the menu on platforms
#              where this is appropriate
#
#     class Menu: # create via factory
#         addcheckbutton(label, variable, state=None, **options)
#         addcommand(label, command, state=None, **options)
#         addradiobutton(label, variable, value, state=None, **options)
#         addseparator()
#         addmenu(label) => Menu (foldout)
#
#     label can use & to mark which character to underline
#     state is either None or a token (as returned by getstate)
#
# for more information, see chapter 2 and the appendix.
#
# written by Fredrik Lundh, 1996-97.
#

import Tkinter
from Tkinter import *

import string

# FIXME: at the moment, we only enable native menus on PC platforms
import sys
use_native_menus = sys.platform == "win32" and TkVersion >= 8.0

class Menu:
    "Tkinter menu wrapper (use with foldout or popup menus)"

    def __init__(self, master, getstate):
        self.menu = Tkinter.Menu(master, tearoff=0, postcommand=self.update)
        self.getstate = getstate
        self.state = []
        self.index = 0

    def _fixlabel(self, label, options, labelid="label"):
        try:
            i = string.index(label, "&")
            options[labelid] = label[:i] + label[i+1:]
            options["underline"] = i
        except ValueError:
            options[labelid] = label

    def addseparator(self):
        "Add a separator item"

        self.menu.add(SEPARATOR)
        self.index = self.index + 1

    def addcommand(self, label, command = None, state = None, **options):
        "Add a command"

        self._fixlabel(label, options)
        if command: options["command"] = command
        else:       options["state"] = state = DISABLED
        apply(self.menu.add, (COMMAND,), options)

        self.state.append((self.index, state))
        self.index = self.index + 1

    def addradiobutton(self, label, variable, value, state = None, **options):
        "Add a radiobutton"

        self._fixlabel(label, options)
        options["variable"] = variable
        options["value"] = value
        apply(self.menu.add, (RADIOBUTTON,), options)

        self.state.append((self.index, state))
        self.index = self.index + 1

    def addcheckbutton(self, label, variable, state = None, **options):
        "Add a checkbutton"

        self._fixlabel(label, options)
        options["variable"] = variable
        apply(self.menu.add, (CHECKBUTTON,), options)

        self.state.append((self.index, state))
        self.index = self.index + 1

    def _installmenu(self, label, menu):
        # used by PulldownMenu.addmenu

        options = {"menu": menu}
        self._fixlabel(label, options)
        apply(self.menu.add, (CASCADE,), options)
        self.index = self.index + 1

    def update(self):
        if callable(self.getstate):
            e = self.getstate()
        else:
            e = []
        for i, s in self.state:
            if not s or s in e:
                self.menu.entryconfig(i, state=NORMAL)
            else:
                self.menu.entryconfig(i, state=DISABLED)

    def addmenu(self, label):
        "Add (another) fold-out menu to this menu"

        menu = Menu(self.menu, self.getstate)
        self._installmenu(label, menu.menu)
        return menu


class PulldownMenu(Menu):
    "Pulldown menu (used with menubars)"

    def __init__(self, master, label, getstate):

        if use_native_menus:

            Menu.__init__(self, master, getstate)

            options = {"menu": self.menu}
            self._fixlabel(label, options)
            apply(master.add_cascade, (), options)

        else:

            options = {}
            self._fixlabel(label, options, "text")
            self.button = apply(Menubutton, (master,), options)
            self.button.pack(side=LEFT, padx="1m")
            Menu.__init__(self, self.button, getstate)
            self.button.config(menu=self.menu)

        self.getstate = getstate

    def addmenu(self, label):
        "Add a fold-out menu to this menu"

        menu = Menu(self.menu, self.getstate)
        self._installmenu(label, menu.menu)
        return menu


class Menubar:
    "Menubar class"

    def __init__(self, master, getstate=None, separator=0):

        if use_native_menus:

            # Tk 8.0
            self.menubar = Tkinter.Menu(master)
            try:
                master.config(menu=self.menubar)
            except AttributeError:
                # master is a toplevel window (Tkinter 1.63)
                master.tk.call(master, "config", "-menu", self.menubar)

            if separator and sys.platform == "win32":
                # add a separator line
                Frame(master, bd=2, relief=SUNKEN, height=2).pack(fill=X)

        else:

            # Tk 4.2 and older
            self.menubar = Frame(master, bd=2, relief=RAISED)
            self.menubar.pack(side=TOP, fill=X)

        self.getstate = getstate

    def addmenu(self, label):
        "Add a pull-down menu to this menubar"

        return PulldownMenu(self.menubar, label, self.getstate)


# --------------------------------------------------------------------
# test stuff

if __name__ == "__main__":

    def hello():
        print "Hello!"

    root = Tk()

    menubar = Menubar(root, separator=1)

    menu = menubar.addmenu("&File")

    menu.addcommand("&Hello", hello)

    menu.addseparator()
    v = IntVar()
    menu.addradiobutton("&A", v, "a")
    menu.addradiobutton("&B", v, "b")
    menu.addradiobutton("&C", v, "c")

    menu.addseparator()
    v = IntVar()
    menu.addcheckbutton("&D", v)

    menu.addseparator()
    submenu = menu.addmenu("&Submenu")
    submenu.addcommand("S&pam")
    submenu.addcommand("E&gg")

    anothersubmenu = submenu.addmenu("An&other")
    anothersubmenu.addcommand("Golden &egg", background="gold")

    menu.addseparator()
    menu.addcommand("&Goodbye", command=root.destroy)

    Frame(root, height=100, width=100).pack()

    root.mainloop()
