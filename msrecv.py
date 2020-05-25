from multiprocessing import Process, Queue as MPQueue
import socket
from contextlib import closing
from loguru import logger


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
