def q5(x):
    low = 1
    high = x + 1
    while high - low > 1:
        mid = (high + low) // 2
        if mid * mid * mid * mid * mid <= x:
            low = mid
        else:
            high = mid
    assert low * low * low * low * low == x
    return low

enc = open('flag.enc', 'rb').read()
enc = int.from_bytes(enc, 'big')
src = q5(enc)
b = 0
q = 1
while q <= src:
    b += 1
    q *= 256
print(src.to_bytes(b, 'big'))
