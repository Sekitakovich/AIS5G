from loguru import logger
import math
from dataclasses import dataclass
from typing import List


@dataclass()
class LatLng(object):  # on DEG format
    lat: float = 0.0
    lng: float = 0.0


class GISLib(object):

    @classmethod
    def calcHeading(cls, *, latS: int, latE: int, lonS: int, lonE: int) -> int:
        radian = math.atan2(latE - latS, lonE - lonS)
        degree = math.degrees(radian)

        angle = int(180 - (degree + 90))
        heading = angle if angle >= 0 else 360 + angle

        return heading

    @classmethod
    def calcHeadingWithF(cls, *, latS: float, latE: float, lonS: float, lonE: float) -> int:
        radian = math.atan2(latE - latS, lonE - lonS)
        degree = math.degrees(radian)

        angle = int(180 - (degree + 90))
        heading = angle if angle >= 0 else 360 + angle

        return heading

    @classmethod
    def flatDistance(cls, x1: float, y1: float, x2: float, y2: float) -> float:
        if x1 != x2 or y1 != y2:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        else:
            return 0.0


if __name__ == '__main__':

    @dataclass()
    class Location(object):
        lat: float
        lng: float
        name: str


    top = Location(lat=35.602192, lng=139.367282, name='京王多摩境駅')

    end: List[Location] = [
        # Location(name='京王多摩センター駅', lat=35.625496, lng=139.424912),
        # Location(name='京王橋本駅', lat=35.595134, lng=139.344944),
        # Location(name='JR八王子駅', lat=35.656592, lng=139.338960),
        # Location(name='小田急町田駅', lat=35.542007, lng=139.445468),
        Location(name='新宿', lat=35.690921, lng=139.700258),
        Location(name='南新宿', lat=35.683469, lng=139.698517),
        Location(name='参宮橋', lat=35.678714, lng=139.693562),
        Location(name='代々木八幡', lat=35.669484, lng=139.688635),
        Location(name='代々木上原', lat=35.669062, lng=139.679678),
        Location(name='東北沢', lat=35.665609, lng=139.673228),
        Location(name='下北沢', lat=35.661637, lng=139.666560),
        Location(name='世田谷代田', lat=35.658174, lng=139.661252),
        Location(name='梅ヶ丘', lat=35.655921, lng=139.653614),
        Location(name='豪徳寺', lat=35.653899, lng=139.646553),
        Location(name='経堂', lat=35.651316, lng=139.636437),
        Location(name='千歳船橋', lat=35.647350, lng=139.624080),
        Location(name='祖師ヶ谷大蔵', lat=35.643189, lng=139.609293),
        Location(name='成城学園前', lat=35.640053, lng=139.598741),
        Location(name='喜多見', lat=35.636692, lng=139.587098),
        Location(name='狛江', lat=35.632170, lng=139.577413),
        Location(name='和泉多摩川', lat=35.627324, lng=139.573709),
        Location(name='登戸', lat=35.620783, lng=139.569912),
        Location(name='向ヶ丘遊園', lat=35.617554, lng=139.564830),
        Location(name='生田', lat=35.615015, lng=139.542215),
        Location(name='読売ランド前', lat=35.614632, lng=139.528250),
        Location(name='百合ヶ丘', lat=35.609110, lng=139.516301),
        Location(name='新百合ヶ丘', lat=35.603805, lng=139.507605),
        Location(name='柿生', lat=35.589831, lng=139.497945),
        Location(name='鶴川', lat=35.583130, lng=139.480895),
        Location(name='玉川学園前', lat=35.563330, lng=139.463333),
        Location(name='町田', lat=35.542007, lng=139.445468),
        Location(name='相模大野', lat=35.532003, lng=139.437627),
        Location(name='小田急相模原', lat=35.515134, lng=139.422596),
        Location(name='相武台前', lat=35.499147, lng=139.408401),
        Location(name='座間', lat=35.480691, lng=139.399932),
        Location(name='海老名', lat=35.452703, lng=139.390906),
        Location(name='厚木', lat=35.443324, lng=139.378426),
        Location(name='本厚木', lat=35.439366, lng=139.364303),
        Location(name='愛甲石田', lat=35.417648, lng=139.343945),
        Location(name='伊勢原', lat=35.396033, lng=139.313504),
        Location(name='鶴巻温泉', lat=35.381131, lng=139.277813),
        Location(name='東海大学前', lat=35.373151, lng=139.271236),
        Location(name='秦野', lat=35.370175, lng=139.225868),
        Location(name='渋沢', lat=35.374168, lng=139.184510),
        Location(name='松田', lat=35.346843, lng=139.137417),
        Location(name='新松田', lat=35.345093, lng=139.139853),
        Location(name='開成', lat=35.326288, lng=139.135899),
        Location(name='栢山', lat=35.310357, lng=139.142707),
        Location(name='富水', lat=35.296356, lng=139.145464),
        Location(name='螢田', lat=35.284922, lng=139.152016),
        Location(name='足柄', lat=35.271799, lng=139.154381),
        Location(name='小田原', lat=35.256420, lng=139.154904),
        Location(name='東神奈川', lat=35.477951, lng=139.633347),
        Location(name='大口', lat=35.492164, lng=139.646157),
        Location(name='菊名', lat=35.509817, lng=139.631350),
        Location(name='新横浜', lat=35.507456, lng=139.617585),
        Location(name='小机', lat=35.508553, lng=139.600073),
        Location(name='鴨居', lat=35.510874, lng=139.567095),
        Location(name='中山', lat=35.514834, lng=139.540247),
        Location(name='十日市場', lat=35.526302, lng=139.516585),
        Location(name='長津田', lat=35.531681, lng=139.494686),
        Location(name='成瀬', lat=35.535514, lng=139.472909),
        Location(name='町田', lat=35.542007, lng=139.445468),
        Location(name='古淵', lat=35.555988, lng=139.419265),
        Location(name='淵野辺', lat=35.568756, lng=139.395058),
        Location(name='矢部', lat=35.573069, lng=139.386767),
        Location(name='相模原', lat=35.581066, lng=139.371001),
        Location(name='橋本', lat=35.594942, lng=139.345020),
        Location(name='相原', lat=35.606865, lng=139.331682),
        Location(name='八王子みなみ野', lat=35.631364, lng=139.330975),
        Location(name='片倉', lat=35.639707, lng=139.341432),
        Location(name='八王子', lat=35.655641, lng=139.338968),
    ]

    for e in end:
        heading = GISLib.calcHeadingWithF(latS=top.lat, latE=e.lat, lonS=top.lng, lonE=e.lng)
        logger.debug('%s = %d' % (e.name, heading))

# 東神奈川,35.477951,139.633347
# 大口,35.492164,139.646157
# 菊名,35.509817,139.63135
# 新横浜,35.507456,139.617585
# 小机,35.508553,139.600073
# 鴨居,35.510874,139.567095
# 中山,35.514834,139.540247
# 十日市場,35.526302,139.516585
# 長津田,35.531681,139.494686
# 成瀬,35.535514,139.472909
# 町田,35.542007,139.445468
# 古淵,35.555988,139.419265
# 淵野辺,35.568756,139.395058
# 矢部,35.573069,139.386767
# 相模原,35.581066,139.371001
# 橋本,35.594942,139.34502
# 相原,35.606865,139.331682
# 八王子みなみ野,35.631364,139.330975
# 片倉,35.639707,139.341432
# 八王子,35.655641,139.338968

# 調布,35.651889,139.544396
# 京王多摩川,35.644804,139.537042
# 京王稲田堤,35.633895,139.531099
# 京王よみうりランド,35.632923,139.517347
# 稲城,35.636216,139.50032
# 若葉台,35.619278,139.4724
# 京王永山,35.629808,139.448221
# 京王多摩センター,35.624977,139.424737
# 京王堀之内,35.624438,139.400314
# 南大沢,35.614138,139.380072
# 多摩境,35.601909,139.366985
# 橋本,35.594942,139.34502

# 新宿,35.690921,139.700258
# 南新宿,35.683469,139.698517
# 参宮橋,35.678714,139.693562
# 代々木八幡,35.669484,139.688635
# 代々木上原,35.669062,139.679678
# 東北沢,35.665609,139.673228
# 下北沢,35.661637,139.66656
# 世田谷代田,35.658174,139.661252
# 梅ヶ丘,35.655921,139.653614
# 豪徳寺,35.653899,139.646553
# 経堂,35.651316,139.636437
# 千歳船橋,35.64735,139.62408
# 祖師ヶ谷大蔵,35.643189,139.609293
# 成城学園前,35.640053,139.598741
# 喜多見,35.636692,139.587098
# 狛江,35.63217,139.577413
# 和泉多摩川,35.627324,139.573709
# 登戸,35.620783,139.569912
# 向ヶ丘遊園,35.617554,139.56483
# 生田,35.615015,139.542215
# 読売ランド前,35.614632,139.52825
# 百合ヶ丘,35.60911,139.516301
# 新百合ヶ丘,35.603805,139.507605
# 柿生,35.589831,139.497945
# 鶴川,35.58313,139.480895
# 玉川学園前,35.56333,139.463333
# 町田,35.542007,139.445468
# 相模大野,35.532003,139.437627
# 小田急相模原,35.515134,139.422596
# 相武台前,35.499147,139.408401
# 座間,35.480691,139.399932
# 海老名,35.452703,139.390906
# 厚木,35.443324,139.378426
# 本厚木,35.439366,139.364303
# 愛甲石田,35.417648,139.343945
# 伊勢原,35.396033,139.313504
# 鶴巻温泉,35.381131,139.277813
# 東海大学前,35.373151,139.271236
# 秦野,35.370175,139.225868
# 渋沢,35.374168,139.18451
# 松田,35.346843,139.137417
# 新松田,35.345093,139.139853
# 開成,35.326288,139.135899
# 栢山,35.310357,139.142707
# 富水,35.296356,139.145464
# 螢田,35.284922,139.152016
# 足柄,35.271799,139.154381
# 小田原,35.25642,139.154904
#
