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

@dataclass()
class Running(object):
    lon: float = 0.0
    lat: float = 0.0
    sog: float = 0.0
    hdg: int = 0
    sv: bool = True
    hv: bool = True

@dataclass()
class Vessel(object):
    at: dt
    profeel: Profeel
    running: Running = Running()


class Collector(Thread):
    def __init__(self, *, infoQueue: queue.Queue):
        super().__init__()
        self.daemon = True

        self.infoQue = infoQueue
        self.tsFormat = '%Y-%m-%d %H:%M:%S'

        self.qp = queue.Queue()
        self.receiver = Receiver(mcip='239.192.0.1', mcport=60001, outQueue=self.qp)

        self.vessel: Dict[int, Vessel] = {}
        self.orphan: Dict[int, Running] = {}

        self.locker = Lock()
        self.t = Thread(target=self.cleanup, daemon=True)

    def run(self) -> None:
        self.t.start()
        while True:
            data: Result = self.qp.get()
            self.entry(data=data)

    def sendProfeel(self, *, mmsi: int, profeel: Profeel):
        info: Dict[str, any] = {
            'type': 'debut',
            'mmsi': mmsi,
            'body': asdict(profeel),
            'at': dt.now().strftime(self.tsFormat)
        }
        self.infoQue.put(info)

    def sendRunning(self, *, mmsi: int, running: Running):
        info: Dict[str, any] = {
            'type': 'live',
            'mmsi': mmsi,
            'at': dt.now().strftime(self.tsFormat),
            'body': asdict(running)
        }
        self.infoQue.put(info)

    def sendVoid(self, *, mmsi: List[int]):
        info: Dict[str, any] = {
            'type': 'retire',
            'mmsi': mmsi,
        }
        self.infoQue.put(info)

    def listUP(self) -> Dict[int, dict]:
        vessel: Dict[int, dict] = {}
        with self.locker:
            for k, v in self.vessel.items():
                vessel[k] = {
                    'body': asdict(v.profeel),
                    'at': v.at.strftime(self.tsFormat)
                }
        return vessel

    def cleanup(self):  # お掃除屋さん
        timeout = 8 * 60
        interval = 1
        top = dt.now()
        last = 0
        while True:
            time.sleep(interval)
            with self.locker:
                current = len(self.vessel)
                if current > last:
                    passed = (dt.now() - top).total_seconds()
                    logger.info('=== holds %d entries after %d secs' % (current, passed))
                    last = current
                void: Dict[int, str] = {}
                for k, v in self.vessel.items():
                    secs = (dt.now() - v.at).total_seconds()
                    if secs >= timeout:
                        void[k] = v.profeel.name
                # self.sendVoid(mmsi=void.keys())
                for k, v in void.items():
                    del (self.vessel[k])
                    info: Dict[str, any] = {
                        'type': 'retire',
                        'mmsi': k,
                    }
                    self.infoQue.put(info)
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

                if mmsi not in self.vessel:
                    logger.debug('+++ append %d (%s)' % (mmsi, name))
                    profeel = Profeel(name=name, imo=imo, callsign=callsign, aisType=header.type, shipType=shiptype)
                    self.vessel[mmsi] = Vessel(profeel=profeel, at=dt.now())
                    self.sendProfeel(mmsi=mmsi, profeel=profeel)
                    if mmsi in self.orphan.keys():
                        running = self.orphan[mmsi]
                        self.vessel[mmsi].running = running
                        self.sendRunning(mmsi=mmsi, running=running)
                        del(self.orphan[mmsi])
                else:
                    secs = (now - self.vessel[mmsi].at).total_seconds()
                    self.vessel[mmsi].at = now
                    logger.success('*** %s was updated (+%d)' % (name, secs))
                    info: Dict[str, any] = {
                        'type': 'update',
                        'mmsi': mmsi,
                        'at': now.strftime(self.tsFormat),
                    }
                    self.infoQue.put(info)

            elif header.type in [1, 2, 3, 18]:
                degLat = int(body['lat'])
                degLon = int(body['lon'])
                lat = float(degLat / 600000)
                lon = float(degLon / 600000)
                sog = float(body['speed'])
                sv = False if sog == 1023 else True
                angle = int(body['heading'])
                hv = True
                if angle == 511:
                    if mmsi in self.vessel.keys():
                        last = self.vessel[mmsi].running
                        hdg = GISLib.calcHeadingWithF(latS=last.lat, lonS=last.lon, latE=lat, lonE=lon)
                    else:
                        hdg = 0
                        hv = False
                else:
                    hdg = angle

                running = Running(lat=lat, lon=lon, sog=sog, hdg=hdg, sv=sv, hv=hv)

                if mmsi in self.vessel:
                    target = self.vessel[mmsi]
                    target.running = running
                else:
                    self.orphan[mmsi] = running
                self.sendRunning(mmsi=mmsi, running=running)


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
        self.add_route('/map', self.map.top)
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
