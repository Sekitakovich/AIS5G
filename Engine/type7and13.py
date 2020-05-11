from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 7: Binary Acknowledge

    def __init__(self):

        super().__init__()

        self.body = {
            'spare': {'type': 'x', 'offset': 38, 'length': 2},
            'mmsi1': {'type': 'u', 'offset': 40, 'length': 30},
            'mmsiseq1': {'type': 'u', 'offset': 70, 'length': 2},
            'mmsi2': {'type': 'u', 'offset': 72, 'length': 30},
            'mmsiseq2': {'type': 'u', 'offset': 102, 'length': 2},
            'mmsi3': {'type': 'u', 'offset': 104, 'length': 30},
            'mmsiseq3': {'type': 'u', 'offset': 134, 'length': 2},
            'mmsi4': {'type': 'u', 'offset': 136, 'length': 30},
            'mmsiseq4': {'type': 'u', 'offset': 166, 'length': 2},
        }

        self.member: Dict[str, Member] = {
            'spare': Member(type='x', offset=38, length=2),
            'mmsi1': Member(type='u', offset=40, length=30),
            'mmsiseq1': Member(type='u', offset=70, length=2),
            'mmsi2': Member(type='u', offset=72, length=30),
            'mmsiseq2': Member(type='u', offset=102, length=2),
            'mmsi3': Member(type='u', offset=104, length=30),
            'mmsiseq3': Member(type='u', offset=134, length=2),
            'mmsi4': Member(type='u', offset=136, length=30),
            'mmsiseq4': Member(type='u', offset=166, length=2),
        }

if __name__ == '__main__':

    s = Structure()
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
