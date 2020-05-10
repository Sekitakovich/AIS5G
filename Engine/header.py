from typing import Dict
from Engine.engine import Engine, Member


class Structure(Engine):  # Common header

    def __init__(self):

        super().__init__()

        self.body = {
            'type': {'type': 'u', 'offset': 0, 'length': 6},
            'repeat': {'type': 'u', 'offset': 6, 'length': 2},
            'mmsi': {'type': 'u', 'offset': 8, 'length': 30},
        }

        self.member: Dict[str, Member] = {
            'type': Member(type='u', offset=0, length=6),
            'repeat': Member(type='u', offset=6, length=2),
            'mmsi': Member(type='u', offset=8, length=30),
        }