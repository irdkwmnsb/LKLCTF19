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



# TODO: replace with base64-encoded hint
COIN = b'''
                           
       ICAgICAgICAgICAg     
     IC                Ag   
   IC                    Ag 
  I    C     A  g  I       C
  A    g     I C   A       g
  I    C     Ag    I       C
  A    g     I H   N       k
  c    mF3a  2  N  hYiB    z
   ZX                    R5 
     Yi                Bl   
       c2VodCBkYWVSCg==     
 
'''[1:]

MAX_BUFFER_SIZE = 64 * 1024     # 64 KiB


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
        return await self.reader.read(n)

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
                await self.write('НЕ ДУДОСЬ МЕНЯ!!!'.encode('utf-8'))
                raise Exception('User sent a string which was too large')
        idx = self.buffer.index(b'\n')
        ret, self.buffer = self.buffer[:idx].strip(), self.buffer[idx+1:]
        return ret


class InputError(Exception):
    pass


def try_convert(a, b):
    try:
        return b(a)
    except Exception as e:
        raise InputError(repr(e)) from e


async def ask(io, b):
    s = generate_expression.gen_expression(b)
    await io.write('TASK: {}\n'.format(s).encode('utf-8'))
    await io.flush()
    result = await io.read_line()
    v = try_convert(result, int)
    return v == b


async def handle(reader, writer):
    logger.info('Connection opened')
    with IO(reader, writer) as io:
        try:
            await io.write(BANNER)
            for i, b in enumerate(reversed(flag)):
                if await ask(io, b):
                    await io.write('Correct! You have mined {} LKLCoins\n'.format((i+1)/len(flag)).encode())
                else:
                    await io.write(b'Wrong! Mining stopped\n')
                    return
            await io.write(b'Congrats! Here is your 1 LKLCoin!\n')
            await io.write(COIN)
            return
        except (InputError, EOFError) as e:
            await io.write(b'Invalid input format, mining stopped\n')
            #await io.write('Ты какую-то хуйню ввёл, переделывай\n'.encode())
    logger.info('Connection closed')


async def start_server(port):
    server = await asyncio.start_server(handle, 'localhost', port)
    await server.serve_forever()


def main():
    port = 9999 if len(sys.argv) < 2 else int(sys.argv[1])
    logger.info('Starting TCP server on {}:{}', 'localhost', port)
    
    asyncio.run(start_server(port))


if __name__ == '__main__':
    main()
