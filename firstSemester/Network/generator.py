import string

def AlphaNumGen():
    i = 1
    while True:
        for letter in string.lowercase:
            yield letter + str(i)
        i += 1