import nclib
import sys

HOST = '127.0.0.1'
PORT = 4001


def main():
    logfile = open('log.txt', 'wb')
    nc = nclib.Netcat(connect=(HOST, PORT), verbose=True, log_send=logfile, log_recv=logfile)
    nc.echo_hex = True

    flag = []

    try:
        while True:
            line = nc.read_line().decode()
            if line.startswith('TASK:'):
                ans = round(eval(line[5:]))
                flag.append(ans)
                nc.send(f'{ans}\n'.encode())
    except nclib.errors.NetcatError:
        print(bytes(reversed(flag)).decode())

if __name__ == '__main__':
    main()
