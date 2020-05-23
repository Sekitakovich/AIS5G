import time
import sqlite3
from contextlib import closing
import argparse
from serial import Serial


class Emulator(object):

    def __init__(self, *, port=None, file=None):

        self.file = file
        self.port = port

    def start(self):

        with closing(Serial(self.port, baudrate=38400, timeout=1)) as sp:
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
                    sp.write(sentence)
                    print('%08d (%.3f) %s: %s' % (index, delta, row['hms'], row['nmea']))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='AIS emulator',
        add_help=True,
    )

    parser.add_argument('--port', help='name of serial port', default='COM5', type=str)
    parser.add_argument('--db', help='SQLite db file', default='./TokyoBay20171107.db', type=str)
    args = parser.parse_args()

    emulator = Emulator(port=args.port, file=args.db)
    emulator.start()

