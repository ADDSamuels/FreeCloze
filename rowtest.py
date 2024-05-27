import tkinter as tk
import tkinter.font as tkFont

def addCharButtons(root, windowWidth, charList, yPos):
    if len(charList) % 2 == 0:
        xStart=0
    else:
        xStart=0
    i = 0
    for char in charList:
        charButton = tk.Button(root, text=char)
        x = xStart + 24*i
        charButton.place(x=x, y=yPos, width=20, height=20)
        i += 1


        



root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# Set the geometry of the root window to match the screen size
root.geometry(f"{screen_width}x{screen_height}")
root.update_idletasks()
windowWidth = root.winfo_width()
addCharButtons(root, windowWidth, "abcdeféß", 100)
root.mainloop()
