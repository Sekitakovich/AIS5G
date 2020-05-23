from contextlib import closing
import sqlite3
from functools import reduce
from operator import xor
from loguru import logger
from threading import Thread
import queue
from serial import Serial
from contextlib import closing

from dispatcher import Dispatcher, Result


class NMEA(object):

    def __init__(self, *, portname: str = '', baudrate: int = 0):

        self.fragment = []
        self.seq = 0

        self.engine = Dispatcher()

        self.quePoint = queue.Queue()
        self.counter = 0

        self.w = Thread(target=self.welcome, daemon=True)
        self.w.start()

        if portname:
            self.portname = portname
            self.baudrate = baudrate
            self.s = Thread(target=self.listner, daemon=True)
            self.s.start()

    def listner(self):
        try:
            with closing(Serial(self.portname, baudrate=self.baudrate)) as sp:
                while True:
                    data = sp.readline()
                    self.quePoint.put(data)
        except (OSError, queue.Full) as e:
            logger.critical(e)

    def welcome(self):
        while True:
            obj = self.quePoint.get()
            self.enter(nmea=obj)

    def parse(self, *, payload: bytes):
        try:
            result = self.engine.parse(payload=payload.decode())
        except ValueError as e:
            logger.error(e)
        else:
            if result.support == True and result.completed == True:
                print(result)
            # else:
            #     print(self.counter)
        self.counter += 1

    def enter(self, *, nmea: bytes) -> bool:
        success: bool = True
        try:
            part = nmea.split(b'*')
            main = part[0][1:]
            if len(part) > 1:
                csum = int(part[1][:2], 16)
                calc = reduce(xor, main, 0)
            else:
                csum = 0
                calc = 0
            if csum == calc:
                item = main.split(b',')
                all = int(item[1])
                now = int(item[2])
                channel = item[4]  # Don't care
                body = item[5]

                if all > 1:  # fragment
                    seq = int(item[3])
                    if now == 1:
                        self.seq = seq

                    if seq == self.seq:
                        self.fragment.append(body)
                        if all == now:
                            payload = b''.join(self.fragment)
                            self.fragment.clear()
                            self.seq = 0
                            self.parse(payload=payload)
                        else:
                            pass
                    else:
                        self.seq = 0
                        self.fragment.clear()
                        raise ValueError('Fragment sequence mismatch')
                else:
                    self.parse(payload=body)

            else:
                raise ValueError('Checksum mismatch')

        except (IndexError, ValueError) as e:
            success = False
            logger.error(e)
            logger.debug(nmea)

        return success


if __name__ == '__main__':

    collector = NMEA()

    db = [
        # './Emulator/singapore-20171031.db',  # 使い物にならない
        './Emulator/singapore-20181025.db',
    ]

    for file in db:
        with closing(sqlite3.connect(file)) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()

            query = 'select * from sentence order by id asc'
            result = cursor.execute(query)

            for row in result:
                item = dict(row)
                nmea: bytes = item['nmea'].encode() + b'\r\n'
                # collector.enter(nmea=nmea)
                collector.quePoint.put(nmea)
