#import sys
#input(sys.getdefaultencoding())
import os
import re
import csv
import tkinter as tk
from tkinter import ttk
import codecs

import tkinter.font as tkFont
#camelCase for variables PascalCase for functions ☺
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
def LacunaOnEnter():
    print("pressed enter")
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
                entry.bind(LacunaOnEnter)

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
def LacunaRoundStart(outLang, inLang):
    global OutLangTexts
    global InLangTexts
    global RoundCount
    with open(f'saves//{outLang}-{inLang}.txt', 'r', encoding='utf-8') as file:#
        for line in file:
            line.rstrip()



    
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

def LacunaMain(outLang, inLang):
    global shift_pressed
    global previous_height
    global previous_width
    global current_entry_var
    print(outLang)
    print(inLang)
    LacunaRoundStart(outLang, inLang)
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

#LacunaMain()

def PrintLogo():
    print("███████╗██████╗░███████╗███████╗░█████╗░██╗░░░░░░█████╗░███████╗███████╗")
    print("██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██║░░░░░██╔══██╗╚════██║██╔════╝")
    print("█████╗░░██████╔╝█████╗░░█████╗░░██║░░╚═╝██║░░░░░██║░░██║░░███╔═╝█████╗░░")
    print("██╔══╝░░██╔══██╗██╔══╝░░██╔══╝░░██║░░██╗██║░░░░░██║░░██║██╔══╝░░██╔══╝░░")
    print("██║░░░░░██║░░██║███████╗███████╗╚█████╔╝███████╗╚█████╔╝███████╗███████╗")
    print("╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝░╚════╝░╚══════╝░╚════╝░╚══════╝╚══════╝")
def heapify(a, b, n, i):
    # Find largest among root and children
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and a[i] < a[l]:
        largest = l

    if r < n and a[largest] < a[r]:
        largest = r

    # If root is not largest, swap with largest and continue heapifying
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        b[i], b[largest] = b[largest] , b[i]
        a,b = heapify(a, b, n, largest)
    return a, b


def heapSort(a, b):
    n = len(a)

    # Build max heap
    for i in range(n//2, -1, -1):
        heapify(a, b, n, i)

    for i in range(n-1, 0, -1):
        # Swap
        a[i], a[0] = a[0], a[i]
        b[i], b[0] = b[0], b[i]
        # Heapify root element
        a, b = heapify(a, b, i, 0)
    return a, b
def EnterWordCount(outLang, lineCount):
    print("The language, "+outLang+", has "+str(lineCount)+" unique words")    
    if lineCount > 50000:
        print("It could be useful since the program has "+str(lineCount)+ " unique words. Type '50000' for a comprehensive fluency.")
    elif lineCount > 20000:
        print("It could be useful since the program has "+str(lineCount)+ " unique words, to type 20000 or "+str(lineCount))
    else:
        print("This language doesn't have too many words. Try typing " +str(lineCount))
    while True:
        desiredWords = input("How many words do you want to learn: ")
        if len(desiredWords) == 0:
            print("Mon Dieu -- please enter a number")
        else:
            desiredWords = int(str(desiredWords).replace("'", "").replace(",", "").replace(" ", ""))
            if desiredWords > lineCount:
                print("Unfortunately your input must be lower or equal to: "+str(lineCount))
            elif desiredWords < 10:
                print("Mon Dieu -- that's barely any words at all. Increase your number")
            else:
                return desiredWords
def CountLines(freqName):
    lineCount = 0
    if os.path.exists(freqName):
        with open(freqName, encoding='utf-8') as file:
            for line in file:
                lineCount += 1
    return lineCount
def EnterHardMode():
    while True:
        hardMode = input("Would you like hard difficulty? Y/N: ")
        if len(hardMode) == 0:
            print("Please enter Y (yes) or N (no)")
        elif (hardMode[0]).upper() == 'Y':
            hardMode = True
            #return hardMode
            print("Hard difficulty is not yet implemented!")
        elif (hardMode[0]).upper() == 'N':
            hardMode = False
            return hardMode
        else:
            print("Please enter Y (yes) or N (no)")
def GetListOfWords(freqName, lineCount):
    listOfWords = []
    i = 0
    with open(freqName, encoding='utf-8') as f:
        for line in f:
            i += 1
            #print(i)
            if i % 80000 == 0:
                menuTitle.config(text=f"{100 * i / lineCount}% complete [part 1]")
                root.update()
            if len(line) > 0:
                line = line.split()
                if len(line) == 2:
                    listOfWords.append([[line[0]], [line[1]], [i]])
                else:
                    print(f"Error: Line error by splitting. Found {len(line.split())} pieces instead of 2!")
            else:
                print("Potential error. Line was blank!")
    return listOfWords
def GetTSVList(outLang, inLang):
    i = 0
    tsvList = []
    tsvName = "tatoeba//" + outLang + "-" + inLang + ".tsv"
    with open(tsvName, encoding='utf-8') as file:#UFT-8 is not automatic on Windows
        for line in file:
            line = line.rstrip()  # Removes trailing whitespace characters from the line
            #print(line)

            line = line.split("\t")  # Splits the line into columns using the tab character as delimiter
            #print(line)
            tsvList.append([[line[1]],[line[3]]])
            
            i += 1
            if i % 20000 == 0:
                menuTitle.config(text=f"please wait [part 2] Item:({i})")
                root.update()
        # rd = csv.reader(file, delimiter="\t", quotechar='"')
        # for line in rd:
        #     tsvList.append([[line[1]],[line[3]]])
        #     i += 1
        #     if i % 20000 == 0:
        #         menuTitle.config(text=f"please wait [part 2] Item:({i})")
        #         root.update()
    return i, tsvList
def SplitTSVList(tsvList, tsvLineCount, lowerOk):
    outLangWords, outLangWordsi = [], []
    outLangWordsCount = 0
    for i in range(tsvLineCount):
        temp = str(tsvList[i][0])[2:-2]
        #print(temp)
        if len(temp) != 0:
            #print(temp)
            temp = re.sub(r"([@„“*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…}{?\\|«»]+)", "", temp)
            temp = re.sub('"', '', temp)
            temp = temp.replace("'", "' ")
            if lowerOk:
                temp = temp.lower()
            tempList = temp.split()
            length = len(tempList)
            for x in tempList:
                outLangWords.append(x)
            for j in range(length):
                outLangWordsi.append(i)
            outLangWordsCount += length
        if i % 2000 == 0:
            menuTitle.config(text=str(round(100*i/tsvLineCount, 2))+"% complete [part 3]")
            root.update()
    return outLangWords, outLangWordsi, outLangWordsCount
def WriteListToFile(fileList, fileName):
    print(fileName)
    print("fi"+str(len(fileList)))
    with open(f'{fileName}.txt', 'w', encoding='utf-8') as file:
        for fileLine in fileList:
            file.write(f"{fileLine}\n")

            
def unescape_unicode(text):
    """
    Convert Unicode escape sequences to proper Unicode characters.
    """
    # Replace escaped single quotes with single quotes
    text = text.replace("\\'", "'")
    # Convert \xa0 to non-breaking space
    text = text.replace("\\xa0", "\u00a0")
    # Convert other escaped Unicode sequences to proper Unicode characters
    text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)
    return text
def WriteTabListToFile(fileList, fileName):
    with open(f'{fileName}.txt', 'w', encoding='utf-8') as file:
        for fileLine in fileList:
            # Convert only escaped Unicode escape sequences to proper Unicode characters
            unescaped_parts = [unescape_unicode(part) for part in fileLine.split("\t")]
            unescaped_line = "\t".join(unescaped_parts)
            file.write(f"{unescaped_line}\n")
def BinarySearch(searchTerm, searchList, searchListLength):
    left = 0
    right = searchListLength
    while left <= right:
        mid = (left + right) // 2
        if searchList[mid] == searchTerm:
            return mid
        elif searchList[mid] < searchTerm:
            left = mid + 1
        else:
            right = mid - 1
    return -1
def CreateFinalList(desiredWords, outLangWords, outLangWordsi, listOfWords, lowerOk, outLangWordsCount, tsvList):
    finalList = []
    for i in range(desiredWords):
        if lowerOk:
            testWord = (str((listOfWords[i][0]))[2:-2]).lower()
        else:
            testWord = str((listOfWords[i][0]))[2:-2]
        binarySearch = BinarySearch(testWord, outLangWords, outLangWordsCount)
        if binarySearch != -1:
            j = outLangWordsi[binarySearch]
            #finalList.append(f"{(tsvList[j][0])[2:-2]}\t{(tsvList[j][1])[2:-2]}\t{str((listOfWords[i][0]))[2:-2]}\t0\t0")
            finalList.append(str(tsvList[j][0])[2:-2] + "\t" + str(tsvList[j][1])[2:-2] + "\t" + str(listOfWords[i][0])[2:-2] + "\t0\t0")
        if i % 20000 == 0:
            pass#menuTitle.config(text=f"{100*i/desiredWords}% complete [part 3]")
    return finalList
def TkEnterTypeMode(outLang, inLang):
    global inTypeMode
    inTypeMode = 1
    """ outLangText1.pack()
    outLangEntry.pack()
    outLangText2.pack(side=tk.LEFT)
    inLangText.pack() """
    #root.update()
    LacunaMain(outLang, inLang)
def refreshTypeMode(event=None):
    #print("refresh")
    if inTypeMode == 1:
        print("refresh1")
        outLangText1.pack()
        outLangEntry.pack()
        outLangText2.pack(side=tk.LEFT)
        inLangText.pack()
        root.update()

def TkSelectLanguage():
    selectedLanguage = menuVar.get()
    if selectedLanguage[0] in ["C","L"]:
        selectedLanguageList = selectedLanguage.split()
        if selectedLanguage[0] == "L":
            print(selectedLanguageList[1])
            print(selectedLanguageList[3])
            outLang = languagesAbbreviations[languages.index(selectedLanguageList[1])]
            inLang = languagesAbbreviations[languages.index(selectedLanguageList[3])]
            outLangFull = selectedLanguageList[1]
            print(outLang + "|" + inLang)
            TkScoreInterface(outLang, inLang, selectedLanguage, outLangFull)
        if selectedLanguage[0] == "C":
            outLang = languagesAbbreviations[languages.index(selectedLanguageList[2])]
            inLang = languagesAbbreviations[languages.index(selectedLanguageList[4])]
            print(outLang + "|" + inLang)
            TkHideAllMenuButtons()
            TkEnterTypeMode(outLang, inLang)
def TkHideAllMenuButtons():
    menuTitle.pack_forget()
    menuCombobox.pack_forget()
    confirmButton.pack_forget()
    desiredWordCountBox.pack_forget()
    backButton.pack_forget()

            
def TkNewLang():
    selectedLanguage = menuVar.get()
    selectedLanguageList = selectedLanguage.split()
    outLang = languagesAbbreviations[languages.index(selectedLanguageList[1])]
    inLang = languagesAbbreviations[languages.index(selectedLanguageList[3])]
    menuTitle.config(text="Please Wait")
    root.update()
    desiredWordCount = (desiredWordCountBox.get()).replace(",", "")
    print(desiredWordCount)
    if len(desiredWordCount) == 0:
        desiredWordCount = 1
    else:
        desiredWordCount = int(desiredWordCount)
    freqName = 'FrequencyWords-master//content//2018//'+outLang+'//'+outLang+'_full.txt'
    lineCount = CountLines(freqName)
    if lineCount >= desiredWordCount:
        #cosmetic
        desiredWordCountBox.pack_forget()
        confirmButton.pack_forget()
        backButton.pack_forget()
        root.update()
        lowerOk = True
        if outLang == "de":
            lowerOk = False
        if not os.path.exists(freqName):
            print(f"\n\nUnfortunately such file {freqName}doesn't exist\n\n")
        else:
            listOfWords = GetListOfWords(freqName, lineCount)
            tsvLineCount, tsvList = GetTSVList(outLang, inLang)
            outLangWords, outLangWordsi, outLangWordsCount = SplitTSVList(tsvList, tsvLineCount, lowerOk)
            menuTitle.config(text="Loading heapsort, this may take a few minutes, please leave the program alone.")
            print("Loading heapsort")
            root.update()
            outLangWords, outLangWordsi = heapSort(outLangWords, outLangWordsi)
            menuTitle.config(text="Finishing heapsort")
            print("Finishing heapsort")
            root.update()
            finalList = CreateFinalList(desiredWordCount, outLangWords, outLangWordsi, listOfWords, lowerOk, outLangWordsCount, tsvList)
            WriteTabListToFile(finalList, f"saves/{outLang}-{inLang}")
    menuTitle.config(text="Finished")
    backButton.pack()
        

def TkBack():
    menuTitle.config(text="Select Language:")
    menuTitle.pack(pady="4px")
    menuCombobox.pack(pady="4px")
    desiredWordCountBox.pack_forget()
    confirmButton.pack_forget()
    confirmButton.config(command=TkSelectLanguage, text="Confirm language")
    confirmButton.pack(pady="4px")
    backButton.pack_forget()
def TkScoreInterface(outLang, inLang, selectedLanguage, outLangFull):
    desiredWordCountBox.pack()
    desiredWordCountBox.focus()
    #backButton.pack()
    confirmButton.pack_forget()
    confirmButton.config(command=TkNewLang, text=f"Start learning {outLangFull}")
    backButton.pack()
    confirmButton.pack()
    freqName = 'FrequencyWords-master//content//2018//'+outLang+'//'+outLang+'_full.txt'
    lineCount = CountLines(freqName)
    #desiredWords = EnterWordCount(outLang, lineCount)
    if lineCount > 50000:
        menuTitle.config(text=f"Learning {selectedLanguage[6:]} is great, since the program has {lineCount} unique words.\nType '50000' for a comprehensive fluency.")
    elif lineCount > 20000:
        menuTitle.config(text=f"Learning {selectedLanguage[6:]} is good, since the program has {(lineCount)} unique words\nType 20000 or {lineCount}.")
    else:
        menuTitle.config(text=f"This language doesn't have too many words.\nTry typing {lineCount}.")
    selectedLanguage = selectedLanguage + "\n" + "lol"
    menuCombobox.pack_forget()
    #menuTitle.config(text=selectedLanguage)

def TkHideMenuInterface():
    menuTitle.pack_forget()
    menuCombobox.pack_forget()
    confirmButton.pack_forget()
    backButton.pack()

def TkGetDirectoryFileNames():
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
PrintLogo()
print("V0.1 Made by REAL NAME: type credits for credits; help for help")
print("Please note words may contain profanity and/or inappropiate references. Please don't give this program to children.")
root = tk.Tk()
root.title("FreeCloze")
languages = ["English", "French", "German", "Italian", "Spanish", "Portuguese", "Polish", "Russian"]
languageExpressions = [f"Learn {y} from {x}" for x in languages for y in languages if x != y]
languagesAbbreviations = ["en", "fr", "de", "it", "es", "pt", "pl", "ru"]
additionalFiles = TkGetDirectoryFileNames()
if len(additionalFiles) > 0:
    languageExpressions = additionalFiles.copy() + ["--------------------------------------"] + languageExpressions.copy()
menuTitle = ttk.Label(root, text="Select Language:", font=("Arial", 14))
menuVar = tk.StringVar()
widthChars = int(root.winfo_screenwidth() * 0.25 / 10)  # Assuming average character width is 10 pixels
menuCombobox = ttk.Combobox(root, width=widthChars, font=("Arial", 12), textvariable=menuVar, values=languageExpressions, state="readonly")
menuCombobox.current(0)
confirmButton = ttk.Button(root, text="Confirm language", command=TkSelectLanguage)
backButton = ttk.Button(root, text="Back", command=TkBack)
desiredWordCountBox = ttk.Entry(root)
menuTitle.pack(pady="4px")
menuCombobox.pack(pady="4px")
desiredWordCountBox.pack_forget()
confirmButton.pack(pady="4px")
inTypeMode = 0
backButton.pack_forget()  # Initially hide the back button
outLangText1 = ttk.Label(root, text="outLangText1", font=("Arial", 14))
outLangEntry = ttk.Entry(root)
fakeLabel = tk.Label(root, text="123123123") #just a test atm
outLangText2 = ttk.Label(root, text="outLangText2", font=("Arial", 14))
inLangText = ttk.Label(root, text="inLangText", font=("Arial", 14))
outLangText1.pack_forget()
outLangEntry.pack_forget()
outLangText2.pack_forget()
inLangText.pack_forget()
fakeLabel.pack_forget()
""" if inTypeMode == 1:
    root.bind("<Configure>", refreshTypeMode)
else:
    print(inTypeMode) """
root.mainloop()
