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

# 빌라 쿼리 실행
officetel_query = "SELECT id, sigungu, lat, lng FROM officetel"
cursor.execute(officetel_query)
officetel = cursor.fetchall()

# 도서관 쿼리 실행
book_query = "SELECT id, name, lat, lng FROM special"
cursor.execute(book_query)
book = cursor.fetchall()

# 연결 종료
# 결과 출력
for a in officetel:
    home_location = (a[2], a[3])
    home_id = a[0]
    nearest_library_id = None
    min_distance = float('inf')
    
    # Find the nearest cinema
    for c in book:
        library_location = (c[2], c[3])
        library_id = c[0]
        distance = geodesic(home_location, library_location).km
        if distance < min_distance:
            min_distance = distance
            nearest_library_id = library_id
    
    # Calculate the score based on the distance to the nearest cinema
    if '서울' in a[1]:
        cutoff_distance = 0.5
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.02))
    elif "부산" in a[1] or '대구' in a[1] or '인천' in a[1] or '광주' in a[1] or '대전' in a[1] or '울산' in a[1] or '경기도' in a[1]:
        cutoff_distance = 0.75
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.03))
    else:
        cutoff_distance = 1
        max_score = 100
        score = max(0, round(max_score - (min_distance - cutoff_distance) / 0.05))
    if score > 100:
        score = 100
    print(a[1],min_distance,home_id,score)
        

    score_query = f"UPDATE score SET special_school = %s WHERE id = {home_id} AND type='officetel'"
    
    cursor.execute(score_query, [score])
    cnx.commit()



    # 아파트 쿼리 실행
#     update_query = f"UPDATE score SET cinema = %s WHERE type='APT' AND id = {home_id}"
    

#     cursor.execute(update_query, [score])

#     cnx.commit()

# cursor.close()
# cnx.close()
