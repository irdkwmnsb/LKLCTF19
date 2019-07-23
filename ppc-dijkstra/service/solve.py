#!/usr/bin/env python3

import nclib
import sys
import json

import graph

HOST = sys.argv[1]
PORT = int(sys.argv[2])


def main():
    logfile = open('log.txt', 'wb')         # Flag will be written here
    nc = nclib.Netcat(connect=(HOST, PORT), log_send=logfile, log_recv=logfile)

    try:
        iteration = 1
        while True:
            line = nc.read_line().decode()
            if line.startswith('TASK:'):
                print(iteration)
                raw_graph = json.loads(line[5:])
                g = {int(k): v for k, v in raw_graph.items()}
                ans = graph.solve(g)
                nc.send(json.dumps(ans).encode() + b'\n')
                iteration += 1
    except nclib.errors.NetcatError:
        print('Look into log.txt, flag should be there')

if __name__ == '__main__':
    main()
