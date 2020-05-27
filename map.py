import responder

class Map(object):

    def __init__(self, *, api: responder.API):
        self.api = api

    def top(self, req: responder.Request, resp: responder.Response):
        resp.content = self.api.template('index.html')

