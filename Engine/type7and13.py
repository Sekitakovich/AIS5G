from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 7: Binary Acknowledge

    def __init__(self):

        super().__init__()

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
