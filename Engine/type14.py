from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 14: Safety-Related Broadcast Message

    def __init__(self):

        super().__init__()

        self.body = {
            'seqno': {'type': 'x', 'offset': 38, 'length': 2},
            'text': {'type': 't', 'offset': 40, 'length': 968},
        }

        self.member: Dict[str, Member] = {
            'seqno': Member(type='x', offset=38, length=2),
            'text': Member(type='t', offset=40, length=968),
        }


if __name__ == '__main__':

    s = Structure()
    print("self.member: Dict[str, Member] = {")
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
    print("}")


