 #hahan't

with open('./primes.txt', 'r') as f:
    b1 = f.read().split('\n')
    b2 = map(lambda s: s.split('#')[0] if len(s) and s[0] != '#' else '', b1)
    primes = list(map(int, filter(lambda s: len(s) > 0, map(lambda s: s.strip(), b2))))

ans = 1

for i in primes:
    print(i)
    ans *= i

print()
print(f'result: {ans}')
print(f'total: {len(primes)} numbers')

with open('./result.txt', 'w') as f:
    f.write(str(ans) + '\n')