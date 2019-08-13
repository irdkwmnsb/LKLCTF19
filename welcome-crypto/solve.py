# 93862360739236268413663408

paycheck = "cashier's check from Boris: 100"
paycheck2 = "cashier's check from Boris:1000"  # same hash

num = 6493092290128853969534189445340477021227798563586778349114399361863758254911436462


def hash(text):
    # text += SALT
    p = 17
    s = 0
    for i in range(len(text)):
        s += p ** i * ord(text[i])

    return s


print(f"need {ord(':') - ord(' ')}")
need = ord(':') - ord(' ')
print(ord('~') - ord('s'))
need -= ord('~') - ord('s')
need *= 17
print(need)

paycheck3 = f"cashier's check from Bor{chr(ord('i')+255)}~ 1000"
print(hash(paycheck2) - hash(paycheck3))  # idk why but they are not equal
print((hash(paycheck2) - hash(paycheck3)) / (17 ** 18))  # wow we should only change ~ to smth
newSymbol = chr(ord('~') + 416)
print(ord(newSymbol), newSymbol, newSymbol.isprintable())  # wow its printable

paycheck3 = f"cashier's check from Bor{chr(ord('i')+255)}{newSymbol} 1000"
print(paycheck3)
print(hash(paycheck2) == hash(paycheck3))
