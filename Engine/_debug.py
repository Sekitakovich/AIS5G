from Engine.header import Structure as Header
from Engine.type1to3 import Structure as Type123
from Engine.type5 import Structure as Type5

if __name__ == '__main__':

    from loguru import logger

    header = Header()
    L = Type123()
    P = Type5()

    with open('../Emulator/payload.txt', 'rt') as f:
        all = f.read().split('\n')
        for line, s in enumerate(all):
            H = header.decode(payload=s)
            if H.completed:
                if H.body['type'] in [1, 2, 3]:
                    r = L.decode(payload=s)
                    if r.completed:
                        heading = r.body['heading']
                        pass
                    else:
                        logger.debug('at %d: %s -> %s' % (line, s, r.reason))
                elif H.body['type'] in [5]:
                    r = P.decode(payload=s)
                    if r.completed:
                        print(r.body['shipname'], r.body['shiptype'])
                        pass
                    else:
                        logger.debug('at %d: %s -> %s' % (line, s, r.reason))
            else:
                logger.error(H)