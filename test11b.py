import tkinter as tk

def create_invisible_entry(event=None):
    pass

def get_coordinates(event=None):
    # Calculate coordinates of all four corners of the label box
    x = outLangText1.winfo_x()
    y = outLangText1.winfo_y()
    width = outLangText1.winfo_width()
    height = outLangText1.winfo_height()

    # Coordinates of all four corners
    top_left = (x, y)
    top_right = (x + width, y)
    bottom_left = (x, y + height)
    bottom_right = (x + width, y + height)

    print("Top Left:", top_left)
    print("Top Right:", top_right)
    print("Bottom Left:", bottom_left)
    print("Bottom Right:", bottom_right)

# Create the main window
root = tk.Tk()

# Additional label above the entry widget
outLangText1 = tk.Text(root, wrap=tk.WORD, font=("Arial", 14), height=2, width=50)
text = "This would be the outLangText1 label. This label will wrap around when it reaches the end of the line."
outLangText1.insert(tk.END, text)

# Find the index of the word "label" and change its background color
start_index = text.find("label")
end_index = start_index + len("label")
outLangText1.tag_add("background_color", f"1.{start_index}", f"1.{end_index}")
outLangText1.tag_config("background_color", background="red")

outLangText1.pack()

# Bind the <Map> event to the get_coordinates function
outLangText1.bind("<Map>", get_coordinates)

root.mainloop()
