import pymysql
from sqlalchemy import create_engine
import pandas as pd

# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

User = "iujuser"
Password = "iuj"
Host = "db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com"
Database = '특화'
# {} 안에 해당하는 정보 넣기. {}는 지우기.
engine = create_engine("mysql+mysqldb://admin:sodam0118@db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com:3306/iujdev")
# print("mysql+mysqldb://iujuser:iuj@db-iuj.cj557j0pfgbg.ap-northeast-2.rds.amazonaws.com:3306/특화")
conn = engine.connect()

df1 = pd.read_csv("3112.csv", encoding='cp949')

df_ = pd.DataFrame(df1[['title','description','school', 'local', 'pubDate', 'link']])
df_.rename(columns={'title':'title', 'description':'description', "school":"school", 'local':'local', 'pubDate':'pubDate', 'link':'link'},inplace=True)

print(df_)

# MySQL에 저장하기
# 변수명은 이전에 만든 데이터프레임 변수명
# name은 생성할 테이블명
# index=False, 인덱스 제외
df_.to_sql(name='news', con=engine, if_exists='append', index=False)
conn.close()