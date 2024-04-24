import tkinter as tk
from tkinter import ttk

def SelectLanguage():
    selectedLanguage = languageVar.get()
    
    if selectedLanguage == "English":
        messageLabel.config(text="English language selected.")
    elif selectedLanguage == "Spanish":
        messageLabel.config(text="Spanish language selected.")
    elif selectedLanguage == "French":
        messageLabel.config(text="French language selected.")
    hideInitialInterface()

def Back():
    languageLabel.pack()
    languageCombobox.pack()
    selectButton.pack()
    messageLabel.config(text="")
    backButton.pack_forget()

def hideInitialInterface():
    languageLabel.pack_forget()
    languageCombobox.pack_forget()
    selectButton.pack_forget()
    backButton.pack()

root = tk.Tk()
root.title("")

languages = ["English", "French", "German", "Italian", "Spanish", "Portuguese", "Polish", "Russian"]
languageExpressions = [f"Learning {y} from {x}" for x in languages for y in languages if x != y]
languageLabel = ttk.Label(root, text="Select Language:", font=("Arial", 14))
languageVar = tk.StringVar()
width_chars = int(root.winfo_screenwidth() * 0.25 / 10)  # Assuming average character width is 10 pixels
languageCombobox = ttk.Combobox(root, width=width_chars, font=("Arial", 12), textvariable=languageVar, values=languageExpressions, state="readonly")
languageCombobox.current(0)
selectButton = ttk.Button(root, text="Confirm", command=SelectLanguage)
backButton = ttk.Button(root, text="Back", command=Back)
messageLabel = ttk.Label(root, text="")

languageLabel.pack()
languageCombobox.pack()
selectButton.pack()
messageLabel.pack()
backButton.pack_forget()  # Initially hide the back button

root.mainloop()