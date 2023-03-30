# 해당 좌표 기준으로 사각형 그려주는 계산기

def cal(lat, lng, length):    # 위도, 경도, 구하는 범위(m)

    R = 6371000 # meter

    length /= 2

    # 위도 1도의 거리
    fixed_lat = 111194.92664455874  # R  * (np.pi / 180), meter
    delta_lat = length / fixed_lat  # 위도
    south_west_latitude = lat - abs(delta_lat)
    north_east_latitude = lat + abs(delta_lat)

    # print(delta_lat * 2 *R * (np.pi / 180))

    fixed_lng = np.cos(math.radians(lat)) * R * (np.pi / 180) # 해당 위도에서 경도 1도의 거리
    # print(fixed_lng)
    delta_lng = length / fixed_lng
    # print(delta_lng)
    # print(delta_lng * 2 *R * (np.pi / 180) * np.cos(math.radians(lat)))
    south_west_longitude = lng - abs(delta_lng)
    north_east_longitude = lng + abs(delta_lng)

    return [south_west_latitude, south_west_longitude, north_east_latitude, north_east_longitude]
            # 좌하 위도경도, 우상 위도경도


def square(lat1, lon1, lat2, lon2): # 위경도1, 위경도2
    R = 6371000
    fixed_lat = 111194.92664455874
    lat = abs(lat2 - lat1)
    세로 = lat * fixed_lat  # m

    fixed_lon = np.cos(math.radians((lat2 + lat1) / 2)) * R * (np.pi / 180) # 경도 1도당 m
    lon = abs(lon2 - lon1)
    가로 = lon * fixed_lon  # m
    
    result = (가로**2 + 세로**2)**0.5   # m

    # print('가로', 가로, '세로', 세로)
    return result