import tkinter as tk
from tkinter import ttk
import os
def SelectLanguage():
    selectedLanguage = menuVar.get()
    selectedLanguage = selectedLanguage.split()
    print(selectedLanguage)
    if selectedLanguage == "English":
        messageLabel.config(text="English language selected.")
    elif selectedLanguage == "Spanish":
        messageLabel.config(text="Spanish language selected.")
    elif selectedLanguage == "French":
        messageLabel.config(text="French language selected.")
    HideMenuInterface()

def Back():
    menuLabel.pack()
    menuCombobox.pack()
    confirmButton.pack()
    messageLabel.config(text="")
    backButton.pack_forget()

def HideMenuInterface():
    menuLabel.pack_forget()
    menuCombobox.pack_forget()
    confirmButton.pack_forget()
    backButton.pack()

def GetDirectoryFileNames():
    additionalFiles = []
    if not os.path.exists("Saves"):
        os.mkdir('saves')
        print("create saves directory")
    else:
        with os.scandir("saves/") as directory:
            for entry in directory:
                if entry.name.endswith(".txt") and entry.is_file():
                    entryName = entry.name[:-4]
                    if entryName.find("-") != -1:
                        entryName = entryName.split("-")
                        for i in range(2):
                            if entryName[i] in languagesAbbreviations:
                                entryName[i] = languages[languagesAbbreviations.index(entryName[i])]
                            else:
                                entryName[i] = "error"
                        additionalFiles.append(f"Continue learning {entryName[0]} from {entryName[1]}")
    return additionalFiles

root = tk.Tk()
root.title("FreeCloze")
languages = ["English", "French", "German", "Italian", "Spanish", "Portuguese", "Polish", "Russian"]
languageExpressions = [f"Learn {y} from {x}" for x in languages for y in languages if x != y]
languagesAbbreviations = ["en", "fr", "de", "it", "es", "pt", "pl", "ru"]
additionalFiles = GetDirectoryFileNames()
if len(additionalFiles) > 0:
    languageExpressions = additionalFiles.copy() + ["--------------------------------------"] + languageExpressions.copy()
menuLabel = ttk.Label(root, text="Select Language:", font=("Arial", 14))
menuVar = tk.StringVar()
widthChars = int(root.winfo_screenwidth() * 0.25 / 10)  # Assuming average character width is 10 pixels
menuCombobox = ttk.Combobox(root, width=widthChars, font=("Arial", 12), textvariable=menuVar, values=languageExpressions, state="readonly")
menuCombobox.current(0)
confirmButton = ttk.Button(root, text="Confirm", command=SelectLanguage)
backButton = ttk.Button(root, text="Back", command=Back)
messageLabel = ttk.Label(root, text="")
menuLabel.pack()
menuCombobox.pack()
confirmButton.pack()
messageLabel.pack()
backButton.pack_forget()  # Initially hide the back button

root.mainloop()