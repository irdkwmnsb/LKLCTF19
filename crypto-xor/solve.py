out = eval(input())

def f(x):
    newx = x**2 + 4919
    return newx % 0xfffff

def xorarrays(a, key):
    b = list()
    for i in range(len(a)):
        b.append(a[i] ^ key[i])
    return b 

def makekey(iv):
    key = [iv]
    for i in range(1, len(out)):
        key.append(f(key[i-1]))
    
    key = [x % 0xff for x in key]
    return key


from tqdm import tqdm
for iv in range(0, 255 * 16 * 8):
    key = makekey(iv)

    plain = list(map(chr, xorarrays(out, key)))
    if plain[:len(plain)//2] == plain[len(plain)//2::]:
        print(''.join(plain[:len(plain)//2]))