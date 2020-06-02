import math
from loguru import logger
from libGis import LatLng


class Spy(object):
    def __init__(self, *, lat: float, lng: float, debug: bool = False):
        self.base: LatLng = LatLng(lat=lat, lng=lng)
        self.debug = debug
        if self.debug:
            logger.debug('Start with location : %s' % self.base)

    def move(self, *, kmH: float, heading: float, secs: int) -> LatLng:
        latlng = LatLng()
        head = math.radians(-heading+90) #Added 90 degrees to fix formula
        # head = math.radians(180 - (heading + 90)) #Added 90 degrees to fix formula
        d = (kmH*secs)/3600 #Distance in km
        if self.debug:
            logger.debug('Distance covered (in km) : %s' % d)
        R = 6378.1  # Radius of the Earth
        lat1 = math.radians(self.base.lat)  # Current lat point converted to radians
        lon1 = math.radians(self.base.lng)  #

        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                         math.cos(lat1) * math.sin(d / R) * math.cos(head))

        lon2 = lon1 + math.atan2(math.sin(head) * math.sin(d / R) * math.cos(lat1),
                                 math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        latlng.lat = lat2
        latlng.lng = lon2
        if self.debug:
            logger.debug('Moved to location : %s' % latlng)
        return latlng #returns Latitude and Longitude of new position

    def start(self, *, lat: float, lng: float):
        latlng = LatLng()
        latlng.lat = lat
        latlng.lng = lng
        return latlng

