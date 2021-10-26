# 1. 설치 requests

import requests
import sqlalchemy as db
import pandas as pd

# 1. requests 모듈로 데이터 다운받기
url = "http://openapi.seoul.go.kr:8088/6d424f64706765743730746d476f47/json/RealtimeCityAir/1/5?END_INDEX=1"
response = requests.get(url)
parseResponse = response.json()

# 2. 데이터 정재하기
row = parseResponse["RealtimeCityAir"]["row"]

weather = []

print(row)
for r in row:
    dict = {}
    dict["MSRDT"] = r["MSRDT"]
    dict["MSRSTE_NM"] = r["MSRSTE_NM"]
    dict["PM10"] = r["PM10"]
    dict["IDEX_NM"] = r["IDEX_NM"]
    weather.append(dict)

#print(weather)

# 3. 판다스로 데이터 변경하기 (csv, db에 데이터 옮기기 편함)
weather_dataFrame = pd.DataFrame(weather)
# print(weather_dataFrame)

# 4. 디비 연결하기
engine = db.create_engine("mariadb+mariadbconnector://python:python1234@127.0.0.1:3306/pythondb")

# 5. 인서트하기
weather_dataFrame.to_sql("weather",engine, index=False,if_exists="replace")

# 6. csv 파일로 만들기
weather_dataFrame.to_csv("weather.csv")

# 7. 불러오기
weather_dataFrame_entity = pd.read_sql("select * from weather", engine)
print(weather_dataFrame_entity)

# 8. Flask 시각화 안해도 됨.