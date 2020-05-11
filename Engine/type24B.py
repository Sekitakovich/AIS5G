from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 24: Static Data Report Part B

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'partno': Member(type='u', offset=38, length=2),
            'shiptype': Member(type='e', offset=40, length=8),
            'vendorid': Member(type='t', offset=48, length=18),
            'model': Member(type='u', offset=66, length=4),
            'serial': Member(type='u', offset=70, length=20),
            'callsign': Member(type='t', offset=90, length=42),
            'to_bow': Member(type='u', offset=132, length=9),
            'to_stern': Member(type='u', offset=141, length=9),
            'to_port': Member(type='u', offset=150, length=6),
            'to_starboard': Member(type='u', offset=156, length=6),
            'mothership_mmsi': Member(type='u', offset=132, length=30),
        }

