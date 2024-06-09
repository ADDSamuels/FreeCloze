import tkinter as tk

def on_enter(event=None):
    print("Enter key pressed")
    print(f"Input text: {entry.get()}")

# Create the main window
root = tk.Tk()
root.title("Enter Key Example")

# Create an Entry widget
entry = tk.Entry(root)
entry.pack(padx=20, pady=20)

# Bind the Enter key (Return) event to the Entry widget
entry.bind('<Return>', on_enter)

# Start the main event loop
root.mainloop()
