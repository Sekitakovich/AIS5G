from dataclasses import dataclass, asdict
from typing import Dict, List
import responder
import json

class Map(object):

    def __init__(self, *, api: responder.API):
        self.api = api

    def top(self, req: responder.Request, resp: responder.Response):
        resp.content = self.api.template('map.html')

