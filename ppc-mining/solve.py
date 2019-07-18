import nclib
import sys
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])


def main():
    logfile = open('log.txt', 'wb')
    nc = nclib.Netcat(connect=(HOST, PORT), log_send=logfile, log_recv=logfile)

    flag = []

    try:
        while True:
            line = nc.read_line().decode()
            if line.startswith('TASK:'):
                print(line.strip())
                ans = round(eval(line[5:]))
                flag.append(ans)
                nc.send(f'{ans}\n'.encode())
    except nclib.errors.NetcatError:
        print(bytes(reversed(flag)).decode())

if __name__ == '__main__':
    main()
