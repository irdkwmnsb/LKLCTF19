text = input()

def hash(text):
	p = 53
	s = 0
	for i in range(len(text)):
		s += p**i*ord(text[i])

	return s

print(hash(text))
