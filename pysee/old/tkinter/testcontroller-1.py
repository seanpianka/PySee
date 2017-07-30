import Tkinter
from tkController import Controller, bind

class myController(Controller):

    @bind("<Button-1>")
    def click(self, event):
        self.anchor = event.x, event.y
        self.item = None

    @bind("<B1-Motion>")
    def drag(self, event):
        bbox = self.anchor + (event.x, event.y)
        if self.item is None:
            self.item = event.widget.create_rectangle(bbox, fill="red")
        else:
            event.widget.coords(self.item, *bbox)

# create widgets

canvas1 = Tkinter.Canvas(bg="white")
canvas1.pack(side="left")

canvas2 = Tkinter.Canvas(bg="black")
canvas2.pack(side="left")

canvas_controller = myController()

canvas_controller.install(canvas1)
canvas_controller.install(canvas2)

Tkinter.mainloop()
