text = input()

SALT = "Это нацист, это нацист, это нацист"

def hash(text):
    text += SALT
    p = 17
    s = 0
    for i in range(len(text)):
        s += p**i*ord(text[i])

    return s

print(hash(text))
