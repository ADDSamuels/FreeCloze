# Define the list of Unicode characters
unicode_list = ['\u00A9', '\u2603', '\u2764']

# Printing each character individually
print("Printing each character individually:")
for char in unicode_list:
    print(char)

# Printing the list joined as a single string
print("\nPrinting the list joined as a single string:")
print(' '.join(unicode_list))

# Using list comprehension to display actual characters
print("\nUsing list comprehension to display actual characters:")
print([char for char in unicode_list])