import mysql.connector
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd

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
    query = "SELECT * FROM student_data"  # 테이블명을 적절히 수정해주세요
    data = pd.read_sql(query, connection)
    subjects = [
    '자료구조', '운영체제', 'C언어', '컴퓨터구조',
    '데이터통신', '데이터베이스_및_실습', '웹_어플리케이션_개발', '컴퓨터_그래픽스'
]

    # 코사인 유사도 계산 함수
    def cos_similarity(vec1, vec2):
        return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

    # 학생 데이터를 벡터로 변환하는 함수
    def student_vector(student):
        vector = [
            student['GPA'],
            student['Frontend'],
            student['Backend'],
            student['AI'],
            student['Security'],
            student['Server']
        ]
        for subject in subjects:
            vector.append(student[subject])
        return vector

    # 새로운 학생 데이터를 추가하고 가장 가까운 데이터 추천
    def recommend_closest_students(new_student, n):
        new_student_vector = student_vector(new_student)
        similarities = []

        for _, existing_student in data.iterrows():
            existing_student_vector = student_vector(existing_student)
            similarity = cos_similarity(new_student_vector, existing_student_vector)
            similarities.append(similarity)

        most_similar_indices = np.argsort(similarities)[-n:]
        most_similar_students = data.iloc[most_similar_indices]

        return most_similar_students

    # 랜덤하게 하나의 학생 데이터를 가져오기
    random_index = np.random.choice(data.index)
    random_student = data.loc[random_index]

    # 추천된 가장 가까운 학생 데이터 출력 (가장 가까운 3명)
    n = 3
    recommended_students = recommend_closest_students(random_student, n)
    print(f"Recommended {n} Closest Students:")
    print(recommended_students)

    # 접속 해제
    connection.close()
    print("MySQL 접속이 닫혔습니다.")

else:
    print("MySQL 접속 실패")
