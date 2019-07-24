#!/usr/bin/env python
import copy
import sys
import heapq
import random as rd
import re
import subprocess as sp
from math import *

SCOUNT = 0
SUNDER = 0
SOVER = 0


def sample(y, amplitude=0.8):
    global SCOUNT, SUNDER, SOVER
    b = int(y * amplitude * 0x7FFFFFFF)
    SCOUNT += 1
    if b < -0x7FFFFFFF:
        SUNDER += 1
        b = -0x7FFFFFFF
    if b > 0x7FFFFFFF:
        SOVER += 1
        b = 0x7FFFFFFF
    return b.to_bytes(4, 'little', signed=True)


def wave(freq, x):
    return sin(x * 2 * pi * freq)


EVENT_START = 0
EVENT_END = 1


class WaveComposer(object):
    def __init__(self):
        self.events = []
    
    def add_wave(self, start, end, freq):
        heapq.heappush(self.events, (start, EVENT_START, freq))
        heapq.heappush(self.events, (end, EVENT_END, freq))

    def compose(self, length, rate):
        waves = [[] for i in range(round(length * rate))]
        ws = []
        for x in range(len(waves)):
            while self.events:
                timestamp, event_type, freq = self.events[0]
                if x/rate < timestamp:
                    break
                heapq.heappop(self.events)
                if event_type == EVENT_START:
                    ws.append(freq)
                else:
                    ws.remove(freq)
            waves[x] = copy.copy(ws)

        samples = [(0).to_bytes(4, 'little')] * len(waves)
        for x in range(len(waves)):
            value = 0.0
            for freq in waves[x]:
                value += wave(freq, x / rate)
            if not waves[x]:
                samples[x] = sample(0)
            else:
                samples[x] = sample(value / len(waves[x]))
        return samples


def make_image(text, spacelength=1):
    with open('font.txt') as f:
        font_text = f.read()
    font = {}
    k = None
    buf = []
    for line in font_text.split('\n'):
        if re.match(r'^[ @]*$', line) is None:
            if line == '$':
                break
            if k is not None:
                font[k] = buf
                buf = []
            k = line[0]
        else:
            buf.append(line)
    font[k] = buf
    for k, v in font.items():
        maxlen = max(map(len, v))
        for i in range(len(v)):
            v[i] = v[i] + ' ' * (maxlen - len(v[i]) + spacelength)
    assert len(set(map(len, font.values()))) == 1
    buf = [[] for i in range(len(font['0']))]
    for c in text:
        fchar = font[c]
        for i in range(len(fchar)):
            buf[i].append(fchar[i])
    return [''.join(line) for line in buf]


def main():
    if 'PyPy' not in sys.version:
        print('Run me with PyPy for better performance', file=sys.stderr)
    rate = 44100
    length = 25

    comp = WaveComposer()
    image = make_image('lklctf{e9bd12a258c5a1fd}')
    syms = len(image[0])
    freqs = len(image)
    symlen = length / syms

    for fid, row in enumerate(image):
        for xid, c in enumerate(row):
            if c == '@':
                comp.add_wave(xid * symlen, (xid + 1) * symlen, 1000 + 200 * (freqs - fid))
    samples = comp.compose(length, rate)

    comp2 = WaveComposer()
    for xid in range(syms):
        comp2.add_wave(xid * symlen, (xid + 1) * symlen, 1000 + 200 * rd.randint(1, freqs))
    samples2 = comp2.compose(length, rate)

    with open('output.pcm', 'wb') as f:
        f.write(b''.join([i + j for i, j in zip(samples, samples2)]))
    print(f'samples: {SCOUNT}, under: {SUNDER}, over: {SOVER}', file=sys.stderr)
    if SUNDER > 0 or SOVER > 0:
        print('WARNING: `under` and `over` should be zeros! Try decreasing amplitude (see line 15)')
    sp.run(['ffmpeg', '-f', 's32le', '-ar', '44100', '-ac', '2', '-i', 'output.pcm', 'output.ogg', '-y'])
    print('Output file is output.ogg', file=sys.stderr)

if __name__ == '__main__':
    main()
