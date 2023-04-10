import mysql.connector
from geopy.distance import geodesic

# MySQL 연결 정보
config = {
    'user': 'iujuser',
    'password': '!uj2023',
    'host': 'db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com',
    'database': 'iujdev',
    'raise_on_warnings': True
}

# MySQL 연결
cnx = mysql.connector.connect(**config)

# 커서 생성
cursor = cnx.cursor(prepared=True)

# 아파트 쿼리 실행
ofc_query = "SELECT id, sigungu, lat, lng FROM officetel"
cursor.execute(ofc_query)
office = cursor.fetchall()

# 영화관 쿼리 실행
cinema_query = "SELECT id, name, lat, lng FROM gallery"
cursor.execute(cinema_query)
cinema = cursor.fetchall()

# 연결 종료
# 결과 출력
for a in office:
    home_location = (a[2], a[3])
    home_id = a[0]
    nearest_cinema_id = None
    min_distance = float('inf')
    
    # Find the nearest cinema
    for c in cinema:
        cinema_location = (c[2], c[3])
        cinema_id = c[0]
        distance = geodesic(home_location, cinema_location).km
        if distance < min_distance:
            min_distance = distance
            nearest_cinema_id = cinema_id
    
    # Calculate the score based on the distance to the nearest cinema
    if '서울' in a[1]:
        cutoff_distance = 0.5
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.02))
    elif "부산" in a[1] or '대구' in a[1] or '인천' in a[1] or '광주' in a[1] or '대전' in a[1] or '울산' in a[1] or '경기도' in a[1]:
        cutoff_distance = 0.75
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.035))
    else:
        cutoff_distance = 1
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.05))
    if score > 100:
        score = 100
    print(a[1],min_distance,home_id,score)
        

    score_query = f"UPDATE score SET art_gallery = %s WHERE id = {home_id} AND type='OFFICETEL' "
    
    cursor.execute(score_query, [score])
    cnx.commit()



    # 아파트 쿼리 실행
#     update_query = f"UPDATE score SET cinema = %s WHERE type='APT' AND id = {home_id}"
    

#     cursor.execute(update_query, [score])

#     cnx.commit()

# cursor.close()
# cnx.close()
