import tkinter as tk
import tkinter.font as tkFont

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    space_width = font.measure(" ")

    for word in words:
        word_width = font.measure(word)
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

def create_widgets_for_text(root, text, font, max_width):
    lines = wrap_text(text, font, max_width)
    entry_widgets = []  # Store entry widgets

    # Calculate the total width of the longest line
    max_line_width = max(sum(font.measure(word) for word in line) + (len(line) - 1) * font.measure(" ") for line in lines)
    
    # Calculate the starting x position to center the text block horizontally
    x_offset = (root.winfo_screenwidth() - max_line_width) // 2

    y_pos = 0
    for line in lines:
        x_pos = x_offset
        for word in line:
            if word == "would":
                label = tk.Label(root, text=word, font=font, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)

                # Create the Entry widget on top of the Label widget
                entry = tk.Entry(root, bg="white", font=font, borderwidth=0)
                entry.place(x=x_pos, y=y_pos, width=label.winfo_reqwidth())
                entry_widgets.append(entry)
            else:
                label = tk.Label(root, text=word, font=font, bg=root.cget('bg'), borderwidth=0)
                label.place(x=x_pos, y=y_pos)
            x_pos += font.measure(word) + font.measure(" ")
        y_pos += font.metrics("linespace")

    # Lift entry widgets to the top
    for entry in entry_widgets:
        entry.lift()

# Create the main window
root = tk.Tk()

# Set the font
font = tkFont.Font(family="Arial", size=20)

# Text to be displayed
text = "This would be an example sentence that I wrote to would how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you would."

# Calculate wrapped text and create widgets
max_width = 400  # Maximum width for the container
create_widgets_for_text(root, text, font, max_width)

# Center the window on the screen
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

root.mainloop()
