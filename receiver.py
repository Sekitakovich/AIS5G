from functools import reduce
from operator import xor
from loguru import logger
from threading import Thread, Lock
import queue
from serial import Serial
from contextlib import closing
import socket
import time
from multiprocessing import Process, Queue as MPQueue
from dataclasses import dataclass, asdict
from typing import Dict, List
from datetime import datetime as dt

from dispatcher import Dispatcher, DispatchResult


class fromUDP(Process):
    def __init__(self, *, mcip: str, mcport: int, quePoint: MPQueue):
        super().__init__()
        self.daemon = True

        self.mcip = mcip
        self.mcport = mcport
        self.quePoint = quePoint

    def run(self) -> None:
        bufferSize = 4096
        run = True
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                                socket.inet_aton(self.mcip) + socket.inet_aton('0.0.0.0'))
                sock.bind(('', self.mcport))

                while run:
                    udpPacket, ipv4 = sock.recvfrom(bufferSize)
                    self.quePoint.put(udpPacket)
        except (socket.error,) as e:
            run = False
            logger.critical(e)


class NMEA(object):

    def __init__(self, *, serialPort: str = '', baudrate: int = 0, mcip: str = '', mcport: int = 0,
                 outQueue: queue.Queue):

        self.fragment = []
        self.seq = 0

        self.engine = Dispatcher()

        self.quePoint = MPQueue()
        self.counter = 0

        self.outQueue = outQueue

        self.w = Thread(target=self.welcome, daemon=True)
        self.w.start()

        # if serialPort:
        #     logger.debug('+++ use Serial')
        #     self.serialPort = serialPort
        #     self.baudrate = baudrate
        #     self.s = Thread(target=self.fromSerial, daemon=True)
        #     self.s.start()

        if mcip:
            logger.debug('+++ use UDP(multicast)')
            self.u = fromUDP(mcip=mcip, mcport=mcport, quePoint=self.quePoint)
            self.u.start()

    # def fromUDP(self):
    #     bufferSize = 4096
    #     run = True
    #     try:
    #         with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
    #             sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #             sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
    #                             socket.inet_aton(self.mcip) + socket.inet_aton('0.0.0.0'))
    #             sock.bind(('', self.mcport))
    #
    #             while run:
    #                 udpPacket, ipv4 = sock.recvfrom(bufferSize)
    #                 self.quePoint.put(udpPacket)
    #     except socket.error as e:
    #         run = False
    #         logger.critical(e)

    # def fromSerial(self):
    #     try:
    #         with closing(Serial(self.serialPort, baudrate=self.baudrate)) as sp:
    #             while True:
    #                 data = sp.readline()
    #                 self.quePoint.put(data)
    #     except (OSError, queue.Full) as e:
    #         logger.critical(e)

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
                self.outQueue.put(result)
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
                if item[0][-3:] == b'VDM':
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
                    pass
            else:
                raise ValueError('Checksum mismatch')

        except (IndexError, ValueError) as e:
            success = False
            logger.error(e)
            logger.debug(nmea)

        return success


@dataclass()
class Profeel(object):
    aisType: int
    name: str
    imo: int
    shipType: int
    callsign: str
    at: dt


@dataclass()
class Running(object):
    at: dt
    lon: float = 0.0
    lat: float = 0.0
    sog: float = 0.0
    hdg: int = 0
    sv: bool = True
    hv: bool = True


@dataclass()
class Vessel(object):
    profeel: Profeel
    running: Running


if __name__ == '__main__':

    qp = queue.Queue()
    collector = NMEA(mcip='239.192.0.1', mcport=60001, outQueue=qp)

    vessel: Dict[int, Vessel] = {}
    pend: Dict[int, Running] = {}
    locker = Lock()


    def cleanup():
        timeout = 10 * 60
        interval = 10
        top = dt.now()
        while True:
            time.sleep(interval)
            with locker:
                current = len(vessel)
                passed = (dt.now() - top).total_seconds()
                logger.info('=== holds %d entries (saved %d) after %d secs' % (current, len(pend), passed))
                void: Dict[int, str] = {}
                for k, v in vessel.items():
                    secs = (dt.now() - v.profeel.at).total_seconds()
                    if secs >= timeout:
                        void[k] = v.profeel.name
                for k, v in void.items():
                    del (vessel[k])
                    logger.error('--- %d (%s) was expired' % (k, v))


    def entry(*, data: DispatchResult):
        now = dt.now()
        with locker:
            header = data.header
            mmsi = header.mmsi
            body = data.body

            if header.type in [5, 19, 24]:
                name = body['shipname']
                imo = body['imo'] if 'imo' in body else ''
                callsign = body['callsign'] if 'callsign' in body else ''
                shiptype = body['shiptype']

                if mmsi not in vessel:
                    logger.debug('+++ append %d (%s)' % (mmsi, name))
                    vessel[mmsi] = Vessel(
                        profeel=Profeel(name=name, imo=imo, callsign=callsign, aisType=header.type, shipType=shiptype,
                                        at=dt.now()),
                        running=Running(at=now))
                    if mmsi in pend.keys():
                        passed = (now - pend[mmsi].at).total_seconds()
                        vessel[mmsi].running = pend[mmsi]
                        del (pend[mmsi])
                        logger.warning('$$$ %d: imported (+%d)' % (mmsi, passed))
                else:
                    secs = (now - vessel[mmsi].profeel.at).total_seconds()
                    vessel[mmsi].profeel.at = now
                    logger.success('*** %s was updated (+%d)' % (name, secs))
            elif header.type in [1, 2, 3, 18]:
                lat = float(body['lat'] / 600000)
                lon = float(body['lon'] / 600000)
                sog = float(body['speed'])
                sv = False if sog == 1023 else True
                hdg = int(body['heading'])
                hv = False if hdg == 511 else True
                if mmsi in vessel:
                    target = vessel[mmsi]
                    target.running.at = now
                    target.running.lon = lon
                    target.running.lat = lat
                    target.running.sog = sog
                    target.running.hdg = hdg
                    target.running.sv = sv
                    target.running.hv = hv
                    print(asdict(target.running))

                else:
                    ooo = Running(lat=lat, lon=lon, sog=sog, hdg=hdg, at=now, sv=sv, hv=hv)
                    pend[mmsi] = ooo
                    # logger.info('### %d %s' % (mmsi, ooo))
                    pass


    t = Thread(target=cleanup, daemon=True)
    t.start()

    while True:
        data: DispatchResult = qp.get()
        entry(data=data)
