from flask import Flask, session, render_template, redirect, request, url_for, jsonify
import pymysql

app = Flask(__name__)
        
@app.route('/', methods=['GET'])
def home():
    return 'Friendly Keyboard Server'

# 특정 아이디가 이미 존재하는지 확인
@app.route('/get_account', methods=['POST'])
def get_account():
    if request.method == 'POST':
        # JSON 형식으로 데이터 받기
        account_id = request.args.get('id')
        
        # 데이터베이스에 접근
        db = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='12345',
                           db='friendly_keyboard_accounts',
                           charset='utf8')

        # 데이터베이스를 사용하기 위한 cursor을 세팅.
        cursor = db.cursor()
        
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
        # JSON 형식으로 데이터 받기
        account_id = request.args.get('key')
        password = request.args.get('password')
        
        # 데이터베이스에 접근
        db = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='12345',
                           db='friendly_keyboard_accounts',
                           charset='utf8')

        # 데이터베이스를 사용하기 위한 cursor을 세팅.
        cursor = db.cursor()
        
        # SQL query 작성
        # INSERT
        sql = "INSERT INTO accounts (id, password) VALUES ('%s', '%s')" % (account_id, password)
        
        # SQL query 실행
        cursor.execute(sql)
        
        # 데이터 변화 적용
        # CREATE 또는 DROP, DELETE, UPDATE, INSERT와 같이
        # 데이터베이스 내부의 데이터에 영향을 주는 함수의 경우 commit()이 필요함.
        db.commit()
        
        return jsonify({'responseText': 'Success'})
        
if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000)