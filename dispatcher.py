from typing import Dict
from loguru import logger
from dataclasses import dataclass

from Engine.header import Structure as CommonHeader
from Engine.type1to3 import Structure as Type1to3
from Engine.type4and11 import Structure as Type4and11
from Engine.type5 import Structure as Type5
from Engine.type6 import Structure as Type6
from Engine.type7and13 import Structure as Type7and13
from Engine.type12 import Structure as Type12
from Engine.type14 import Structure as Type14
from Engine.type15 import Structure as Type15
from Engine.type16 import Structure as Type16
from Engine.type17 import Structure as Type17
from Engine.type18 import Structure as Type18
from Engine.type19 import Structure as Type19
from Engine.type20 import Structure as Type20
from Engine.type21 import Structure as Type21
from Engine.type24A import Structure as Type24A
from Engine.type24B import Structure as Type24B
from Engine.type27 import Structure as Type27


@dataclass()
class Header(object):
    type: int
    repeat: int
    mmsi: int


@dataclass()
class DispatchResult(object):
    header: Header
    body: Dict[str, any]
    completed: bool
    support: bool


class Dispatcher(object):
    def __init__(self):

        self.header = CommonHeader()
        self.type1to3 = Type1to3()
        self.type4and11 = Type4and11()
        self.type5 = Type5()
        self.type6 = Type6()
        self.type7and13 = Type7and13()
        self.type12 = Type12()
        self.type14 = Type14()
        self.type15 = Type15()
        self.type16 = Type16()
        self.type17 = Type17()
        self.type18 = Type18()
        self.type19 = Type19()
        self.type20 = Type20()
        self.type21 = Type21()
        self.type24A = Type24A()
        self.type24B = Type24B()
        self.type27 = Type27()

        self.save24: Dict[str, dict] = {}

    def parse(self, *, payload: str) -> DispatchResult:
        header = self.header.parse(payload=payload).body
        result = DispatchResult(header=Header(type=header['type'], repeat=header['repeat'], mmsi=header['mmsi']), body={},
                                completed=True, support=True)
        if 'type' in header:
            thisType = header['type']
            thisMMSI = header['mmsi']
            if thisType in (1, 2, 3):
                s = self.type1to3.parse(payload=payload)
                result.body = s.body

                # ooo = self.type1to3.disassemble(source=s)
                # print(ooo)

            elif thisType in [4, 11]:
                s = self.type4and11.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 5:
                s = self.type5.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 6:
                s = self.type6.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType in [7, 13]:
                result.support = False

            elif thisType == 8:
                result.support = False

            elif thisType == 12:
                s = self.type12.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 14:
                s = self.type14.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 15:
                result.support = False

            elif thisType == 16:
                s = self.type16.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 17:
                s = self.type17.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 18:
                s = self.type18.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))
            elif thisType == 19:
                s = self.type19.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 20:
                s = self.type20.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 21:
                s = self.type21.parse(payload=payload)
                result.body = s.body
                # print('Type[%d] = %s' % (thisType, s))

            elif thisType == 24:

                if thisMMSI not in self.save24:
                    self.save24[thisMMSI] = {}

                target = self.save24[thisMMSI]

                partA = self.type24A.parse(payload=payload).body
                if partA and partA['partno'] == 0:
                    target['A'] = partA
                partB = self.type24B.parse(payload=payload).body
                if partB and partB['partno'] == 1:
                    target['B'] = partB

                if 'A' in target and 'B' in target:
                    s = target['A']
                    s.update(target['B'])
                    del (self.save24[thisMMSI])
                    result.body = s
                    # print('Type[%d] = %s' % (thisType, s))
                else:
                    # result['completed'] = False
                    result.completed = False

            elif thisType == 27:
                s = self.type27.parse(payload=payload)
                result.body = s.body

            else:
                result.completed = False
                raise ValueError('void AIS type %d' % (thisType,))
                # logger.debug('void %d' % (thisType,))
                pass
        else:
            result.completed = False
            raise ValueError('No valid type')
            # logger.critical('No type')
            pass

        return result


if __name__ == '__main__':

    dispatcher = Dispatcher()

    with open('payload.txt', 'rt') as f:
        for p in f.read().split('\n'):
            ooo = dispatcher.parse(payload=p)
            if 'header' in ooo.keys() and 'body' in ooo.keys():
                header = ooo['header']
                body = ooo['body']
                if header['type'] in [5, 24]:
                    print(header, body)
