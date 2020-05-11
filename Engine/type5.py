from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):

    '''
    ClassA 静的データ
    '''

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'ais_version': Member(type='u', offset=38, length=2),
            'imo': Member(type='u', offset=40, length=30),
            'callsign': Member(type='t', offset=70, length=42),
            'shipname': Member(type='t', offset=112, length=120),
            'shiptype': Member(type='u', offset=232, length=8),
            'to_bow': Member(type='u', offset=240, length=9),
            'to_stern': Member(type='u', offset=249, length=9),
            'to_port': Member(type='u', offset=258, length=6),
            'to_starboard': Member(type='u', offset=264, length=6),
            'epfd': Member(type='u', offset=270, length=4),
            'month': Member(type='u', offset=274, length=4),
            'day': Member(type='u', offset=278, length=5),
            'hour': Member(type='u', offset=283, length=5),
            'minute': Member(type='u', offset=288, length=6),
            'draught': Member(type='U1', offset=294, length=8),
            'destination': Member(type='t', offset=302, length=120),
            'dte': Member(type='u', offset=422, length=1),
        }
