from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 19: Extended Class B CS Position Report

    def __init__(self):

        super().__init__()

        self.body = {
            'reserved': {'type': 'x', 'offset': 38, 'length': 8},
            'speed': {'type': 'U1', 'offset': 46, 'length': 10},
            'accuracy': {'type': 'b', 'offset': 56, 'length': 1},
            'lon': {'type': 'I4', 'offset': 57, 'length': 28},
            'lat': {'type': 'I4', 'offset': 85, 'length': 27},
            'course': {'type': 'U1', 'offset': 112, 'length': 12},
            'heading': {'type': 'u', 'offset': 124, 'length': 9},
            'second': {'type': 'u', 'offset': 133, 'length': 6},
            'regional': {'type': 'u', 'offset': 139, 'length': 4},
            'shipname': {'type': 't', 'offset': 143, 'length': 120},
            'shiptype': {'type': 'u', 'offset': 263, 'length': 8},
            'to_bow': {'type': 'u', 'offset': 271, 'length': 9},
            'to_stern': {'type': 'u', 'offset': 280, 'length': 9},
            'to_port': {'type': 'u', 'offset': 289, 'length': 6},
            'to_starboard': {'type': 'u', 'offset': 295, 'length': 6},
            'epfd': {'type': 'e', 'offset': 301, 'length': 4},
            'raim': {'type': 'b', 'offset': 305, 'length': 1},
            'assigned': {'type': 'b', 'offset': 307, 'length': 1},
            'spare': {'type': 'x', 'offset': 308, 'length': 4},
        }

        self.member: Dict[str, Member] = {
            'reserved': Member(type='x', offset=38, length=8),
            'speed': Member(type='U1', offset=46, length=10),
            'accuracy': Member(type='b', offset=56, length=1),
            'lon': Member(type='I4', offset=57, length=28),
            'lat': Member(type='I4', offset=85, length=27),
            'course': Member(type='U1', offset=112, length=12),
            'heading': Member(type='u', offset=124, length=9),
            'second': Member(type='u', offset=133, length=6),
            'regional': Member(type='u', offset=139, length=4),
            'shipname': Member(type='t', offset=143, length=120),
            'shiptype': Member(type='u', offset=263, length=8),
            'to_bow': Member(type='u', offset=271, length=9),
            'to_stern': Member(type='u', offset=280, length=9),
            'to_port': Member(type='u', offset=289, length=6),
            'to_starboard': Member(type='u', offset=295, length=6),
            'epfd': Member(type='e', offset=301, length=4),
            'raim': Member(type='b', offset=305, length=1),
            'assigned': Member(type='b', offset=307, length=1),
            'spare': Member(type='x', offset=308, length=4),
        }

if __name__ == '__main__':

    s = Structure()
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))