import tkinter as tk
import tkinter.font as tkFont
""" import win32api 
def check_caps_lock_status():
   return win32api.GetKeyState(0x14) & 1 == 1 """
def LacunaWrapText(text, mainFont, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    space_width = mainFont.measure(" ")

    for word in words:
        word_width = mainFont.measure(word)
        if current_width + word_width + (space_width if current_line else 0) <= max_width:
            current_line.append(word)
            current_width += word_width + (space_width if current_line else 0)
        else:
            lines.append(current_line)
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(current_line)

    return lines

def LacunaCheckInput(entry_var, correct_word="would"):
    text = entry_var.get()
    print("Entered text:", text)
    
    for i, char in enumerate(text):
        if i >= len(correct_word) or char != correct_word[i]:
            entry_var.widget.config(fg="red")
            print("Color: red")
            return
    entry_var.widget.config(fg="#00ff00")
    print("Color: green")

def LacunaOnModified(entry_var, correct_word="would"):
    LacunaCheckInput(entry_var, correct_word)

def LacunaCreateTextWidges(root, text, mainFont, max_width):
    global entry
    lines = LacunaWrapText(text, mainFont, max_width)
    entry_widgets = []  # Store entry widgets

    # Calculate the total width of the longest line
    max_line_width = max(sum(mainFont.measure(word) for word in line) + (len(line) - 1) * mainFont.measure(" ") for line in lines)
    
    # Calculate the starting x position to center the text block horizontally
    x_offset = (root.winfo_width() - max_line_width) // 2

    y_pos = 0
    for line in lines:
        x_pos = x_offset
        for word in line:
            if word == "would":
                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)

                # Create the Entry widget on top of the Label widget
                #entry_var = tk.StringVar()
                entry = tk.Entry(root, textvariable=entry_var, bg="white", font=mainFont, borderwidth=0, fg="black", insertbackground="white")

                #entry = tk.Entry(root, textvariable=entry_var, bg="white", font=mainFont, borderwidth=0, fg="black")
                entry.place(x=x_pos, y=y_pos, width=label.winfo_reqwidth())
                entry_var.widget = entry  # Add a reference to the entry widget in the StringVar
                entry_widgets.append(entry)
                entry.focus_set()

                # Bind the StringVar to trigger LacunaOnModified when the value changes
                entry_var.trace_add("write", lambda name, index, mode, sv=entry_var: LacunaOnModified(sv, correct_word="would"))
            else:
                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)
            x_pos += mainFont.measure(word) + mainFont.measure(" ")
        y_pos += mainFont.metrics("linespace")

    # Lift entry widgets to the top
    for entry in entry_widgets:
        entry.lift()
    return x_offset, y_pos
def ButtonsAddChar(char):
    if shift_pressed:
        if char == "ß":
            char = "ẞ" #instead of ss
        else:
            char = char.upper()
    print(f"Chartobeaddedtest:\t{char}")
    # Get the current content of the entry
    current_text = entry_var.get()
    # Append the new character
    new_text = current_text + char
    # Update the entry with the new text
    entry_var.set(new_text)
    entry.icursor(tk.END)
def ButtonsInitChar(root, windowWidth, charList, yPos):
    mainFont = tkFont.Font(family="Arial", size=25)
    xStart = 0
    buttons = []
    if len(charList) % 2 == 1:
        xStart = windowWidth / 2 - (((len(charList) - 1) * 45) - 5) / 2 #odd
    else:
        xStart = windowWidth / 2 - (len(charList) * 45) / 2 #even
    for i, char in enumerate(charList):
        charButton = tk.Button(root, text=char, font=mainFont, command=lambda char2=char: ButtonsAddChar(char2))# need to set it to char2, since otherwise tk.Button will just set it to the last letter of char2
        x = xStart + 45 * (i - 1)
        charButton.place(x=x, y=yPos, width=40, height=40)
        buttons.append(charButton)

    return buttons

def ButtonsChangeText():
    for button in buttons:
        if shift_pressed:# is not check_caps_lock_status(): #just if shift_pressed in non-windows version
            #check if text of char is ß (sharp-s), since before 2017
            #the upper case of ß was SS. SS is still allowed, but I changed it to ẞ for style and functionality.
            if button["text"] == "ß":
                button.config(text="ẞ")
            else:
                button.config(text=button["text"].upper())
        else:
            button.config(text=button["text"].lower())
# Define the function to detect Shift key press
def LacunaOnShiftPress(event):
    global shift_pressed
    shift_pressed = True
    ButtonsChangeText()

# Define the function to detect Shift key release
def LacunaOnShiftRelease(event):
    global shift_pressed
    shift_pressed = False
    ButtonsChangeText()

def LacunaStartGui():
    global buttons
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Button):
            widget.destroy()
    mainFont = tkFont.Font(family="Arial", size=20)
    minFont = tkFont.Font(family="Arial", size=15)
    text = "This would be an example sentence that I wrote to show how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you."
    max_width = root.winfo_width() / 2  # Maximum width for the container
    x_offset, y_pos = LacunaCreateTextWidges(root, text, mainFont, max_width)
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    underLabel = tk.Label(root, text="This would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining text", font=minFont, wraplength=max_width, justify='left', anchor='nw')
    underLabel.place(x=x_offset, y=y_pos+5)#20 + 45 for buttons
    root.update_idletasks()  # Ensure all pending events are processed
    #underLabel = underLabel.winfo_height()  # Get the height of the label
    buttons = ButtonsInitChar(root, root.winfo_width(), "wouldæœùîфю", y_pos+5+underLabel.winfo_height())
    root.update_idletasks() #potentially not needed
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    
    root.update_idletasks()

    

# Create the main window
root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# Set the geometry of the root window to match the screen size
root.geometry(f"{screen_width}x{screen_height}")
root.update_idletasks()
entry_var = tk.StringVar()
LacunaStartGui()
root.update_idletasks()

# Initialize the shift_pressed variable
shift_pressed = False


# Track previous dimensions
previous_width = root.winfo_width()
previous_height = root.winfo_height()

def LacunaOnConfigure(event):
    global previous_width, previous_height
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if current_width != previous_width or current_height != previous_height:
        previous_width = current_width
        previous_height = current_height
        LacunaDebouncedStartGui()

# Debounce mechanism
def LacunaDebounce(func, delay):
    def LacunaDebouncedFunc(*args, **kwargs):
        if hasattr(LacunaDebouncedFunc, 'after_id'):
            root.after_cancel(LacunaDebouncedFunc.after_id)
        LacunaDebouncedFunc.after_id = root.after(delay, lambda: func(*args, **kwargs))
    return LacunaDebouncedFunc

LacunaDebouncedStartGui = LacunaDebounce(LacunaStartGui, 200)  # 200 milliseconds delay

root.bind('<Configure>', LacunaOnConfigure)
root.bind('<Shift_L>', LacunaOnShiftPress)
root.bind('<KeyRelease-Shift_L>', LacunaOnShiftRelease)
root.bind('<Shift_R>', LacunaOnShiftPress)
root.bind('<KeyRelease-Shift_R>', LacunaOnShiftRelease)
root.mainloop()
