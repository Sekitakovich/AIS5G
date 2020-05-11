from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Type 16: Assignment Mode Command

    def __init__(self):

        super().__init__()

        self.body = {
            'spare1': {'type': 'x', 'offset': 38, 'length': 2},
            'mmsi1': {'type': 'u', 'offset': 40, 'length': 30},
            'offset1': {'type': 'u', 'offset': 70, 'length': 12},
            'increment1': {'type': 'u', 'offset': 82, 'length': 10},
            'mmsi2': {'type': 'u', 'offset': 92, 'length': 30},
            'offset2': {'type': 'u', 'offset': 122, 'length': 12},
            'increment2': {'type': 'u', 'offset': 134, 'length': 10},
        }

        self.member: Dict[str, Member] = {
            'spare1': Member(type='x', offset=38, length=2),
            'mmsi1': Member(type='u', offset=40, length=30),
            'offset1': Member(type='u', offset=70, length=12),
            'increment1': Member(type='u', offset=82, length=10),
            'mmsi2': Member(type='u', offset=92, length=30),
            'offset2': Member(type='u', offset=122, length=12),
            'increment2': Member(type='u', offset=134, length=10),
        }


if __name__ == '__main__':

    s = Structure()
    print("self.member: Dict[str, Member] = {")
    for k, v in s.body.items():
        print("'%s': Member(type='%s', offset=%s, length=%s)," % (k, v['type'], v['offset'], v['length']))
    print("}")

