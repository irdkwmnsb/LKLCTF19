def f(x):
    newx = x**2 + 4919
    return newx % 0xfffff


def xorarrays(a, key):
    b = list()
    for i in range(len(a)):
        b.append(a[i] ^ key[i])
    return b 


def makekey(k, l):
    iv = 0 
    for i in range(len(k)):
        iv += i*ord(k[i])
    
    key = [iv]
    for i in range(1, l):
        key.append(f(key[i-1]))
    
    key = [x % 0xff for x in key]
    return key


tx = input()
key = input()

tx *= 2

if len(key) != 16:
    print("lox")
    exit(0)

key = makekey(key, len(tx))
a = [ord(x) for x in tx]
print(xorarrays(a, key))