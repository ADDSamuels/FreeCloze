def split(textSplit, word, i, char)
string = input("C'est une vraie suprise")
textSplit = string.split()
i = 0
for word in textSplit:
    if word.find("-") > 0:
        textSplit = split(textSplit, word, i, "-")
    if word.find("'") > 0:

    i += 1
