import numpy as np
import math
import pymysql
import csv

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
    
def data(query):
    # MySQL 서버에 연결합니다.
    conn = pymysql.connect(
        host='db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com',
        user='iujuser',
        password='!uj2023',
        db='iujdev',
        charset='utf8mb4'
    )

#     # 커서 객체를 생성합니다.
    cursor = conn.cursor()

#     # SQL 쿼리를 실행합니다.
    # cursor.execute(query)
    # "SELECT lat, lng FROM apt"

#     # 저장
    conn.commit()

#     # 결과를 가져옵니다.
    result = cursor.fetchall()
    print(result)

#     # 연결을 닫습니다.
#     conn.close()

#     return result

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

print(data("SELECT lat, lng, id FROM officetel"))
# def intersection_area(rectangles):
#     x_min = min(rect[0] for rect in rectangles)
#     y_min = min(rect[1] for rect in rectangles)
#     x_max = max(rect[2] for rect in rectangles)
#     y_max = max(rect[3] for rect in rectangles)

#     grid = [[0] * (y_max - y_min) for _ in range(x_max - x_min)]

#     for rect in rectangles:
#         for i in range(rect[0] - x_min, rect[2] - x_min):
#             for j in range(rect[1] - y_min, rect[3] - y_min):
#                 grid[i][j] = 1

#     area = 0
#     for i in range(x_max - x_min):
#         for j in range(y_max - y_min):
#             if grid[i][j] == 1:
#                 area += 1

#     return area


# with open('cctv_officetel.csv', mode='w', newline='') as new_file:
#     fieldnames = ['id', 'type', 'cctv']  # 포함시키고 싶은 컬럼(column) 이름 정의
#     writer = csv.DictWriter(new_file, fieldnames=fieldnames)

#     # CSV 파일에 헤더(header) 작성
#     writer.writeheader()

    
# 기존 테이블에서 특정 컬럼(column)만을 선택하여 CSV 파일에 작성
# building = data("SELECT lat, lng, id FROM officetel")
# for i in building:
#     if float(i[0]):

#         if new_cctvs:
#             cctv_area = intersection_area(new_cctvs)
#         else:
#             cctv_area = 0
#         result = cctv_area // 100
#         writer.writerow({'id': i[2], 'type': 'OFFICETEL', 'cctv': result})


'''
# # R = 6371000 # 지구 반지름(m)

# apt = data("SELECT lat, lng, id FROM officetel")


# for i in apt:
#     if float(i[0]):
#         lat = np.longdouble(i[0])  # 위도 degree
#         lng = np.longdouble(i[1])  # 경도
#         print(i)
#         # 150m 범위 안의 cctv를 찾아야함
#         area_150 = cal(lat, lng, 150)
#         # print('150 범위', area_150)
#         # square(area_150[0], area_150[1], area_150[2], area_150[3])


#         # db에서 cctv 가져오기
#         cctvs = data(f"SELECT lat, lng FROM cctv WHERE lat > {area_150[0]} and lat < {area_150[2]} and lng > {area_150[1]} and lng < {area_150[3]}")
#         # print('cctv 중심좌표 목록', cctvs)
#         # (('34.8804', '128.626'), ('34.8814', '128.6243'), ('34.8811', '128.6246'), ('34.8808', '128.6259'), ('34.8814', '128.625'), ('34.8807', '128.6247'))
#         # 문자열이니 숫자로 바꿔야함. np.longdouble()
        
#         area_100 = cal(lat, lng, 100)
#         # total_area = square(area_100[0], area_100[1], area_100[2], area_100[3])
#         # print(total_area)
#         # print('area100', area_100)

#         new_cctvs = []
#         for cctv in cctvs:  # ('34.8804', '128.626')
#             # print(cctv)
#             cctv_area = cal(np.longdouble(cctv[0]), np.longdouble(cctv[1]), 50) # 문자열을 숫자로 변환
#             # print(np.longdouble(cctv[0]), np.longdouble(cctv[1]))
#             # print(cctv_area)
#             if area_100[0] > cctv_area[0]:
#                 cctv_area[0] = area_100[0]
#             if area_100[1] > cctv_area[1]:
#                 cctv_area[1] = area_100[1]
#             if area_100[2] < cctv_area[2]:
#                 cctv_area[2] = area_100[2]
#             if area_100[3] < cctv_area[3]:
#                 cctv_area[3] = area_100[3]
#             new_cctvs.append([int(cctv_area[0]*111194.92664455874), int(cctv_area[1]*np.cos(math.radians((cctv_area[0] + cctv_area[2]) / 2)) * 6371000 * (np.pi / 180)), int(cctv_area[2]*111194.92664455874), int(cctv_area[3]*np.cos(math.radians((cctv_area[0] + cctv_area[2]) / 2)) * 6371000 * (np.pi / 180))])
        
#         # print('새 cctv 좌하우상 좌표 목록', new_cctvs)
#         # [[34.850450339197046, 128.5821821127936, 34.85079058397032, 128.58304793791854]]
        

        
#         # 순회하며 범위 계산
#         if new_cctvs:
#             cctv_area = intersection_area(new_cctvs)
#         else:
#             cctv_area = 0
#         # print(cctv_area)
#         # print(new_cctvs)

#         # print('cctv가 차지하는 영역',cctv_area)
#         # print('전체 영역',total_area)

#         result = cctv_area // 100
#         # print('점수', result)
#         data(f"UPDATE score SET cctv = {result} WHERE type = 'OFFICETEL' AND id = {i[2]}")```