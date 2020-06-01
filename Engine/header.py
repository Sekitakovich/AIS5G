from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Common header

    def __init__(self):
        super().__init__()

        self.member: Dict[str, Member] = {
            'type': Member(type='u', offset=0, length=6),
            'repeat': Member(type='u', offset=6, length=2),
            'mmsi': Member(type='u', offset=8, length=30),
        }

if __name__ == '__main__':
    e = Structure()
    p = [
        '$77gg:002?aw@0ND29GR=AT<21r1',
        '====16KDIf0002awTgbD9ro39iF60H4W',
    ]

    for s in p:
        r = e.decode(payload=s)
        if r.completed:
            print(r.body)
        else:
            print(r.reason)
