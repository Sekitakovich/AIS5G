from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict


# @dataclass_json()
@dataclass()
class Profeel(object):
    name: str
    age: int

@dataclass_json()
@dataclass()
class Member(object):
    number: int
    profeel: List[Profeel] = field(default_factory=list)


