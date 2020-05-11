from Engine.template import Engine as Template


class Structure(Template):  # Type 6: Binary Addressed Message

    def __init__(self):

        super().__init__()

        self.body = {
            'seqno': {'type': 'u', 'offset': 38, 'length': 2},
            'dest_mmsi': {'type': 'u', 'offset': 40, 'length': 30},
            'retransmit': {'type': 'b', 'offset': 70, 'length': 1},
            'spare': {'type': 'x', 'offset': 71, 'length': 1},
            'dac': {'type': 'u', 'offset': 72, 'length': 10},
            'fid': {'type': 'u', 'offset': 82, 'length': 6},
            # 'data': {'type': 'd', 'offset': 88, 'length': 920},
        }

        self.data = {}

    def decode(self, *, payload: str) -> dict:

        item = self.parse(payload=payload, table=self.body)

        if item['dac'] in self.data:
            dac = self.data[item['dac']]
            if item['fid'] in dac:
                data = dac[item['fid']]
                plus = self.parse(payload=payload, table=data)
                item.update(plus)
                # self.logger.debug(msg=item)
            else:
                pass
                # self.logger.debug('--- not found DAC:FID entry(%d:%d)' % (item['dac'], item['fid']))
        else:
            pass
            # self.logger.debug('--- not found DAC:FID entry(%d:%d)' % (item['dac'], item['fid']))

        return item
