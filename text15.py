import tkinter as tk
import tkinter.font as tkFont
import time

def wrapText(text, mainFont, max_width):
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

def check_input(entry_var, correct_word="would"):
    text = entry_var.get()
    print("Entered text:", text)
    
    for i, char in enumerate(text):
        if i >= len(correct_word) or char != correct_word[i]:
            entry_var.widget.config(fg="red")
            print("Color: red")
            return
    entry_var.widget.config(fg="#00ff00")
    print("Color: green")

def on_modified(entry_var, correct_word="would"):
    check_input(entry_var, correct_word)

def create_widgets_for_text(root, text, mainFont, max_width):
    lines = wrapText(text, mainFont, max_width)
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
                entry_var = tk.StringVar()
                entry = tk.Entry(root, textvariable=entry_var, bg="white", font=mainFont, borderwidth=0, fg="black")
                entry.place(x=x_pos, y=y_pos, width=label.winfo_reqwidth())
                entry_var.widget = entry  # Add a reference to the entry widget in the StringVar
                entry_widgets.append(entry)
                entry.focus_set()

                # Bind the StringVar to trigger on_modified when the value changes
                entry_var.trace_add("write", lambda name, index, mode, sv=entry_var: on_modified(sv, correct_word="would"))
            else:
                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)
            x_pos += mainFont.measure(word) + mainFont.measure(" ")
        y_pos += mainFont.metrics("linespace")

    # Lift entry widgets to the top
    for entry in entry_widgets:
        entry.lift()
    return x_offset, y_pos

def startLacunaGUI(event=None):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
            widget.destroy()
    mainFont = tkFont.Font(family="Arial", size=20)
    minFont = tkFont.Font(family="Arial", size=15)
    text = "This would be an example sentence that I wrote to show how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you."
    max_width = root.winfo_width() / 2  # Maximum width for the container
    x_offset, y_pos = create_widgets_for_text(root, text, mainFont, max_width)
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    underLabel = tk.Label(root, text="This would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining textThis would be the underlining text", font=minFont, wraplength=max_width, justify='left', anchor='nw')
    underLabel.place(x=x_offset, y=y_pos+20)

# Create the main window
root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# Set the geometry of the root window to match the screen size
root.geometry(f"{screen_width}x{screen_height}")
root.update_idletasks()
startLacunaGUI()

# Track previous dimensions
previous_width = root.winfo_width()
previous_height = root.winfo_height()

def on_configure(event):
    global previous_width, previous_height
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if current_width != previous_width or current_height != previous_height:
        previous_width = current_width
        previous_height = current_height
        debounced_startLacunaGUI()

# Debounce mechanism
def debounce(func, delay):
    def debounced_func(*args, **kwargs):
        if hasattr(debounced_func, 'after_id'):
            root.after_cancel(debounced_func.after_id)
        debounced_func.after_id = root.after(delay, lambda: func(*args, **kwargs))
    return debounced_func

debounced_startLacunaGUI = debounce(startLacunaGUI, 200)  # 200 milliseconds delay

root.bind('<Configure>', on_configure)
root.mainloop()
