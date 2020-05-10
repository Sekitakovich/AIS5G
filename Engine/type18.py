from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):

    '''
    ClassB 標準位置通報(SO/CS共通: 差異はradioフィールドのみ)
    '''

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
            'regional': {'type': 'u', 'offset': 139, 'length': 2},
            'cs': {'type': 'b', 'offset': 141, 'length': 1},
            'display': {'type': 'b', 'offset': 142, 'length': 1},
            'dsc': {'type': 'b', 'offset': 143, 'length': 1},
            'band': {'type': 'b', 'offset': 144, 'length': 1},
            'msg22': {'type': 'b', 'offset': 145, 'length': 1},
            'assigned': {'type': 'b', 'offset': 146, 'length': 1},
            'raim': {'type': 'b', 'offset': 147, 'length': 1},
            'radio': {'type': 'u', 'offset': 148, 'length': 20},
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
            'regional': Member(type='u', offset=139, length=2),
            'cs': Member(type='b', offset=141, length=1),
            'display': Member(type='b', offset=142, length=1),
            'dsc': Member(type='b', offset=143, length=1),
            'band': Member(type='b', offset=144, length=1),
            'msg22': Member(type='b', offset=145, length=1),
            'assigned': Member(type='b', offset=146, length=1),
            'raim': Member(type='b', offset=147, length=1),
            'radio': Member(type='u', offset=148, length=20),
        }

if __name__ == '__main__':

    s = Structure()
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))