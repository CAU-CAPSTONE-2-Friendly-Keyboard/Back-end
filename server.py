from flask import Flask, session, render_template, redirect, request, url_for, jsonify
import pymysql
from inference import loadModel, get_inference_hate_speech

app = Flask(__name__)

# 데이터베이스에 접근
db = pymysql.connect(host='localhost',
                   port=3306,
                   user='root',
                   password='12345',
                   db='friendly_keyboard_accounts',
                   charset='utf8')

# 데이터베이스를 사용하기 위한 cursor을 세팅.
cursor = db.cursor()

def connectDB():
    global db, cursor
    
    # 데이터베이스에 접근
    db = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='12345',
                       db='friendly_keyboard_accounts',
                       charset='utf8')

    # 데이터베이스를 사용하기 위한 cursor을 세팅.
    cursor = db.cursor()
    
        
@app.route('/', methods=['GET'])
def home():
    return 'Friendly Keyboard Server'

# 특정 아이디가 이미 존재하는지 확인
@app.route('/get_account', methods=['POST'])
def get_account():
    if request.method == 'POST':
        global db, cursor
        
        # JSON 형식으로 데이터 받기
        account_data = request.get_json()
        account_id = account_data['id']
        
        connectDB()
        
        # SQL query 작성
        # SELECT
        sql = "SELECT * FROM accounts WHERE id = '%s'" % (account_id)
        
        # SQL query 실행
        cursor.execute(sql)
        
        # SQL query 실행 결과를 가져옴
        result = cursor.fetchone() 
        
        if str(type(result)) == "<class 'NoneType'>":
            return jsonify({'responseText': "Available"})
        else:
            return jsonify({'responseText': "Unavailable"})

# 회원가입시 데이터베이스에 계정 데이터 추가
@app.route('/sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        global db, cursor
        
        # JSON 형식으로 데이터 받기
        account_data = request.get_json()
        account_id = account_data['id']
        password = account_data['password']
        hate_speech_count = 0
        
        connectDB()
        
        # SQL query 작성
        # INSERT
        sql = "INSERT INTO accounts (id, password, hate_speech_count) VALUES ('%s', '%s', '%d')" % (account_id, password, hate_speech_count)
        
        # SQL query 실행
        cursor.execute(sql)
        
        # 데이터 변화 적용
        # CREATE 또는 DROP, DELETE, UPDATE, INSERT와 같이
        # 데이터베이스 내부의 데이터에 영향을 주는 함수의 경우 commit()이 필요함.
        db.commit()
        
        return jsonify({'responseText': 'Success'})
    
# 로그인 시 아이디와 비밀번호가 올바른지 확인
@app.route('/sign-in', methods=['POST'])
def sign_in():
    if request.method == 'POST':
        global db, cursor
        
        # JSON 형식으로 데이터 받기
        account_data = request.get_json()
        account_id = account_data['id']
        password = account_data['password']
        
        connectDB()
        
        # SQL query 작성
        # SELECT
        sql = "SELECT * FROM accounts WHERE id = '%s' AND password = '%s'" % (account_id, password)
        
        # SQL query 실행
        cursor.execute(sql)
        
        # SQL query 실행 결과를 가져옴
        result = cursor.fetchone() 
        
        if str(type(result)) == "<class 'NoneType'>":
            return jsonify({'responseText': "Unavailable"})
        else:
            return jsonify({'responseText': "Available"})
    
# 입력한 문자열에 혐오 표현 존재 여부 확인
@app.route('/inference_hate_speech', methods=['POST'])
def inference_hate_speech():
    if request.method == 'POST':
        # JSON 형식으로 데이터 받기
        text = request.get_json()['text']
        
        # 혐오 표현 존재 여부 확인
        # result == 'clean' or 'notClean'
        result = get_inference_hate_speech(text)
        
        return jsonify({'inference_hate_speech_result': result})
        
        
if __name__ == '__main__':
    loadModel()
    app.run('0.0.0.0', port = 5000)