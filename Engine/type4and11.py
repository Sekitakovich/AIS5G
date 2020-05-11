from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):

    def __init__(self):

        super().__init__()

        self.member: Dict[str, any] = {
            'year': Member(type='u', offset=38, length=14),
            'month': Member(type='u', offset=52, length=4),
            'day': Member(type='u', offset=56, length=5),
            'hour': Member(type='u', offset=61, length=5),
            'minute': Member(type='u', offset=66, length=6),
            'second': Member(type='u', offset=72, length=6),
            'accuracy': Member(type='b', offset=78, length=1),
            'lon': Member(type='I4', offset=79, length=28),
            'lat': Member(type='I4', offset=107, length=27),
            'epfd': Member(type='e', offset=134, length=4),
            'spare': Member(type='x', offset=138, length=10),
            'raim': Member(type='b', offset=148, length=1),
            'radio': Member(type='u', offset=149, length=19),
        }
