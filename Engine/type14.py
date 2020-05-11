from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 14: Safety-Related Broadcast Message

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'seqno': Member(type='x', offset=38, length=2),
            'text': Member(type='t', offset=40, length=968),
        }
