import mysql.connector
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import random

# MySQL 접속 정보 설정
db_config = {
    'host': 'dongha.xyz',
    'user': 'gachon',
    'password': 'gachon',
    'database': 'gachon'
}

# MySQL 서버에 접속
connection = mysql.connector.connect(**db_config)

if connection.is_connected():
    print("MySQL에 성공적으로 접속되었습니다.")

    # 데이터베이스에서 데이터 불러오기
    query = "SELECT * FROM gachon.food"  # 테이블명을 적절히 수정해주세요
    data = pd.read_sql(query, connection)

    # 코사인 유사도 계산 함수
    def cos_similarity(vec1, vec2):
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    # 음식 데이터를 벡터로 변환하는 함수
    places_map = {
        '반도체 대학': 1, '글로벌센터': 1,
        '가천관': 2,
        '바이오나노연구원': 3, '한의과대학': 3,
        '전자정보도서관': 4, '스타덤광장': 4,
        '산학협력관': 5, '공과대학2': 5,
        '예술체육대학': 6, '교육대학원': 6,
        'AI공학관': 7, '제3기숙사': 7,
        '제2기숙사': 8, '제1기숙사': 8,
        '학생회관': 9, '학군단': 9,
        '공과대학1': 10, '바이오나노대학': 10
    }

    menus = [
        ['치킨'], ['피자'], ['족발&보쌈'], ['찜&탕&찌개'], ['돈까스&회&일식'],
        ['고기&구이'], ['야식'], ['양식'], ['중식'], ['아시안'],
        ['백반&죽&국수'], ['도시락'], ['분식'], ['카페&디저트'], ['패스트푸드']
    ]

    def food_vector(food):
        place_vector = [0] * 10
        menu_vector = [0] * 15

        place = food['장소']
        menu = food['메뉴']

        place_code = places_map.get(place, 0)
        if place_code > 0:
            place_vector[place_code - 1] = 1

        menu_index = menus.index([menu])
        menu_vector[menu_index] = 1

        return place_vector + menu_vector

    # 새로운 음식 데이터를 추가하고 가장 유사한 음식 추천
    def recommend_similar_food(new_food, n):
        new_food_vector = food_vector(new_food)
        similarities = []

        for _, existing_food in data.iterrows():
            existing_food_vector = food_vector(existing_food)
            similarity = cos_similarity(new_food_vector, existing_food_vector)
            similarities.append(similarity)

        most_similar_indices = np.argsort(similarities)[-n:]
        most_similar_food = data.iloc[most_similar_indices]

        return most_similar_food

    # 랜덤하게 하나의 음식 데이터를 가져오기
    random_index = np.random.choice(data.index)
    random_food = data.loc[random_index]

    # 추천된 가장 유사한 음식 데이터 출력 (가장 유사한 3개)
    n = 3
    recommended_food = recommend_similar_food(random_food, n)
    print(f"Recommended {n} Similar Foods:")
    print(recommended_food)

    connection.close()
    print("MySQL 접속이 닫혔습니다.")

else:
    print("MySQL 접속 실패")
