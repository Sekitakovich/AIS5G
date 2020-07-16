import sys
import time
from datetime import datetime as dt
import socket
from contextlib import closing
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<level>{time:HH:mm:ss} {file}:{line}:{function} {message}</level>")


class PlayBack(object):
    def __init__(self, *, src: str = '080203_111800.txt', port:int, address: str):

        self.port = port
        self.address = address

        with open(file=src, mode='rt') as f:
            all = f.read()
            self.record = all.split('\n')

    def go(self):
        ip = socket.gethostbyname(socket.gethostname())
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip))
            counter = 0
            last = dt.now()
            for packet in self.record:
                if packet:
                    part = packet.split(' ')
                    at = dt.strptime(part[0], '%Y%m%d%H%M%S%f')
                    nmea = part[1]

                    sentence = (nmea + '\r\n').encode()
                    sock.sendto(sentence, (self.address, self.port))

                    logger.info('%s %s' % (at.strftime('%H:%M:%S'), nmea))
                    wait = (at - last).total_seconds() if counter else 0
                    time.sleep(wait)
                    counter += 1
                    last = at


if __name__ == '__main__':
    pb = PlayBack(port=60001, address='239.192.0.1')
    pb.go()
