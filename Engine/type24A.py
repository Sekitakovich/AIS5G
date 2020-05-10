from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 24: Static Data Report Part A

    def __init__(self):

        super().__init__()

        self.body = {
            'partno': {'type': 'u', 'offset': 38, 'length': 2},
            'shipname': {'type': 't', 'offset': 40, 'length': 120},
            'spare': {'type': 'x', 'offset': 160, 'length': 8},
        }

        self.member: Dict[str, Member] = {
            'partno': Member(type='u', offset=38, length=2),
            'shipname': Member(type='t', offset=40, length=120),
            'spare': Member(type='x', offset=160, length=8),
        }

if __name__ == '__main__':

    s = Structure()
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))