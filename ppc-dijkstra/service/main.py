#!/usr/bin/env python3
import json
import sys
from contextlib import closing

from loguru import logger
import asyncio

import graph

# Большая часть кода тупо скопирована из ppc-mining


WELCOME = b'''
You will have to calculate ping between servers 1 and `i` for i in {1, 2, 3, 4, ..., N}, where N is
the number of servers.

Accepted answer format: json dictionary, keys are server numbers, values are ping values.
No newlines, exactly one newline at the end of input. See the task description for more
complete info.

Example: if ping 1 <-> 2 = 130, ping 1 <-> 3 = 81, ping 1 <-> 4 = 13, then the answer should be:
{"1": 0, "2": 130, "3": 81, "4": 13}
'''[1:]


ITERATIONS = 50
FLAG = b'LKLCTF{8d1702cd321d611408d58c0266feb82fc2dd12406fe2dfb2bc0c7654b5a642a6}'


class InputError(Exception):
    pass


def try_parse(data):
    try:
        raw = json.loads(data.decode('utf-8'))
        return {int(k): v for k, v in raw.items()}
    except Exception as e:
        raise InputError() from e


async def handle(r, w):
    logger.info('Connection opened from {}', w.get_extra_info('peername'))
    try:
        with closing(w):
            try:
                w.write(WELCOME)
                for i in range(ITERATIONS):
                    g, correct = graph.generate()
                    w.write(b'TASK: ' + json.dumps(g).encode('utf-8') + b'\n')
                    await w.drain()
                    line = await asyncio.wait_for(r.readline(), 5.0)
                    ans = try_parse(line)
                    if ans != correct:
                        w.write(b'Incorrect!\n')
                        await w.drain()
                        return
                logger.info('Peer {} solved the task', w.get_extra_info('peername'))
                w.write(b'Congratulations! Here is your flag: ' + FLAG)
            except (InputError, EOFError) as e:
                w.write(b'Invalid input format\n')
                await w.drain()
            except asyncio.TimeoutError:
                w.write(b'Network map has changed, we don\'t need your answer now')
                await w.drain()
    finally:
        logger.info('Connection closed')


async def start_server(port):
    server = await asyncio.start_server(handle, '0.0.0.0', port)
    await server.serve_forever()


def main():
    port = 9999
    logger.info('Starting TCP server on {}:{}', '0.0.0.0', port)
    
    asyncio.run(start_server(port))


if __name__ == '__main__':
    main()
