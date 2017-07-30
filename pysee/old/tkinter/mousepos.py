import tkinter as tk
root = tk.Tk()

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

root.bind('<Motion>', motion)
x = root.winfo_pointerx()
y = root.winfo_pointery()
root.mainloop()
