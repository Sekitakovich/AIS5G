from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 12: Addressed Safety-Related Message

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'seqno': Member(type='x', offset=38, length=2),
            'dest_mmsi': Member(type='u', offset=40, length=30),
            'retransmit': Member(type='b', offset=70, length=1),
            'spare': Member(type='x', offset=71, length=1),
            'text': Member(type='t', offset=72, length=936),
        }
