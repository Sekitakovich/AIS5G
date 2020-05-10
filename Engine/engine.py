from typing import Dict
import numpy as np
from dataclasses import dataclass
from loguru import logger


@dataclass()
class Member(object):
    type: str
    offset: int
    length: int


class Engine(object):

    def __init__(self):

        self.armor = '0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW`abcdefghijklmnopqrstuvw'
        self.checkTable = np.fromstring(self.armor, dtype=np.uint8)

        self.bitstring = {}
        for value, c in enumerate(self.armor):
            self.bitstring[c] = format(value, '06b')

        self.itu = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_ !\"#$%&'()*+,-./0123456789:;<=>?"  # ITU-R M.1371-5
        self.body = {}
        self.member: Dict[str, Member] = {}

    # def isValidPyaload(self, *, src: str):  # srcに変な文字が含まれていたらFalseを返す
    #
    #     return np.all(np.in1d(np.fromstring(src, dtype=np.uint8), self.checkTable))
    #
    def convert_complement_on_two_into_decimal(self, *, bits=None):  # 2018-12-21 orz ...

        return -int(bits[0]) << len(bits) | int(bits, 2)

    def parse(self, *, payload: str) -> dict:

        result = {}
        # table = self.member
        table = self.body

        try:
            src = ''.join([self.bitstring[c] for c in payload])
        except (KeyError,) as e:
            logger.error(e)
        else:
            for k, v in table.items():
                try:
                    # bits = src[v.offset:v.offset + v.length]
                    bits = src[v['offset']:v['offset'] + v['length']]

                    # type = v.type
                    type = v['type']
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

                    # else:
                    #     pass
                except Exception as e:
                    logger.critical(e)
                    # break

        return result

    def parse2(self, *, payload: str) -> Dict[str, any]:

        result: Dict[str, any] = {}
        table = self.member
        # table = self.body

        try:
            src = ''.join([self.bitstring[c] for c in payload])
        except (KeyError,) as e:
            logger.error(e)
        else:
            for k, v in table.items():
                try:
                    bits = src[v.offset:v.offset + v.length]
                    # bits = src[v['offset']:v['offset'] + v['length']]

                    type = v.type
                    # type = v['type']
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

                    # else:
                    #     pass
                except Exception as e:
                    logger.critical(e)
                    # break

        return result
