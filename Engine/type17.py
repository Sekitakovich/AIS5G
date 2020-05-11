from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 17: DGNSS Broadcast Binary Message

    def __init__(self):

        super().__init__()

        self.body = {
            'spare1': {'type': 'x', 'offset': 38, 'length': 2},
            'lon': {'type': 'I4', 'offset': 40, 'length': 18},
            'lat': {'type': 'I4', 'offset': 58, 'length': 17},
            'spare2': {'type': 'x', 'offset': 75, 'length': 5},
            'data': {'type': 'd', 'offset': 80, 'length': 736},
        }

        self.member: Dict[str, Member] = {
            'spare1': Member(type='x', offset=38, length=2),
            'lon': Member(type='I4', offset=40, length=18),
            'lat': Member(type='I4', offset=58, length=17),
            'spare2': Member(type='x', offset=75, length=5),
            'data': Member(type='d', offset=80, length=736),
        }

if __name__ == '__main__':

    s = Structure()
    print("self.member: Dict[str, Member] = {")
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
    print("}")

