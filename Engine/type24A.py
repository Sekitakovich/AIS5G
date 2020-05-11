from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 24: Static Data Report Part A

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'partno': Member(type='u', offset=38, length=2),
            'shipname': Member(type='t', offset=40, length=120),
            'spare': Member(type='x', offset=160, length=8),
        }
