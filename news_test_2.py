# from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import json
# import sys
# import POSUtil

# from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import urllib.request

import json
import pandas as pd
import pymysql
from sqlalchemy import create_engine


client_id = "GqCJlCEVWxwY6cBaaQ0l"
client_secret = "6IR_imM2wA"

def get_news_items(search_word):
    encText = urllib.parse.quote(search_word)
    # url = "https://openapi.naver.com/v1/search/news.json?query=" + encText # JSON 결과

    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText +"&display=100" # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과

    url += "&sort=sim"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        # print(response_body.decode('utf-8'))
        # print(type(json.loads(response_body.decode('utf-8'))))
        items = json.loads(response_body.decode('utf-8'))['items']
        return items


# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
# DB 설정
User = "iujuser"
Password = "iuj"
Host = "db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com"
Database = '특화'
engine = create_engine("mysql+mysqldb://admin:sodam0118@db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com:3306/iujdev")
conn = pymysql.connect(host='db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com',
                        user='iujuser',
                        password='!uj2023',
                        db='iujdev',
                        charset='utf8')
curs = conn.cursor()

corpus = [] 

df = pd.DataFrame(columns=['title', 'description', 'school', 'local', 'pubDate','link'])

school_set = ['어린이집', '유치원', '초등학교', '중학교', '고등학교', '학원']
local_set = ['서울', '부산', '인천', '대구', '대전', '광주', '울산', '세종시', '경기도', '강원도', '충청북도','충북', '충청남도','충남', '전라북도','전북', '전라남도','전남', '경상북도','경북', '경상남도','경남', '제주']

for school_item in school_set:
    # 검색어: 교육 + 정책
    search_word = school_item + ', ' + '정책'
    items = get_news_items(search_word)

    for local_item in local_set:
        # 검색어: 교육 + 지역 + 정책
        search_word = school_item + ', ' + local_item + ', ' + '정책'
        items = get_news_items(search_word)

        for item in items:
            df = df.append({
                'title': item['title'].replace("&lt;","").replace("&gt;","").replace("&apos;","").replace("&quot;","").replace("<b>","").replace("</b>",""), 
                'description': item['description'].replace("&lt;","").replace("&gt;","").replace("&apos;","").replace("&quot;","").replace("<b>","").replace("</b>",""), 
                'school': school_item, 
                'local': local_item,
                'pubDate': item['pubDate'][:16], 
                'link': item['originallink']
            }, ignore_index=True)

df.to_csv("3.csv")
# print(corpus)


'''
['이달 전국서 2만7000여 가구 분양… 전년보다 87%↑', '‘결혼지옥’ 아내보다 누나-처제와 친한 남편 “데이트도 셋이 해” 경악', '네이버 라인망가 선배는 남자아이, 日 
애니메이션 제작 확정', '도봉구, 서울형 키즈카페 10개소 이상 확대 조성', '이달 전국 아파트 2만7399가구 분양…전년比 87% 증가', '더프라미스, 안산 화재 피해가구 
모금운동 시작', '프론테오코리아, 협업툴 부정행위 방지 위한 AI 솔루션 ‘키빗 아이’ 출시', '대전시, 대전형 청년주택 건립사업 국비 40억 원 확보', '장원영·안유진, 아이브 첫 정규에 단독 작사로 참여', '‘문희준♥’ 소율, 산후우울증 고백 “울컥한 게 자주 올라와”']
'''

# 'originallink'


# search_word = '초등학교' + ', ' + '정책'
# items = get_news_items(search_word)

# for i in items:
#     data = i['title'] + ' ' + i['description']
#     print(i)


# # TfidfVectorizer를 이용하여 단어의 빈도수를 계산하고 벡터화
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(corpus)

# # 벡터화된 데이터와 단어 목록 저장
# feature_names = vectorizer.get_feature_names_out()

# # TfidfTransformer를 이용하여 데이터를 TF-IDF 값으로 변환
# transformer = TfidfTransformer()
# X_tfidf = transformer.fit_transform(X)
# print(X_tfidf.shape)


# from sklearn.metrics.pairwise import linear_kernel
# cosine_sim = linear_kernel(X_tfidf, X_tfidf)

# # 인덱스 테이블 만들기
# df = pd.DataFrame([{"title": i["title"], "link": i["originallink"], "description":i["description"]} for i in items])


# indices = pd.Series(df.index, index=df.title).drop_duplicates()
# # print(indices)



# sys.stdout = open('stdout.txt', 'w')


# # 변환된 데이터에서 각 단어의 중요도 출력
# for i in range(len(corpus)):
#     # 현재 문서에서 사용된 단어 목록만 추출
#     words_in_doc = set(vectorizer.build_analyzer()(corpus[i]))
#     doc_indices = [np.where(feature_names == word)[0][0] for word in words_in_doc]

#     print("Document {}:".format(i))
#     for j in doc_indices:
#         print("{}: {}".format(feature_names[j], X_tfidf[i,j]))
#     print("\n")

# sys.stdout.close()


# def movie_REC(title, cosine_sim=cosine_sim):
#     #입력한 영화로 부터 인덱스 가져오기
#     idx = indices[title]

#     # 모든 영화에 대해서 해당 영화와의 유사도를 구하기
#     sim_scores = list(enumerate(cosine_sim[idx]))

#     # 유사도에 따라 영화들을 정렬
#     sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse = True)

#     # 가장 유사한 10개의 영화를 받아옴
#     sim_scores = sim_scores[1:6]

#     # 가장 유사한 10개 영화의 인덱스 받아옴
#     movie_indices = [i[0] for i in sim_scores]
    
#     #기존에 읽어들인 데이터에서 해당 인덱스의 값들을 가져온다. 그리고 스코어 열을 추가하여 코사인 유사도도 확인할 수 있게 한다.
#     result_df = df.iloc[movie_indices].copy()
#     result_df['score'] = [i[1] for i in sim_scores]
    
#     # 읽어들인 데이터에서 줄거리 부분만 제거, 제목과 스코어만 보이게 함
#     # del result_df['content']

#     # 가장 유사한 10개의 영화의 제목을 리턴
#     return result_df


# result = movie_REC("지방도 387호선 남양주 화도~운수구간 올해 상반기 착공")

# print(result)





# # 데이터 저장
# df_data.to_sql(name='news', con=engine, if_exists='append', index=False)

# conn.commit()

# # 자원반납
# conn.close()