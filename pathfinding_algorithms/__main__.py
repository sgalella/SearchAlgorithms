import tkinter as tk

from .menu_window import MenuWindow


root = tk.Tk()
p = tk.PhotoImage(file="images/icon.png")
root.iconphoto(False, p)
MenuWindow(root).pack()
root.mainloop()
