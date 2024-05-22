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
    y_pos = 0
    entry_widgets = []  # Store entry widgets

    for line in lines:
        x_pos = 0
        for word in line:
            if word == "would":
                label = tk.Label(root, text=word, font=font)
                label.place(x=x_pos, y=y_pos+3)

                # Create the Entry widget on top of the Label widget
                entry = tk.Entry(root, bg="white", font=font)
                entry.place(x=x_pos, y=y_pos+3, width=label.winfo_reqwidth())
                entry_widgets.append(entry)
            else:
                label = tk.Label(root, text=word, font=font)
                label.place(x=x_pos, y=y_pos)
            x_pos += label.winfo_reqwidth() + font.measure(" ")
        y_pos += font.metrics("linespace")

    # Lift entry widgets to the top
    for entry in entry_widgets:
        entry.lift()

# Create the main window
root = tk.Tk()

# Set the font
font = tkFont.Font(family="Arial", size=14)

# Text to be displayed
text = "This would be  an example sentence that I wrote to would how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you would."

# Calculate wrapped text and create widgets
max_width = 400  # Maximum width for the container
create_widgets_for_text(root, text, font, max_width)

root.mainloop()
