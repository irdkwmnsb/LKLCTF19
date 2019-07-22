# 93862360739236268413663408

num = 93862360739236268413663408

def hash(l):
    prime = 53
    s = 0
    for i in range(len(l)):
        s += prime**i*(l[i])

    return s

p = 53
ans = list()
nn = num
for i in range(21): 
    if nn // (p**(20-i)) >= 1: 
        ans.append(nn // p**(20-i)) 
        nn -= (nn // p**(20-i)) * (p**(20-i))
    else:
    	ans.append(0)

for x in ans[::-1]: 
    print('%' + '%02x' % x, end='')

# ?password=↑