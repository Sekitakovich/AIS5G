from dataclasses import dataclass, field
from datetime import datetime as dt


@dataclass()
class Profeel(object):  # 船舶の情報
    name: str = ''  # 船名
    callsign: str = ''  # JJ1MYA
    imo: int = 0  # IMO
    AISclass: str = ''  # A or B
    shipType: int = 0  # see AIS


@dataclass()
class Location(object):
    lon: float = 0.0
    lat: float = 0.0
    sog: float = 0.0
    hdg: int = 0
    sv: bool = True


@dataclass()
class Vessel(object):
    at: dt  # update at datetime
    pv: bool = False  # profeel is valid
    lv: bool = False  # locaion is valid
    ready: bool = False
    profeel: Profeel = Profeel()
    location: Location = Location()
    isCustomer: bool = False  # is customer ?
    lastSend: dt = dt.now()
