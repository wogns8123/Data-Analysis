from geopy.distance import geodesic
import mysql.connector

# MySQL 연결 정보
config = {
  'user': 'your_username',
  'password': 'your_password',
  'host': 'localhost',
  'database': 'your_database_name',
  'raise_on_warnings': True
}

# 특정 경위도
my_location = (37.12345, -122.54321)

# MySQL 연결
cnx = mysql.connector.connect(**config)

# 커서 생성
cursor = cnx.cursor()

# 쿼리 실행
query = "SELECT id, name, lat, lng, addr FROM cinema"
cursor.execute(query)

# 결과 가져오기
result = cursor.fetchall()

# 거리 계산
nearest_cinema = None
min_distance = float('inf')
for cinema in result:
    cinema_location = (cinema[2], cinema[3])
    distance = geodesic(my_location, cinema_location).km
    if distance < min_distance:
        nearest_cinema = cinema
        min_distance = distance

# 연결 종료
cursor.close()
cnx.close()

# 결과 출력
print(nearest_cinema)
