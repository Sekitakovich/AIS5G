import math
from pyproj import Geod

p1_latitude = 35.3524
p1_longitude = 135.0302

# 飛行物体は緯度(obj_latitude)、経度(obj_longitude)、高度(obj_altitude)のところにある
obj_latitude = 35.3532
obj_longitude = 135.0305
obj_altitude = 1000 # 単位は(m)

# ellpsは赤道半径。GPSはWGS84を使っている。距離は6,378,137m
g = Geod(ellps='WGS84')

# inv() method
# 引数は inv(p1の経度, p1の緯度, 対象の経度, 対象の緯度, radians=False)
# radiansで出力が変わる。無し、またはFalseでDegree、Trueを入れればRadianで出力される
# 戻り値は方位角(azimuth)、反方位角(back_azimuth)、距離(distance_2d)の順番
# azimuth, back_azimuth, distance_2d = g.inv(p1_longitude, p1_latitude, obj_longitude, obj_latitude)

# 必要なものだけ欲しいなら以下でも可
result = g.inv(p1_longitude, p1_latitude, obj_longitude, obj_latitude)
# azimuth = result[0]
# back_azimuth = result[1]
distance_2d = result[2]

# inv()で求めた距離が分かれば、GPSの高度と合わせて仰角(elevation)が分かる
# math.degrees()はmath.atan2()の戻り値がRadianなので、Degree(°)に変換している。
elevation = math.degrees(math.atan2(obj_altitude, distance_2d))

# 飛行物体までの直線距離(distance_3d)はmathを使ってピタゴラスの定理
# math.pypotで求められる。
# distance_3d = math.hypot(distance_2d, obj_altitude)

print('fin')
