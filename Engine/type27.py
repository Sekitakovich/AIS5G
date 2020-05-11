from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 27: Long Range AIS Broadcast message

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'accuracy': Member(type='b', offset=38, length=1),
            'raim': Member(type='b', offset=39, length=1),
            'status': Member(type='e', offset=40, length=4),
            'lon': Member(type='I4', offset=44, length=28),
            'lat': Member(type='I4', offset=62, length=27),
            'speed': Member(type='U1', offset=79, length=6),
            'course': Member(type='U1', offset=85, length=9),
            'gnss': Member(type='b', offset=94, length=1),
            'spare': Member(type='x', offset=95, length=1),
        }
