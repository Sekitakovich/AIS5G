from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):

    '''
    ClassB 標準位置通報(SO/CS共通: 差異はradioフィールドのみ)
    '''

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'reserved': Member(type='x', offset=38, length=8),
            'speed': Member(type='U1', offset=46, length=10),
            'accuracy': Member(type='b', offset=56, length=1),
            'lon': Member(type='I4', offset=57, length=28),
            'lat': Member(type='I4', offset=85, length=27),
            'course': Member(type='U1', offset=112, length=12),
            'heading': Member(type='u', offset=124, length=9),
            'second': Member(type='u', offset=133, length=6),
            'regional': Member(type='u', offset=139, length=2),
            'cs': Member(type='b', offset=141, length=1),
            'display': Member(type='b', offset=142, length=1),
            'dsc': Member(type='b', offset=143, length=1),
            'band': Member(type='b', offset=144, length=1),
            'msg22': Member(type='b', offset=145, length=1),
            'assigned': Member(type='b', offset=146, length=1),
            'raim': Member(type='b', offset=147, length=1),
            'radio': Member(type='u', offset=148, length=20),
        }
