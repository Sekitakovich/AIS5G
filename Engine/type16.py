from typing import Dict
from Engine.template import Engine, Member


class Structure(Engine):  # Type 16: Assignment Mode Command

    def __init__(self):

        super().__init__()

        self.member: Dict[str, Member] = {
            'spare1': Member(type='x', offset=38, length=2),
            'mmsi1': Member(type='u', offset=40, length=30),
            'offset1': Member(type='u', offset=70, length=12),
            'increment1': Member(type='u', offset=82, length=10),
            'mmsi2': Member(type='u', offset=92, length=30),
            'offset2': Member(type='u', offset=122, length=12),
            'increment2': Member(type='u', offset=134, length=10),
        }
