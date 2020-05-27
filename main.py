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
import json
import responder

from dispatcher import Dispatcher, Result
from websocketServer import WebsocketServer
from map import Map
from gis import GISLib


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


class Receiver(object):

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
                # calc = reduce(xor, main, 0)
                calc = csum
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
class Profeel(object):  # 船舶の情報
    name: str = ''  # 船名
    callsign: str = ''  # JJ1MYA
    imo: int = 0  # IMO
    AISclass: str = ''  # A or B
    shipType: int = 0  # see AIS


@dataclass()
class Location(object):
    lon: float = 0.0
    lat: float = 0.0
    sog: float = 0.0
    hdg: int = 0
    sv: bool = True


@dataclass()
class Vessel(object):
    at: dt  # update at datetime
    pv: bool = False  # profeel is valid
    lv: bool = False  # locaion is valid
    ready: bool = False
    profeel: Profeel = Profeel()
    location: Location = Location()


class Collector(Thread):
    def __init__(self, *, infoQueue: queue.Queue):
        super().__init__()
        self.daemon = True

        self.holdMinutes: int = 10

        self.infoQue = infoQueue
        self.tsFormat = '%Y-%m-%d %H:%M:%S'

        self.qp = queue.Queue()
        self.receiver = Receiver(mcip='239.192.0.1', mcport=60001, outQueue=self.qp)

        self.vessel: Dict[int, Vessel] = {}
        self.entries: int = 0

        self.locker = Lock()
        self.t = Thread(target=self.cleanup, daemon=True)

    def run(self) -> None:
        self.t.start()
        while True:
            data: Result = self.qp.get()
            self.entry(data=data)

    def sendFull(self, *, mmsi: int):
        target = self.vessel[mmsi]
        info: Dict[str, any] = {
            'type': 'debut',
            'mmsi': mmsi,
            'profeel': asdict(target.profeel),
            'location': asdict(target.location),
            'at': dt.now().strftime(self.tsFormat)
        }
        self.infoQue.put(info)

    def sendLocation(self, *, mmsi: int, location: Location, at: dt):
        info: Dict[str, any] = {
            'type': 'live',
            'mmsi': mmsi,
            'location': asdict(location),
            'at': at.strftime(self.tsFormat),
        }
        self.infoQue.put(info)
        pass

    def sendVoid(self, *, mmsi: int):
        info: Dict[str, any] = {
            'type': 'retire',
            'mmsi': mmsi,
        }
        self.infoQue.put(info)
        pass

    def listUP(self) -> Dict[int, dict]:
        vessel: Dict[int, dict] = {}
        with self.locker:
            for k, v in self.vessel.items():
                if v.ready:
                    vessel[k] = {
                        'at': v.at.strftime(self.tsFormat),
                        'profeel': asdict(v.profeel),
                        'location': asdict(v.location),
                    }
        return vessel

    def cleanup(self):  # お掃除屋さん
        timeout = self.holdMinutes * 60
        interval = 5
        top = dt.now()
        last = 0
        while True:
            time.sleep(interval)
            with self.locker:
                if self.entries != last:
                    passed = (dt.now() - top).total_seconds()
                    logger.info('=== holds %d entries after %d secs' % (self.entries, passed))
                    last = self.entries
                void: Dict[int, str] = {}
                for k, v in self.vessel.items():
                    secs = (dt.now() - v.at).total_seconds()
                    if secs >= timeout:
                        void[k] = v.profeel.name if v.pv else '???'
                        self.entries -= 1
                for k, v in void.items():
                    del (self.vessel[k])
                    self.sendVoid(mmsi=k)
                    logger.error('--- %d (%s) was expired' % (k, v))

    def entry(self, *, data: Result):
        now = dt.now()
        with self.locker:
            header = data.header
            mmsi = header.mmsi
            body = data.body

            if header.type in [5, 19, 24]:
                name = body['shipname']
                imo = body['imo'] if 'imo' in body else ''
                callsign = body['callsign'] if 'callsign' in body else ''
                shiptype = body['shiptype']
                AISclass = 'A' if header.type == 5 else 'B'
                profeel = Profeel(name=name, imo=imo, callsign=callsign, AISclass=AISclass, shipType=shiptype)

                if mmsi not in self.vessel:
                    self.vessel[mmsi] = Vessel(profeel=profeel, pv=True, at=now)
                    # logger.debug('+++ append %d (%s) from profeel' % (mmsi, name))
                else:
                    target = self.vessel[mmsi]
                    secs = (now - target.at).total_seconds()
                    target.profeel = profeel
                    target.pv = True
                    target.at = now
                    if target.lv:
                        if target.ready is False:
                            target.ready = True
                            self.entries += 1
                            self.sendFull(mmsi=mmsi)
                            logger.success('!!! %d(%s) was Completed' % (mmsi, target.profeel.name))

            elif header.type in [1, 2, 3, 18]:
                degLat = int(body['lat'])
                degLon = int(body['lon'])
                lat = float(degLat / 600000)
                lon = float(degLon / 600000)
                sog = float(body['speed'])
                sv = False if sog == 1023 else True
                angle = int(body['heading'])
                if angle == 511:
                    if mmsi in self.vessel:
                        last = self.vessel[mmsi].location
                        hdg = GISLib.calcHeadingWithF(latS=last.lat, lonS=last.lon, latE=lat, lonE=lon)
                        pass
                    else:
                        hdg = 0
                else:
                    hdg = angle

                location = Location(lat=lat, lon=lon, sog=sog, hdg=hdg, sv=sv)

                if mmsi in self.vessel:
                    target = self.vessel[mmsi]
                    target.location = location
                    target.at = now
                    target.lv = True
                    if target.pv:
                        if target.ready is False:
                            target.ready = True
                            self.entries += 1
                            logger.success('!!! %d(%s) was Completed' % (mmsi,target.profeel.name))
                            self.sendFull(mmsi=mmsi)

                else:
                    self.vessel[mmsi] = Vessel(location=location, lv=True, at=now)
                if self.vessel[mmsi].ready:
                    self.sendLocation(mmsi=mmsi, location=location, at=now)

class Main(responder.API):
    def __init__(self):
        super().__init__()

        self.infoQueue = queue.Queue()
        self.t = Thread(target=self.entrance, daemon=True)
        self.t.start()

        self.collector = Collector(infoQueue=self.infoQueue)
        self.collector.start()

        '''
        websocket server
        '''
        self.ws = WebsocketServer(debug=True)
        self.add_route('/ws', self.ws.wsserver, websocket=True)

        '''
        Map
        '''
        self.map = Map(api=self)
        self.add_route('/', self.map.top)
        self.add_route('/shiplist', self.shipList)

        self.run(address='0.0.0.0', port=80)

    def shipList(self, req: responder.Request, resp: responder.Response):
        s = self.collector.listUP()
        resp.content = json.dumps(s)

    def entrance(self):
        while True:
            info = self.infoQueue.get()
            # print(info)
            self.ws.bc(message=json.dumps(info))


if __name__ == '__main__':

    main = Main()

    while True:
        time.sleep(10)
