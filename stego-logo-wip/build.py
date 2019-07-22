import os

os.system('ffmpeg -i flag.txt -y flag.png')

PIXEL_WIDTH = 8
PIXEL_HEIGHT = 16

w = PIXEL_WIDTH * len(open('flag.txt').read().strip())
h = PIXEL_HEIGHT

import PIL.Image

img0 = PIL.Image.open('logo0.png')
width, height = img0.size

flag = PIL.Image.open('flag.png')

x = (width - w) // 2
y = (height - h) // 2

for i in range(width):
    for j in range(height):
        a, b, c, d = img0.getpixel((i, j))
        a &= 0xfe
        b &= 0xfe
        c &= 0xfe
        d &= 0xfe
        if i - x in range(w) and j - y in range(h) and flag.getpixel((i - x, j - y)):
            a |= 1
            b |= 1
            c |= 1
            d |= 1
        img0.putpixel((i, j), (a, b, c))

img0.save('logo.png')
