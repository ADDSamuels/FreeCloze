import re
while True:
    regex=input("Please input statement for regexifaction: ")
    regex=re.sub("([@1234567890*^%$€§\´¿¡·—£!¬¦|~#():;,.+=_><¦`…{}?\\|]+)","",regex)
    
    print("regex: "+regex)
