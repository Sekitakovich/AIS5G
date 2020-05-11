from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 21: Aid-to-Navigation Report

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'aid_type': Member(type='e', offset=38, length=5),
            'name': Member(type='t', offset=43, length=120),
            'accuracy': Member(type='b', offset=163, length=1),
            'lon': Member(type='I4', offset=164, length=28),
            'lat': Member(type='I4', offset=192, length=27),
            'to_bow': Member(type='u', offset=219, length=9),
            'to_stern': Member(type='u', offset=228, length=9),
            'to_port': Member(type='u', offset=237, length=6),
            'to_starboard': Member(type='u', offset=243, length=6),
            'epfd': Member(type='e', offset=249, length=4),
            'second': Member(type='x', offset=253, length=6),
            'off_position': Member(type='b', offset=259, length=1),
            'regional': Member(type='u', offset=260, length=8),
            'raim': Member(type='b', offset=268, length=1),
            'virtual_aid': Member(type='b', offset=269, length=1),
            'assigned': Member(type='b', offset=270, length=1),
            'spare': Member(type='x', offset=271, length=1),
            'extension': Member(type='t', offset=272, length=88),
        }
