import tkinter as tk
import tkinter.font as tkFont

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
    if hasattr(entry_var, 'widget'):
        for i, char in enumerate(text):
            if i >= len(correct_word) or char != correct_word[i]:
                entry_var.widget.config(fg="red")
                print("Color: red")
                return
        entry_var.widget.config(fg="#00ff00")
        print("Color: green")
    else:
        print("Widget does not exist!")

def LacunaOnModified(*args, entry_var, correct_word="would"):
    LacunaCheckInput(entry_var, correct_word)

def LacunaCreateTextWidgets(root, text, mainFont, max_width, entry_values=None):
    lines = LacunaWrapText(text, mainFont, max_width)
    entry_widgets = []

    max_line_width = max(sum(mainFont.measure(word) for word in line) + (len(line) - 1) * mainFont.measure(" ") for line in lines)
    x_offset = (root.winfo_width() - max_line_width) // 2

    y_pos = 0
    entry_count = 0
    for line in lines:
        x_pos = x_offset
        for word in line:
            if word == "would":
                entry_var = tk.StringVar()
                entry_var.trace_add("write", lambda name, index, mode, sv=entry_var: LacunaOnModified(name, index, mode, entry_var=sv, correct_word="would"))

                if entry_values and entry_count < len(entry_values):
                    entry_var.set(entry_values[entry_count])
                entry_count += 1

                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)

                entry = tk.Entry(root, textvariable=entry_var, bg="white", font=mainFont, borderwidth=0, fg="black", insertbackground="white")
                entry.place(x=x_pos, y=y_pos, width=label.winfo_reqwidth())
                entry_var.widget = entry
                entry_widgets.append(entry)
                entry.focus_set()

                global current_entry_var
                current_entry_var = entry_var
            else:
                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)
            x_pos += mainFont.measure(word) + mainFont.measure(" ")
        y_pos += mainFont.metrics("linespace")

    for entry in entry_widgets:
        entry.lift()
    return x_offset, y_pos

def ButtonsAddChar(char):
    global current_entry_var
    if current_entry_var is None:
        return

    if shift_pressed:
        if char == "ß":
            char = "ẞ"
        else:
            char = char.upper()
    print(f"Char to be added: {char}")
    current_text = current_entry_var.get()
    new_text = current_text + char
    current_entry_var.set(new_text)
    current_entry_var.widget.icursor(tk.END)

def ButtonsInitChar(root, windowWidth, charList, yPos):
    mainFont = tkFont.Font(family="Arial", size=25)
    buttons = []
    if len(charList) % 2 == 1:
        xStart = windowWidth / 2 - (((len(charList) - 1) * 45) - 5) / 2
    else:
        xStart = windowWidth / 2 - (len(charList) * 45) / 2
    for i, char in enumerate(charList):
        charButton = tk.Button(root, text=char, font=mainFont, command=lambda char2=char: ButtonsAddChar(char2))
        x = xStart + 45 * i
        charButton.place(x=x, y=yPos, width=40, height=40)
        buttons.append(charButton)

    return buttons

def ButtonsChangeText():
    for button in buttons:
        if shift_pressed:
            if button["text"] == "ß":
                button.config(text="ẞ")
            else:
                button.config(text=button["text"].upper())
        else:
            button.config(text=button["text"].lower())

def LacunaOnShiftPress(event):
    global shift_pressed
    shift_pressed = True
    ButtonsChangeText()

def LacunaOnShiftRelease(event):
    global shift_pressed
    shift_pressed = False
    ButtonsChangeText()

def LacunaStartGui(root, entry_values=None):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Button):
            widget.destroy()
    
    mainFont = tkFont.Font(family="Arial", size=20)
    minFont = tkFont.Font(family="Arial", size=15)
    text = "This would be an example sentence that I wrote to show how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you."
    max_width = root.winfo_width() / 2
    
    x_offset, y_pos = LacunaCreateTextWidgets(root, text, mainFont, max_width, entry_values)
    root.update_idletasks()
    
    underLabel = tk.Label(root, text="This would be the underlining text", font=minFont, wraplength=max_width, justify='left', anchor='nw')
    underLabel.place(x=x_offset, y=y_pos + 5)
    root.update_idletasks()
    
    global buttons
    buttons = ButtonsInitChar(root, root.winfo_width(), "wouldæœùîфю", y_pos + 5 + underLabel.winfo_height())
    root.update_idletasks()
    LacunaCheckInput(current_entry_var, "would")

def LacunaOnConfigure(event, root):
    global previous_width, previous_height
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if current_width != previous_width or current_height != previous_height:
        previous_width = current_width
        previous_height = current_height
        
        # Save current entry values
        entry_values = [entry.get() for entry in root.winfo_children() if isinstance(entry, tk.Entry)]
        
        LacunaDebouncedStartGui(root, entry_values)

def LacunaDebounce(func, delay):
    def LacunaDebouncedFunc(*args, **kwargs):
        if hasattr(LacunaDebouncedFunc, 'after_id'):
            root.after_cancel(LacunaDebouncedFunc.after_id)
        LacunaDebouncedFunc.after_id = root.after(delay, lambda: func(*args, **kwargs))
    return LacunaDebouncedFunc

def LacunaMain():
    global root
    global shift_pressed
    global previous_height
    global previous_width
    global current_entry_var

    root = tk.Tk()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.update_idletasks()
    
    current_entry_var = None
    LacunaStartGui(root)
    root.update_idletasks()
    
    shift_pressed = False

    previous_width = root.winfo_width()
    previous_height = root.winfo_height()

    global LacunaDebouncedStartGui
    LacunaDebouncedStartGui = LacunaDebounce(LacunaStartGui, 200)

    root.bind('<Configure>', lambda event: LacunaOnConfigure(event, root))
    root.bind('<Shift_L>', LacunaOnShiftPress)
    root.bind('<KeyRelease-Shift_L>', LacunaOnShiftRelease)
    root.bind('<Shift_R>', LacunaOnShiftPress)
    root.bind('<KeyRelease-Shift_R>', LacunaOnShiftRelease)
    root.mainloop()

LacunaMain()
