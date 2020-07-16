from typing import Dict
from dataclasses import dataclass, field
from loguru import logger
from numba import jit

from common import Location, Profeel

@dataclass()
class ParseResult(object):
    completed: bool = True
    reason: str = ''
    body: Dict[str, any] = field(default_factory=dict)


@dataclass()
class Member(object):
    type: str
    offset: int
    length: int


class Engine(object):

    def __init__(self):

        armor = '0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW`abcdefghijklmnopqrstuvw'
        self.bitstring: Dict[str, str] = {key: format(value, '06b') for value, key in enumerate(armor)}

        self.itu = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_ !\"#$%&'()*+,-./0123456789:;<=>?"  # ITU-R M.1371-5

        self.member: Dict[str, Member] = {}  # to be override

    def convert_complement_on_two_into_decimal(self, *, bits: str):  # 2018-12-21 orz ...

        return -int(bits[0]) << len(bits) | int(bits, 2)

    def decode(self, *, payload: str) -> ParseResult:

        pr = ParseResult()  # challenge

        result: Dict[str, any] = {}
        table = self.member

        try:
            src = ''.join([self.bitstring[c] for c in payload])
        except (KeyError,) as e:
            pr.completed = False
            pr.reason = e
            logger.error(e)
        else:
            for k, v in table.items():
                bits = src[v.offset:v.offset + v.length]
                if bits:
                    try:

                        type = v.type
                        symbol = type[:1]

                        if symbol in ('u', 'e'):  # Unsigned integer or Enumerated type (controlled vocabulary)
                            result[k] = int(bits, 2)

                        elif symbol == 'U':  # Unsigned integer with scale - renders as float, suffix is decimal places
                            base = int(bits, 2)
                            result[k] = base / (int(type[1:]) * 10)

                        elif symbol == 'i':  # Signed integer
                            base = self.convert_complement_on_two_into_decimal(bits=bits)
                            result[k] = base

                        elif symbol == 'I':  # Signed integer with scale - renders as float, suffix is decimal places
                            base = self.convert_complement_on_two_into_decimal(bits=bits)
                            result[k] = base

                        elif symbol == 'b':  # Boolean
                            result[k] = True if int(bits, 2) else False

                        elif symbol == 'x':  # Spare or reserved bit
                            pass

                        elif symbol == 't':  # String (packed six-bit ASCII)
                            base = ''.join(
                                [self.itu[int(c, 2)] for c in [bits[p:p + 6] for p in range(0, len(bits), 6)]]
                            )
                            result[k] = base.strip().replace('@', '')
                            # result[k] = base.strip()

                        elif type[:1] == 'd':  # Data (uninterpreted binary)
                            base = [int(c, 2) for c in [bits[p:p + 8] for p in range(0, len(bits), 8)]]
                            result[k] = base
                            pass

                        elif type[:1] == 'a':  # Array boundary
                            pass
                    except Exception as e:
                        pr.completed = False
                        pr.reason = e
                        logger.critical(e)
                        break
                else:
                    # logger.debug('bits empty')
                    pr.completed = False
                    pr.reason = 'bits empty at key %s' % k
                    break

        if pr.completed:
            pr.body = result

        else:
            logger.critical(pr.reason)

        return pr
