test = "C'est l'anniversaire de Muiriel ! Bon\tTest"
print(test)
test = test.split("\t")
for item in test:
    print(item)
