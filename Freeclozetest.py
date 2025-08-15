import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import random
import time
import sys
from multiprocessing import Process, Event,freeze_support
from playsound import playsound
from gtts import gTTS
# Global event for stopping the process
import threading
#camelCase for variables PascalCase for functions ☺
textEntry = None
stop_event = Event()
sound_process = None
sound_duration = 0.2  # Duration to play sound (in seconds)

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) # Change working directory to the directory of the script

def play_sound(disc):
    playsound(disc)
# Function to play sound
def SoundPlay(file, stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        if time.time() - start_time >= sound_duration:
            break
        playsound(file)  # playsound is blocking; it will wait until the sound finishes
        time.sleep(0.1)  # Add a small sleep to prevent tight looping

# Function to start the sound process
def SoundStartProcess(name):
    global sound_process
    if sound_process is not None and sound_process.is_alive():
        print("Sound process is already running.")
        return
    stop_event.clear()
    print(f"name={name}")
    sound_process = Process(target=SoundPlay, args=(f"{name}.mp3", stop_event))
    sound_process.start()


def async_tts_and_play(text, filename="test"):
    def task():
        tts = gTTS(text=text, lang=outLang2, slow=False)
        tts.save(f"{filename}.mp3")
        SoundStartProcess(filename)
    threading.Thread(target=task).start()

# Function to stop the sound process
def SoundStopProcess():
    if sound_process is not None:
        stop_event.set()  # Signal the process to stop
        if sound_process.is_alive():
            sound_process.terminate()  # Forcefully terminate the process
            sound_process.join()  # Ensure the process has fully stopped
def LacunaWrapText(textSplit, mainFont, max_width, indexList):
    lines = []
    current_line = []
    current_width = 0
    space_width = mainFont.measure(" ")
    i = 0  # Initialize the counter

    while i < len(textSplit):
        word = textSplit[i]
        word_width = mainFont.measure(word)

        # Determine the spacing to be used
        if i < len(indexList) and (indexList[i] == 1 or indexList[i] == 12):
            spacing = 0
        else:
            spacing = space_width

        # Check up to two characters ahead
        if i + 1 < len(indexList) and (indexList[i + 1] == 1 or indexList[i + 1] == 12):
            spacing_next = 0
        else:
            spacing_next = space_width
        
        if i + 2 < len(indexList) and (indexList[i + 2] == 1 or indexList[i + 2] == 12):
            spacing_next_next = 0
        else:
            spacing_next_next = space_width

        if current_width + word_width + (spacing if current_line else 0) <= max_width:
            current_line.append(word)
            current_width += word_width + (spacing if current_line else 0)
        else:
            lines.append(current_line)
            current_line = [word]
            current_width = word_width

        # Move to the next word
        i += 1

    if current_line:
        lines.append(current_line)
        
    return lines

def LacunaCheckInput(entry_var):
    text = entry_var.get()
    print("Entered text:", text)
    if hasattr(entry_var, 'widget'):
        for i, char in enumerate(text):
            if i >= len(correct_word) or char.lower() != correct_word[i].lower():
                entry_var.widget.config(fg="red")
                print("Color: red")
                return
        entry_var.widget.config(fg="#00ff00")
        print("Color: green")
    else:
        print("Widget does not exist!")

def LacunaOnModified(*args, entry_var):
    LacunaCheckInput(entry_var)
def LacunaContinue(event=None): # bind() method passes the event object to it, but button doesn't give event var object, so event=None so it's optional
    print("continue page")
    #SoundStopProcess()
    root.update_idletasks()
    
    if len(roundList) == 0:
        print("Continue 1")
        LacunaUpdateGui()
        LacunaStartGui(root)
    else:
        print("Continue 2")
        LacunaStartGui(root)

def LacunaOnEnter(event, mainFont, entry_var):# event, entry, mainfont
    global textEntry
    if event.keysym == 'Return':
        if correct_word == textEntry.get():
            text = "Correct"
        elif correct_word.lower() == textEntry.get().lower():
            text = "Correct"
            entry_var.set(correct_word)
        else:
            text = "Incorrect"
        # Playing sound
        #if __name__ == "__main__": #On windows, when using the multiprocessing module, the process that spawns other processes must protect the entry point of the program using the if __name__ == '__main__': idiom.
        
        i = roundList[0]
        textEntry.config(bg=root.cget('bg'))
        textEntry.config(state="readonly")
        speakText = outLangTexts[roundList[0]]
        if text=="Correct":
            print("Answer: Correct")
            if progressInts[i] != "4":
                print("++")
                progressInts[i] = str(int(progressInts[i]) + 1)
            daysCalc = [1,10,30,180,180]
            secondsInts[i] = str(int(time.time()) + daysCalc[int(progressInts[i])] * 86400) # 24hr x 60m x 60s= 86400 seconds q.d
            print(roundList)
            #pop 1st element of roundList
            roundList.pop(0)
            print(roundList)
        else:
            print("Answer: Incorrect")
            progressInts[i] = "0"
            secondsInts[i] = "0"
            print(roundList)
            #move 1st element of roundList to the back
            roundList.append(roundList[0])
            roundList.pop(0)
            print(roundList)
            current_entry_var.set(correct_word)
            current_entry_var.widget.icursor(tk.END)
            current_entry_var.widget.config(fg="black")#
        

        textEntry.bind('<Return>', LacunaContinue) #.bind doesn't require command= since it is normally binding to a function anyway by default
        print("Color: green")
        forwardButton = tk.Button(root, text=text+"!", font=mainFont, command=LacunaContinue)
        forwardButton.place(x=xOffset,y = yPos + 40)
        root.update_idletasks()
        async_tts_and_play(speakText)


        
def LacunaCreateTextWidgets(root, textSplit, indexList, missingWordI, mainFont, maxFont, max_width, progress, entry_values=None):
    lines = LacunaWrapText(textSplit, mainFont, max_width, indexList)
    entry_widgets = []

    max_line_width = max(sum(mainFont.measure(word) for word in line) + (len(line) - 1) * mainFont.measure(" ") for line in lines)
    global xOffset
    xOffset = (root.winfo_width() - max_line_width) // 2
    #print(f"missingWordI:{missingWordI} ergo {textSplit[missingWordI]}")
    pos = 11 - len(roundList)
    
    match progress:
        case "0":
            progress = "◌"
        case "1":
            progress = "◔"
        case "2":
            progress = "◑"
        case "3":
            progress = "◕"
        case "4":
            progress = "●"
        case _:
            progress = "?"
    if len(roundList) == 10:
        textlabel = f"Saved!: {progress} "
    textlabel = f"{pos}. {progress} "
    label = tk.Label(root, text = textlabel, font=maxFont, bg=root.cget('bg'), borderwidth=0)
    print(xOffset)
    label.place(x=xOffset,y=0)
    global correct_word
    correct_word = textSplit[missingWordI]
    global yPos 
    yPos = 50
    entry_count = 0
    i = 0
    for line in lines:
        xPos = xOffset
        for word in line:
            if i == missingWordI:
                entry_var = tk.StringVar()
                entry_var.trace_add("write", lambda name, index, mode, sv=entry_var: LacunaOnModified(name, index, mode, entry_var=sv))

                if entry_values and entry_count < len(entry_values):
                    entry_var.set(entry_values[entry_count])
                entry_count += 1

                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=xPos, y=yPos)
                global textEntry
                textEntry = tk.Entry(root, textvariable=entry_var, bg="white", font=mainFont, borderwidth=0, fg="black", insertbackground="white")
                textEntry.place(x=xPos, y=yPos, width=label.winfo_reqwidth())
                entry_var.widget = textEntry
                entry_widgets.append(textEntry)
                textEntry.focus_set()
                textEntry.bind('<Return>', lambda event: LacunaOnEnter(event, mainFont, entry_var))

                global current_entry_var
                current_entry_var = entry_var
            else:
                label = tk.Label(root, text=word, font=mainFont, bg=root.cget('bg'), borderwidth=0)
                label.place(x=xPos, y=yPos)
            xPos += mainFont.measure(word) + mainFont.measure(" ")
            i += 1
        yPos += mainFont.metrics("linespace")
    
    for entries in entry_widgets:
        entries.lift()
    return yPos, xOffset

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

def ButtonsInitChar(root, windowWidth, charList):
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
            if button["text"] == "ß": #since ß reverts to SS
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
def LacunaUpdateGui():
    filePath = fr'saves/{outLang2}-{inLang2}.txt'
    tempFilePath = r'saves/temp_file.txt'

    with open(filePath, 'r', encoding='utf-8') as originalFile, open(tempFilePath, "w", encoding="utf-8") as tempFile:#
        i = 0
        for line in originalFile:
            if i in lacunaI:
                j = lacunaI.index(i)
                j2 = lacunaI[lacunaI.index(i)]
                t = "\t"
                print(f"j = {j}, j2 ={j2}{t}lacunaI ={ lacunaI}{t}i = {i}")
                tempFile.write(outLangTexts[j] + t + inLangTexts[j] + t + lacunaTexts[j] + t + progressInts[j] + t + secondsInts[j] + "\n")
                #lacunaI.pop(j)
            else:
                tempFile.write(line)
            i += 1
    os.replace(tempFilePath, filePath)
    print("Updated")
    #SoundStartProcess("Correct")
    LacunaRoundStart()


def LacunaRoundStart():
    global outLangTexts
    global inLangTexts
    global lacunaTexts
    global lacunaI
    global progressInts
    global secondsInts
    outLangTexts = []
    inLangTexts = []
    lacunaTexts = []
    progressInts = [] # Progress ints is a number from 0 -5, 0 means 0%, 1 means 25% 2=50% 3=75% and 4 = 100%
    secondsInts = []
    lacunaI = []
    global roundCount
    global roundList
    with open(rf'saves/{outLang2}-{inLang2}.txt', 'r', encoding='utf-8') as file:#
        i = 0
        for line in file:
            line.rstrip()
            lineSplit = line.split("\t")
            if len(lineSplit) == 5:
                if int(lineSplit[3]) == int(lineSplit[4]) == 0:
                    if len(outLangTexts) < 10:
                        outLangTexts.append(lineSplit[0])
                        inLangTexts.append(lineSplit[1])
                        lacunaTexts.append(lineSplit[2])
                        progressInts.append(lineSplit[3])
                        secondsInts.append(lineSplit[4])
                        lacunaI.append(i)

            else:
                print("Lacuna Error:")
                print(line)
            i += 1
    roundList = [i for i in range(0, 10)]
    random.shuffle(roundList)
    


def LacunaPunctuationSorting(word, word2, i, textSplit):
    #word2 = "".join(e for e in word if e.isalnum())
    indexList = [0] * len(textSplit)
    if word.find(word2) > 0:
        print("ping1")
        textSplit[i] = word[word.find(word2):]
        textSplit.insert(i, word[:word.find(word2)])
        indexList.append(0)
        i += 1
        indexList[i] = 12 
        word = word[word.find(word2):]
    if len(word) - len(word2) > 0:
        textSplit[i] = word[len(word2):]
        textSplit.insert(i, word[:len(word2)])
        indexList.append(0)
        if indexList[i] != 12:
            indexList[i] = 1
        indexList[i+1] = 2
    return textSplit, i, indexList
# def LacunaPunctuationSorting2(word, word2, i, textSplit, ifBefore):
#     indexList = [0] * len(textSplit)
#     if ifBefore == 0:

#     else:

#     return 0


def LacunaReturnIndexList(textSplit, missingWord):
    indexList = [0] * len(textSplit)
    i = textSplit.index(missingWord)
    indexList[i] = 1
    return textSplit, i, indexList
def TrimApostrophe(string):
    return string[:string.find("'") if "'" in string else len(string)]
# def LacunaFindIndex(text, missingWord, apostropheMode):
#     print(f"text={text},missingWord={missingWord}")
#     textSplit = text.split()
#     print(textSplit)
#     if apostropheMode:
#         f = "'"
#     else:
#         f = 0
#     missingWordCap = missingWord[0].upper() + missingWord[1:]
#     if missingWord in textSplit:
#         return LacunaReturnIndexList(textSplit, missingWord)
#     if missingWordCap in textSplit:
#         return LacunaReturnIndexList(textSplit, missingWordCap)
#     i = 0
#     for word in textSplit:
#         word2 = "".join(e for e in word if e.isalnum() or e == f)
#         if word2 == missingWord or word2 == missingWordCap:
#             return LacunaPunctuationSorting(word, word2, i, textSplit)
#         i += 1
#     i = 0
#     # do same but for - chars
#     for word in textSplit:
#         word2 = "".join(e for e in word if e.isalnum() or e=="-" or e == f) # maybe also e=="'"
#         if word2 == missingWord or word2 == missingWordCap:
#             return LacunaPunctuationSorting(word, word2, i, textSplit)
#         i += 1
#     if apostropheMode:
#         print("Error! Can't find a place!")
#         return "There is an error! Please help!".split(), 0, [0,0,0,0,0,0]
#     else:
#         return LacunaFindIndex(missingWord, textSplit, True)

def LacunaFindIndex(text, missingWord):
    print(f"text={text},missingWord={missingWord}")
    textSplit = text.split()
    print(textSplit)
    missingWordCap = missingWord[0].upper() + missingWord[1:]
    if missingWord in textSplit:
        return LacunaReturnIndexList(textSplit, missingWord)
    if missingWordCap in textSplit:
        return LacunaReturnIndexList(textSplit, missingWordCap)
    i = 0
    for word in textSplit:
        word2 = "".join(e for e in word if e.isalnum())
        if word2 == missingWord or word2 == missingWordCap:
            return LacunaPunctuationSorting(word, word2, i, textSplit)
        i += 1
    i = 0
    # do same but for special characters  
    """ for word in textSplit:
        word2 = "".join(e for e in word if e.isalnum() or e=="-") # maybe also e=="-"
        if word2 == missingWord or word2 == missingWordCap:
            return LacunaPunctuationSorting(word, word2, i, textSplit)
        i += 1 """
    #for apostrophes
    for word in textSplit:
        word2 = "".join(e for e in word if e.isalnum() or e=="'") #maybe also e=="-"
        j = word2.find("'")
        if j > -1:
            wordA = word2[:j+1]
            wordB = word2[j+1:]
            if wordA == missingWord or wordA == missingWordCap:
                print("wordA")
                return LacunaPunctuationSorting(word, wordA, i, textSplit)
            if wordB == missingWord or wordB == missingWordCap:
                print("wordB")
                return LacunaPunctuationSorting(word, wordB, i, textSplit)
        i += 1



    print("Error! Can't find a place!")
    return "There is an error! Please help!".split(), 0, [0,0,0,0,0,0] 

                    
def LacunaStartGui(root, entry_values=None):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Button):
            widget.destroy()
    maxFont = tkFont.Font(family="Arial", size=25)
    mainFont = tkFont.Font(family="Arial", size=20)
    minFont = tkFont.Font(family="Arial", size=15)
    #text = "This would be an example sentence that I wrote to show how the wrap works. I have changed the sentence so that it should be understandable and also to test if the wrapping is working correctly. Thank you."
    text = outLangTexts[roundList[0]]
    missingWord = lacunaTexts[roundList[0]]
    progress = progressInts[roundList[0]]
    textSplit, missingWordI, indexList = LacunaFindIndex(text, missingWord)
    print(textSplit)
    max_width = root.winfo_width() / 2

    if missingWord not in text:
        if missingWord.title() in text:
            missingWord = missingWord.title()
            print("Missing word is 'titled'")
        else:
            print(f"Missing Word {missingWord} not in text")
    else:
        print(missingWord)
    global yPos
    yPos, xOffset = LacunaCreateTextWidgets(root, textSplit, indexList, missingWordI, mainFont, maxFont, max_width, progress, entry_values)
    root.update_idletasks()
    
    underLabel = tk.Label(root, text = inLangTexts[roundList[0]], font=minFont, wraplength=max_width, justify='left', anchor='nw')
    yPos += 5
    underLabel.place(x=xOffset, y=yPos)
    root.update_idletasks()
    yPos += underLabel.winfo_height() 
    global buttons
    #buttonText
    print(outLang2)
    match outLang2:
        case "en":
            buttonText = "é"
        case "fr":
            buttonText = "éâêîôûàèùëïüÿæœç"
        case "de":
            buttonText = "äöüß"
        case "it":
            buttonText = "àèìòùéó"    
        case "es":
            buttonText = "áéíóúñü"
        case "pt":
            buttonText = "áéíóúâêôãõàç"
        case "pl":
            buttonText = "ąćęłńóśźż"
        case "ru":
            buttonText = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        case _:
            buttonText = "idkwouldæœùîфю"
    buttons = ButtonsInitChar(root, root.winfo_width(), buttonText)
    root.update_idletasks()
    LacunaCheckInput(current_entry_var)

def LacunaOnConfigure(event, root):
    global previous_width, previous_height
    current_width = root.winfo_width()
    current_height = root.winfo_height()

    if current_width != previous_width or current_height != previous_height:
        previous_width = current_width
        previous_height = current_height
        
        # Save current values of entries
        entry_values = [entries.get() for entries in root.winfo_children() if isinstance(entries, tk.Entry)]
        
        LacunaDebouncedStartGui(root, entry_values)

def LacunaDebounce(func, delay):
    def LacunaDebouncedFunc(*args, **kwargs):
        if hasattr(LacunaDebouncedFunc, 'after_id'):
            root.after_cancel(LacunaDebouncedFunc.after_id)
        LacunaDebouncedFunc.after_id = root.after(delay, lambda: func(*args, **kwargs))
    return LacunaDebouncedFunc

def LacunaMain():
    global shift_pressed
    global previous_height
    global previous_width
    global current_entry_var
    print(outLang2)
    print(inLang2)
    LacunaRoundStart()
    print(outLangTexts)
    print(roundList)
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

    
def TkEnterTypeMode(outLang, inLang):
    global inTypeMode
    global outLang2
    global inLang2
    outLang2 = outLang
    inLang2 = inLang
    inTypeMode = 1
    """ outLangText1.pack()
    outLangEntry.pack()
    outLangText2.pack(side=tk.LEFT)
    inLangText.pack() """
    #root.update()
    LacunaMain()
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
            print("lol")
        if selectedLanguage[0] == "C":
            outLang = languagesAbbreviations[languages.index(selectedLanguageList[2])]
            inLang = languagesAbbreviations[languages.index(selectedLanguageList[4])]
            print(outLang + "|" + inLang)
            TkHideAllMenuButtons()
            TkEnterTypeMode(outLang, inLang)
def TkHideAllMenuButtons():
    splashTitle.pack_forget()
    menuTitle.pack_forget()
    menuCombobox.pack_forget()
    confirmButton.pack_forget()
    desiredWordCountBox.pack_forget()
    backButton.pack_forget()

            

        

def TkBack():
    splashTitle.pack(pady="4px")
    menuTitle.config(text="Select Language:")
    menuTitle.pack(pady="4px")
    menuCombobox.pack(pady="4px")
    desiredWordCountBox.pack_forget()
    confirmButton.pack_forget()
    confirmButton.config(command=TkSelectLanguage, text="Confirm language")
    confirmButton.pack(pady="4px")
    backButton.pack_forget()


def TkHideMenuInterface():
    splashTitle.pack_forget()
    menuTitle.pack_forget()
    menuCombobox.pack_forget()
    confirmButton.pack_forget()
    backButton.pack()

def TkGetDirectoryFileNames():
    additionalFiles = []
    if not os.path.exists("Saves"):
        #os.makedirs('saves', exist_ok=True)
        print("create saves directory")
    else:
        with os.scandir("saves/") as directory:
            for entries in directory:
                if entries.name.endswith(".txt") and entries.is_file():
                    entryName = entries.name[:-4]
                    if entryName.find("-") != -1:
                        entryName = entryName.split("-")
                        for i in range(2):
                            if entryName[i] in languagesAbbreviations:
                                entryName[i] = languages[languagesAbbreviations.index(entryName[i])]
                            else:
                                entryName[i] = "error"
                        additionalFiles.append(f"Continue learning {entryName[0]} from {entryName[1]}")
    return additionalFiles
if __name__ == "__main__":    
    from multiprocessing import freeze_support
    freeze_support()
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
    splashTitle =ttk.Label(root, text="███████╗██████╗░███████╗███████╗░█████╗░██╗░░░░░░█████╗░███████╗███████╗\n██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██║░░░░░██╔══██╗╚════██║██╔════╝\n█████╗░░██████╔╝█████╗░░█████╗░░██║░░╚═╝██║░░░░░██║░░██║░░███╔═╝█████╗░░\n██╔══╝░░██╔══██╗██╔══╝░░██╔══╝░░██║░░██╗██║░░░░░██║░░██║██╔══╝░░██╔══╝░░\n██║░░░░░██║░░██║███████╗███████╗╚█████╔╝███████╗╚█████╔╝███████╗███████╗\n╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝░╚════╝░╚══════╝░╚════╝░╚══════╝╚══════╝\nLearn languages by filling in cloze tests",font='TkFixedFont')
    menuTitle = ttk.Label(root, text="Select Language:", font=("Arial", 14))
    menuVar = tk.StringVar()
    widthChars = int(root.winfo_screenwidth() * 0.25 / 10)  # Assuming average character width is 10 pixels
    menuCombobox = ttk.Combobox(root, width=widthChars, font=("Arial", 12), textvariable=menuVar, values=languageExpressions, state="readonly")
    menuCombobox.current(0)
    confirmButton = ttk.Button(root, text="Confirm language", command=TkSelectLanguage)
    backButton = ttk.Button(root, text="Back", command=TkBack)
    desiredWordCountBox = ttk.Entry(root)
    splashTitle.pack(pady="4px")
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
    root.mainloop()
""" if inTypeMode == 1:
    root.bind("<Configure>", refreshTypeMode)
else:
    print(inTypeMode) """

