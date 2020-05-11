from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):

    # ClassA 位置通報 1/2/3共通(差異はradioフィールドのみ)

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'status': Member(type='e', offset=38, length=4),
            'turn': Member(type='I3', offset=42, length=8),
            'speed': Member(type='U1', offset=50, length=10),
            'accuracy': Member(type='b', offset=60, length=1),
            'lon': Member(type='I4', offset=61, length=28),
            'lat': Member(type='I4', offset=89, length=27),
            'course': Member(type='U1', offset=116, length=12),
            'heading': Member(type='u', offset=128, length=9),
            'second': Member(type='u', offset=137, length=6),
            'maneuver': Member(type='e', offset=143, length=2),
            'spare': Member(type='x', offset=145, length=3),
            'raim': Member(type='b', offset=146, length=1),
            'radio': Member(type='u', offset=147, length=19),
        }
