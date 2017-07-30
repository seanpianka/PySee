import Tkinter
import tkFont

##
# A Listbox that has an additional {@link autowidth} method.

class Listbox(Tkinter.Listbox):

    ##
    # Sets the size this widget so that all text is visible.
    #
    # @param maxwidth Maximum width, in character units.

    def autowidth(self, maxwidth=100):
        autowidth(self, maxwidth)

##
# Sets the size of a Listbox widget so that all text is visible.
#
# @param list Listbox widget.
# @param maxwidth Maximum width, in character units.

def autowidth(list, maxwidth=100):
    font = tkFont.Font(font=list.cget("font"))
    pixels = 0
    for item in list.get(0, "end"):
        pixels = max(pixels, font.measure(item))
    # bump listbox size until all entries fit
    pixels = pixels + 10
    width = int(list.cget("width"))
    for w in range(0, maxwidth+1, 5):
        if list.winfo_reqwidth() >= pixels:
            break
        list.config(width=width+w)

if __name__ == "__main__":

    w = Listbox()
    w.pack()

    for i in range(1, 50):
        w.insert("end", "*"*i)

    w.autowidth()

    w.mainloop()
