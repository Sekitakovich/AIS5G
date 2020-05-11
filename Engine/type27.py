from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 27: Long Range AIS Broadcast message

    def __init__(self):

        super().__init__()

        self.body = {
            'accuracy': {'type': 'b', 'offset': 38, 'length': 1},
            'raim': {'type': 'b', 'offset': 39, 'length': 1},
            'status': {'type': 'e', 'offset': 40, 'length': 4},
            'lon': {'type': 'I4', 'offset': 44, 'length': 28},
            'lat': {'type': 'I4', 'offset': 62, 'length': 27},
            'speed': {'type': 'U1', 'offset': 79, 'length': 6},  # 0-62(kn) 63 == invalid
            'course': {'type': 'U1', 'offset': 85, 'length': 9},  # 0-359 511 == invalid
            'gnss': {'type': 'b', 'offset': 94, 'length': 1},
            'spare': {'type': 'x', 'offset': 95, 'length': 1},
        }

        self.member: Dict[str, Member] = {
            'accuracy': Member(type='b', offset=38, length=1),
            'raim': Member(type='b', offset=39, length=1),
            'status': Member(type='e', offset=40, length=4),
            'lon': Member(type='I4', offset=44, length=28),
            'lat': Member(type='I4', offset=62, length=27),
            'speed': Member(type='U1', offset=79, length=6),
            'course': Member(type='U1', offset=85, length=9),
            'gnss': Member(type='b', offset=94, length=1),
            'spare': Member(type='x', offset=95, length=1),
        }

if __name__ == '__main__':

    s = Structure()
    print("self.member: Dict[str, Member] = {")
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
    print("}")


