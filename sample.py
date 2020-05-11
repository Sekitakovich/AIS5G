from typing import Dict
from loguru import logger

from Engine.header import Structure as Header
from Engine.type1to3 import Structure as Type1to3
from Engine.type5 import Structure as Type5
from Engine.type18 import Structure as Type18
from Engine.type19 import Structure as Type19
from Engine.type24A import Structure as Type24A
from Engine.type24B import Structure as Type24B


class Dispatcher(object):
    def __init__(self):

        self.header = Header()
        self.type1to3 = Type1to3()
        self.type5 = Type5()
        self.type18 = Type18()
        self.type19 = Type19()
        self.type24A = Type24A()
        self.type24B = Type24B()

        self.save24: Dict[str, dict] = {}

    def parse(self, *, payload: str) -> Dict[str, any]:
        result: Dict[str, any] = {}
        header = self.header.parse(payload=payload)
        if 'type' in header:
            result['header'] = header
            thisType = header['type']
            thisMMSI = header['mmsi']
            if thisType in (1, 2, 3):
                s = self.type1to3.parse(payload=payload)
                result['body'] = s
                # print('Type[%d] = %s' % (thisType, s))
            elif thisType == 5:
                s = self.type5.parse(payload=payload)
                result['body'] = s
                # print('Type[%d] = %s' % (thisType, s))
            elif thisType == 18:
                s = self.type18.parse(payload=payload)
                result['body'] = s
                # print('Type[%d] = %s' % (thisType, s))
            elif thisType == 19:
                s = self.type19.parse(payload=payload)
                result['body'] = s
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 24:

                if thisMMSI not in self.save24:
                    self.save24[thisMMSI] = {}

                target = self.save24[thisMMSI]

                partA = self.type24A.parse(payload=payload)
                if partA and partA['partno'] == 0:
                    target['A'] = partA
                partB = self.type24B.parse(payload=payload)
                if partB and partB['partno'] == 1:
                    target['B'] = partB

                if 'A' in target and 'B' in target:
                    s = target['A']
                    s.update(target['B'])
                    del(self.save24[thisMMSI])
                    result['body'] = s
                    # print('Type[%d] = %s' % (thisType, s))
            else:
                # logger.debug('void %d' % (thisType,))
                pass
        else:
            logger.critical('No type')

        return result


if __name__ == '__main__':

    vessel: Dict[int, dict] = {}
    dispatcher = Dispatcher()

    with open('payload.txt', 'rt') as f:
        for p in f.read().split('\n'):
            ooo = dispatcher.parse(payload=p)
            if 'header' in ooo.keys() and 'body' in ooo.keys():
                header = ooo['header']
                body = ooo['body']
                if header['type'] in [5, 24]:
                    vessel[header['mmsi']] = body
                    pass

        print(vessel)