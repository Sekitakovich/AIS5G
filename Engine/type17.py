from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 17: DGNSS Broadcast Binary Message

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'spare1': Member(type='x', offset=38, length=2),
            'lon': Member(type='I4', offset=40, length=18),
            'lat': Member(type='I4', offset=58, length=17),
            'spare2': Member(type='x', offset=75, length=5),
            'data': Member(type='d', offset=80, length=736),
        }
