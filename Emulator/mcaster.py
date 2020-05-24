import time
import sqlite3
from contextlib import closing
import argparse
import socket


class Emulator(object):

    def __init__(self, *, port: int=0, address: str='', file: str=''):

        self.address = address
        self.port = port
        self.file = file

    def start(self):

        ip = socket.gethostbyname(socket.gethostname())
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip))
            while True:
                with closing(sqlite3.connect(self.file)) as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    query = 'select * from sentence order by id asc'
                    cursor.execute(query)

                    for index, row in enumerate(cursor, 1):

                        delta = row['delta']
                        if delta:
                            time.sleep(delta)

                        sentence = (row['nmea'] + '\r\n').encode()
                        sock.sendto(sentence, (self.address, self.port))
                        print('%08d (%.3f) %s' % (index, delta, row['nmea']))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='AIS emulator',
        add_help=True,
    )

    file = './singapore-20181025.db'

    parser.add_argument('--db', help='SQLite db file', default=file, type=str)
    parser.add_argument('--port', help='name of UDP port', default=60001, type=int)
    parser.add_argument('--ip', help='multicast group', default='239.192.0.1', type=str)
    args = parser.parse_args()

    emulator = Emulator(port=args.port, address=args.ip, file=args.db)
    emulator.start()

