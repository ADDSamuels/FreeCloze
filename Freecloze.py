#import sys
#input(sys.getdefaultencoding())
import os
import re
import csv
#camelCase for variables PascalCase for functions ☺
def PrintLogo():
    print("███████╗██████╗░███████╗███████╗░█████╗░██╗░░░░░░█████╗░███████╗███████╗")
    print("██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██║░░░░░██╔══██╗╚════██║██╔════╝")
    print("█████╗░░██████╔╝█████╗░░█████╗░░██║░░╚═╝██║░░░░░██║░░██║░░███╔═╝█████╗░░")
    print("██╔══╝░░██╔══██╗██╔══╝░░██╔══╝░░██║░░██╗██║░░░░░██║░░██║██╔══╝░░██╔══╝░░")
    print("██║░░░░░██║░░██║███████╗███████╗╚█████╔╝███████╗╚█████╔╝███████╗███████╗")
    print("╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝░╚════╝░╚══════╝░╚════╝░╚══════╝╚══════╝")
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
            if i % 20000 == 0:
                print(str(100 * i / lineCount)+"% complete [part 1]")
            if len(line) > 0:
                line = line.split()
                if len(line) == 2:
                    listOfWords.append([[line[0]], [line[1]], [i]])
                else:
                    print("Error: Line error by splitting. Found "+str(len (line.split()))+" pieces instead of 2!")
            else:
                print("Potential error. Line was blank!")
    return listOfWords
def GetTSVList(outLang, inLang):
    i = 0
    tsvList = []
    tsvName = "Tatoeba//" + outLang + "-" + inLang + ".tsv"
    with open(tsvName, encoding='utf-8') as file:#UFT-8 is not automatic on Windows
        rd = csv.reader(file, delimiter="\t", quotechar='"')
        for line in rd:
            tsvList.append([[line[1]],[line[3]]])
            i += 1
            if i % 20000 == 0:
                print(f"please wait [part 2] Item:({i})")
    return i, tsvList
def SplitTSVList(tsvList, tsvLineCount, lowerOk):
    outLangWords, outLangWordsi, popList = [], [], []
    outLangWordsCount = 0
    for i in range(tsvLineCount):
        temp = str(tsvList[i][0])[2:-2]
        if len(temp) != 0:
            #print(temp)
            temp = re.sub("([@„“*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…}{?\\|«»]+)", "", temp)
            temp = temp.replace("'", "' ")
            tempList = temp.split()
            length = len(tempList)
            j = 0
            while j < length:
                #tempList[j] = re.sub("([@„“*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…}{?\\|«»]+)", "", tempList[j])
                if len(tempList[j]) == 0:
                    popList.append(j)
                elif lowerOk:
                    tempList[j] = tempList[j].lower()
                j += 1
            if len(popList) > 0: #reversing the List, if I pop off the item 1, I have to adjust the rest of the list, for the rest of the pops
                popList.sort(reverse=True)
                print("↓"+str(i))
                print(tempList)
                print(popList)
                for k in popList:
                    tempList.pop(k)
                print(tempList)
                print("↑")
            length -= len(popList)
            outLangWords = outLangWords.copy() + tempList
            outLangWordsi = outLangWordsi.copy() + [j]*length
            outLangWordsCount += length
            #print(".")
            popList = []
    return outLangWords, outLangWordsi, outLangWordsCount
def WriteListToFile(fileList, fileName):
    with open(f'{fileName}.txt', 'w', encoding='utf-8') as file:
        for fileLine in fileList:
            file.write(f"{fileLine}\n")
def NewLang():
    lowerOk = True
    inLang = input("What language do you speak?, Type the two letter code: ")#no error checking
    if inLang == 'en' or inLang[:2] == 'en':
        print("Great!")
    else:
        print("More languages will be added!")
    outLang = input("What language do you want to learn?, Type the two letter code: ")#no error checking
    if outLang == 'de' or outLang[:2] == 'de':
        print("Great!")
        lowerOk = True
    else:
        print("More languages will be added")
    print("Please wait")
    freqName = 'FrequencyWords-master//content//2018//'+outLang+'//'+outLang+'_full.txt'
    if not os.path.exists(freqName):
        print(f"\n\nUnfortunately such file {freqName}doesn't exist\n\n")
    lineCount = CountLines(freqName)
    desiredWords = EnterWordCount(outLang, lineCount)
    hardMode = EnterHardMode()
    listOfWords = GetListOfWords(freqName, lineCount)
    #print(listOfWords)
    tsvLineCount, tsvList = GetTSVList(outLang, inLang)
    outLangWords, outLangWordsi, outLangWordsCount = SplitTSVList(tsvList, tsvLineCount, lowerOk)
    WriteListToFile(outLangWords, "outlangwords")
    WriteListToFile(outLangWordsi, "outlangwords")
    WriteListToFile(outLangWordsCount, "outLangWordsCount")
    #print(tsvList)
    #print(tsvList[0:3])
    print(f"Length of TSV list={len(tsvList)}")
    skippedWordList = []
    i=0
    #print(listOfWords[0][0])
    #print(listOfWords[1][0])
    #print(listOfWords[2][0])
    finalList = []
    for i in range(desiredWords):
        if i % 50 == 0:
            print(str(100*i/desiredWords)+"% complete [part 3]")
        if hardMode:
            print("Hard mode doesn't work!")
        else:
            j = 0
            loopPass = 0
            if lowerOk:
                testWord = (str((listOfWords[i][0]))[2:-2]).lower()
            else:
                testWord = str((listOfWords[i][0]))[2:-2]
            while j < tsvLineCount and loopPass == 0:
                try:
                    test = str(tsvList[j][0])[2:-2]
                    if len(test) == 0:
                        print("len of test is 0!")
                    test = test.replace("'", "' ")
                    test = test.split()
                    length = len(test)
                    k = 0
                    while k < length:
                        if lowerOk:
                            test[k] = re.sub("([@*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…}{?\\|«»]+)", "", test[k]).lower()
                        else:
                            test[k] = re.sub("([@*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…}{?\\|«»]+)", "", test[k])
                        k += 1
                    if testWord in test:
                        loopPass = 1
                        finalList.append(f"{tsvList[j][0]}\t{tsvList[j][1]}\t{str((listOfWords[i][0]))[2:-2]}")
                    else:
                        j += 1
                except:
                    print(f"{test}\ntestword:{testWord}\ni:{i}\nj:{j}")
                    print("\nERROR!!\n")
                    j += 1
                    loopPass = 1
            if j == tsvLineCount:
                skippedWordList.append(testWord)
        i += 1
        if tsvLineCount > j:
            pass
        else:
            print(f"Error! j={j}")
        #print("i:"+str(i))
    print("Skipped words="+str(skippedWordList))
    with open(f'{outLang}-{inLang}-{desiredWords}.txt', 'w', encoding='utf-8') as file:
        for line in finalList:
            file.write(f"{line}\n")

PrintLogo()
print("V0.1 Made by REAL NAME: type credits for credits; help for help")
print("Please note words may contain profanity and/or inappropiate references. Please don't give this program to children.")
if not os.path.exists("Saves"):
    os.mkdir('saves')
    print("Welcome to FreeCloze! This is a free software")
else:
    print("Welcome back to FreeCloze!")
NewLang()

#assuming unsaved, and have selected German to learn
#assumed learning from English



















a=input('\nProgram finished')
