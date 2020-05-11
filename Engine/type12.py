from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 12: Addressed Safety-Related Message

    def __init__(self):

        super().__init__()

        self.body = {
            'seqno': {'type': 'x', 'offset': 38, 'length': 2},
            'dest_mmsi': {'type': 'u', 'offset': 40, 'length': 30},
            'retransmit': {'type': 'b', 'offset': 70, 'length': 1},
            'spare': {'type': 'x', 'offset': 71, 'length': 1},
            'text': {'type': 't', 'offset': 72, 'length': 936},
        }

        self.member: Dict[str, Member] = {
            'seqno': Member(type='x', offset=38, length=2),
            'dest_mmsi': Member(type='u', offset=40, length=30),
            'retransmit': Member(type='b', offset=70, length=1),
            'spare': Member(type='x', offset=71, length=1),
            'text': Member(type='t', offset=72, length=936),
        }


if __name__ == '__main__':

    s = Structure()
    print("self.member: Dict[str, Member] = {")
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
    print("}")

