import tkinter as tk
from tkinter import font

def get_last_letter_position():
    # Get the width and height of the label widget
    label_width = label.winfo_width()
    label_height = label.winfo_height()

    # Get the font metrics
    font_metrics = font.Font(font=label.cget("font")).metrics('linespace')

    # Calculate the position of the last character
    last_char_index = len(text) - 1
    last_char_line = text.rfind('\n') + 2  # Index of the first character of the last line
    space_width = font.Font(font=label.cget("font")).measure(' ') if ' ' in text else font.Font(font=label.cget("font")).measure('a')  # Measure the width of a space or a character
    last_char_x = (last_char_index - last_char_line) * space_width  # Measure the width of a space character
    last_char_y = label_height - font_metrics - 5  # Adjust this value as needed

    # Calculate the position of the smiley
    smile_x = last_char_x
    smile_y = last_char_y - 5  # Adjust this value as needed

    print(f"Position of the last letter: ({last_char_x}, {last_char_y})")
    print(f"Position of the smiley: ({smile_x}, {smile_y})")

    # Create a label with the character "☺" and place it on the last character
    smile_label = tk.Label(root, text="☺")
    smile_label.place(x=smile_x, y=smile_y)

root = tk.Tk()

text = "This is a long text that wraps within a label widget in Tkinter."

label = tk.Label(root, text=text, wraplength=200, justify='left')
label.pack()

# Update the GUI to ensure proper rendering
root.update_idletasks()

# Maximize the window
root.state('zoomed')

# Delay getting the position until after window is drawn
root.after(100, get_last_letter_position)

root.mainloop()
