import tkinter as tk
import tkinter.font as tkFont

def buttonsAddChar(root, windowWidth, charList, yPos):
    mainFont = tkFont.Font(family="Arial", size=25)
    xStart = 0
    buttons = []
    if len(charList) % 2 == 1:
        xStart = windowWidth / 2 - (((len(charList) - 1) * 45) - 5) / 2 #odd
    else:
        xStart = windowWidth / 2 - (len(charList) * 45) / 2 #even
    for i, char in enumerate(charList):
        charButton = tk.Button(root, text=char, font=mainFont)
        x = xStart + 45 * (i - 1)
        charButton.place(x=x, y=yPos, width=40, height=40)
        buttons.append(charButton)

    return buttons

def buttonsChangeText():
    for button in buttons:
        if shift_pressed:
            #check if text of char is ß (sharp-s), since before 2017
            #the upper case of ß was SS. SS is still allowed, but I changed it to ẞ for style and functionality.
            if button["text"] == "ß":
                button.config(text="ẞ")
            else:
                button.config(text=button["text"].upper())
        else:
            button.config(text=button["text"].lower())

# Define the function to detect Shift key press
def on_shift_press(event):
    global shift_pressed
    shift_pressed = True
    buttonsChangeText()

# Define the function to detect Shift key release
def on_shift_release(event):
    global shift_pressed
    shift_pressed = False
    buttonsChangeText()

root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# Set the geometry of the root window to match the screen size
root.geometry(f"{screen_width}x{screen_height}")
root.update_idletasks()

# Add character buttons and store them in a list
buttons = buttonsAddChar(root, root.winfo_width(), "abcdeféßйяæœùč̈ëÿäðζ", 100)

# Initialize the shift_pressed variable
shift_pressed = False

# Bind Shift key press and release events to the main window
root.bind('<Shift_L>', on_shift_press)
root.bind('<KeyRelease-Shift_L>', on_shift_release)
root.bind('<Shift_R>', on_shift_press)
root.bind('<KeyRelease-Shift_R>', on_shift_release)

root.mainloop()
