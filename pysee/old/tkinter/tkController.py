# File: tkController.py

import Tkinter

PREFIX = "tkController"

class Controller:

    def __init__(self, master=None):
        if master is None:
            master = Tkinter._default_root
        assert master is not None
        self.tag = PREFIX + str(id(self))
        def bind(event, handler):
            master.bind_class(self.tag, event, handler)
        self.create(bind)

    def install(self, widget):
        widgetclass = widget.winfo_class()
        # remove widget class bindings and other controllers
        tags = [self.tag]
        for tag in widget.bindtags():
            if tag != widgetclass and tag[:len(PREFIX)] != PREFIX:
                tags.append(tag)
        widget.bindtags(tuple(tags))

    def create(self, handle):
        # the default implementation looks for decorated methods
        for key in dir(self):
            method = getattr(self, key)
            if hasattr(method, "tkevent") and callable(method):
                handle(method.tkevent, method)

##
# Simple event decorator for Python 2.4 and later.

def bind(event):
    def decorator(func):
        func.tkevent = event
        return func
    return decorator
