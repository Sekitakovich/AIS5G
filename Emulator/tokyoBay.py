import socket
from contextlib import closing
import argparse
import time


class Emulator(object):

    def __init__(self, *, port: int=0, address: str='', file: str=''):

        self.address = address
        self.port = port
        # self.wait = 0.05
        self.wait = 0.01

        with open(file, 'rt', encoding='utf-8') as f:
            all = f.read()
            self.row = all.split('\n')

    def start(self):

        ip = socket.gethostbyname(socket.gethostname())
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip))
            while True:
                for index,line in enumerate(self.row):
                    sentence = (line + '\r\n').encode()
                    sock.sendto(sentence, (self.address, self.port))
                    print('%08d (%.3f) %s' % (index, self.wait, line))
                    time.sleep(self.wait)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='AIS emulator',
        add_help=True,
    )

    file = './NMEA3_2017-11-07_TokyoBay4_withAtoN.NMEA'

    parser.add_argument('--file', help='NMEA logfile', default=file, type=str)
    parser.add_argument('--port', help='name of UDP port', default=60001, type=int)
    parser.add_argument('--ip', help='multicast group', default='239.192.0.1', type=str)
    args = parser.parse_args()

    emulator = Emulator(port=args.port, address=args.ip, file=args.file)
    emulator.start()

