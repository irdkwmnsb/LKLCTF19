#!/usr/bin/env python3

import sys
from loguru import logger
import asyncio
from contextlib import closing

import generate_expression


flag = b'LKLCTF{R3VeRs3_oF_2CsA_i5_AsC1i_2be0ac50_a104b017}'

BANNER = b'''
********************************
* ADVANCED SAUSAGE COMPUTING 2 *
********************************

      ===> Welcome <===


You   will   earn  LKLCoins  for
solving  mathematical  problems.
Let's go!

'''[1:]



#f"What 50-letter word is not the same backwards? the flag"
COIN = b'''
       V2hhdCA1MC1sZXR0
     ZX                Ig
   d2                    9y
  Z    C     B  p  c       y
  B    u     b 3   Q       g
  d    G     hl    I       H
  N    h     b W   U       g
  Y    mFja  3  d  hcmR    z
   Py                    B0
     aG                Ug
       ZmxhZyAgICAgICAg
'''[1:]

MAX_BUFFER_SIZE = 8 * 1024     # 8 KiB


class IO(object):
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.buffer = b''

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.writer.close()
    
    async def recv(self, n):
        return await asyncio.wait_for(self.reader.read(n), timeout=5.0)

    async def flush(self):
        await self.writer.drain()

    async def write(self, data):
        self.writer.write(data)
        await self.flush()

    async def read_line(self):
        while b'\n' not in self.buffer:
            data = await self.recv(4096)
            if not data:
                raise EOFError()
            self.buffer += data
            if len(self.buffer) > MAX_BUFFER_SIZE:
                logger.warning('Potential DoS attack - received string is too large')
                await self.write('Не пытайся меня сломать. Я не pwn'.encode('utf-8'))
                raise Exception('User sent a string which was too large')
        idx = self.buffer.index(b'\n')
        ret, self.buffer = self.buffer[:idx].strip(), self.buffer[idx+1:]
        return ret


class InputError(Exception):
    pass


def try_func(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), True
    except Exception as e:
        return None, False


async def ask(io, b):
    task = None
    while True:
        task = generate_expression.gen_expression(b)
        logger.debug("Generated task: %s" % task)
        if try_func(eval, task)[1]:
            break
    await io.write('TASK: {}\n'.format(task).encode('utf-8'))
    await io.flush()
    result = await io.read_line()
    v, r = try_func(int, result)
    if not r:
        raise InputError()
    return v == b


async def handle(reader, writer):
    # Лютый говнокод, но вроде работает
    logger.info('Connection opened from {}', writer.get_extra_info('peername'))
    try:
        with IO(reader, writer) as io:
            try:
                await io.write(BANNER)
                for i, b in enumerate(reversed(flag)):
                    if await ask(io, b):
                        await io.write('Correct! You have mined {} LKLCoins\n'.format((i+1)/len(flag)).encode())
                    else:
                        await io.write(b'Wrong! Mining stopped\n')
                        return
                logger.info('Peer solved all tasks')
                await io.write(b'Congrats! Here is your 1 LKLCoin!\n')
                await io.write(COIN)
                return
            except (InputError, EOFError) as e:
                await io.write(b'Invalid input format, mining stopped\n')
            except asyncio.TimeoutError:
                await io.write(b'Sorry, we don\'t have time to wait so long. Bye\n')
    finally:
        logger.info('Connection closed')


async def start_server(port):
    server = await asyncio.start_server(handle, '0.0.0.0', port)
    await server.serve_forever()


def main():
    port = 9999 if len(sys.argv) < 2 else int(sys.argv[1])
    logger.info('Starting TCP server on {}:{}', '0.0.0.0', port)
    
    asyncio.run(start_server(port))


if __name__ == '__main__':
    main()
