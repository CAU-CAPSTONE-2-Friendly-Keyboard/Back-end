from flask import Flask, request, jsonify
import pymysql
from datetime import datetime
from inference import loadModel, get_inference_hate_speech
from badwords_filtering import get_data, bad2star

app = Flask(__name__)

db = pymysql.connect(host='localhost',
                   port=3306,
                   user='root',
                   password='12345',
                   db='friendly_keyboard_accounts',
                   charset='utf8')

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
        
        # SQL query 작성
        # CREATE
        sql = """CREATE TABLE %s_dateTable(
            `index` INT NOT NULL AUTO_INCREMENT,
            `date` VARCHAR(255) NOT NULL,
            `count1` INT NOT NULL,
            `count2` INT NOT NULL,
            `count3` INT NOT NULL,
            `count4` INT NOT NULL,
            `count5` INT NOT NULL,
            `count6` INT NOT NULL,
            `count7` INT NOT NULL,
            `count8` INT NOT NULL,
            `count9` INT NOT NULL,
            PRIMARY KEY(`index`)
            ) CHARSET=utf8;
        """ % (account_id)
        
        cursor.execute(sql)
        db.commit()
        
        sql = """CREATE TABLE %s_chatTable(
            `index` INT NOT NULL AUTO_INCREMENT,
            `id` INT NOT NULL,
            `text` VARCHAR(255) NOT NULL,
            `date` VARCHAR(255) NOT NULL,
            PRIMARY KEY(`index`)
            ) CHARSET=utf8;
        """ % (account_id)
        
        cursor.execute(sql)
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
        global db, cursor
        
        # JSON 형식으로 데이터 받기
        data = request.get_json()
        account_id = data['id']
        text = data['text']
        masking_option = data['masking_option']
        
        # 혐오 표현 존재 여부 확인
        out = get_inference_hate_speech(text)
        result = out['result']
        index = out['index'] # 1 ~ 10
        
        if result != 'clean':
            connectDB()
            
            # SQL query 작성
            # SELECT
            sql = "SELECT hate_speech_count FROM accounts WHERE id = '%s'" % (account_id)
            
            # SQL query 실행
            cursor.execute(sql)
            
            # SQL query 실행 결과를 가져옴
            # hate_speech_count의 값을 1 증가시킴.
            hate_speech_count = cursor.fetchone()[0] + 1
            
            # SQL query 작성
            # UPDATE
            sql = "UPDATE accounts SET hate_speech_count = '%d' WHERE id = '%s'" % (hate_speech_count, account_id);
            
            # SQL query 실행
            cursor.execute(sql)
            
            # 데이터 변화 적용
            # CREATE 또는 DROP, DELETE, UPDATE, INSERT와 같이
            # 데이터베이스 내부의 데이터에 영향을 주는 함수의 경우 commit()이 필요함.
            db.commit()
            
            count = 0
            date = str(datetime.now().date())
            sql = "SELECT * FROM %s_dateTable WHERE date = '%s'" % (account_id, date)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if str(type(row)) == "<class 'NoneType'>":
                sql = """INSERT INTO %s_dateTable (date, count1, count2,
                count3, count4, count5, count6, count7, count8, count9) VALUES
                ('%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d')
                """ % (account_id, date, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                cursor.execute(sql)
                db.commit()
                count = 1
            else:
                count = row[index + 1] + 1
            
            sql = "UPDATE %s_dateTable SET count%d = '%d' WHERE date = '%s'" % (account_id, index, count, date)
            
            cursor.execute(sql)
            db.commit()
            
            if masking_option == True:
                text, used_badwords = bad2star(text)
            
        return jsonify({
            'inference_hate_speech_result': result,
            'text': text
            })

# 특정 계정의 혐오 표현 전체 사용 횟수 가져오기.
@app.route('/get_hate_speech_counts_sum', methods=['POST'])
def get_hate_speech_counts_sum():
    if request.method == 'POST':
        global db, cursor
        
        data = request.get_json()
        account_id = data['id']
        
        connectDB()
        
        sql = "SELECT hate_speech_count FROM accounts WHERE id = '%s'" % (account_id)
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        
        return jsonify({'result': result})

# 특정 계정의 날짜별 혐오 표현 사용 횟수 가져오기.
@app.route('/get_hate_speech_counts', methods=['POST'])
def get_hate_speech_counts():
    if request.method == 'POST':
        global db, cursor
        
        data = request.get_json()
        account_id = data['id']
        
        connectDB()
        
        sql = 'SELECT * FROM %s_dateTable' % (account_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        count1 = {}
        count2 = {}
        count3 = {}
        count4 = {}
        count5 = {}
        count6 = {}
        count7 = {}
        count8 = {}
        count9 = {}
        
        if str(type(result)) != "<class 'NoneType'>":
            for row in result:
                count1[row[1]] = row[2]
                count2[row[1]] = row[3]
                count3[row[1]] = row[4]
                count4[row[1]] = row[5]
                count5[row[1]] = row[6]
                count6[row[1]] = row[7]
                count7[row[1]] = row[8]
                count8[row[1]] = row[9]
                count9[row[1]] = row[10]
            
        return jsonify({
            'count1': count1,
            'count2': count2,
            'count3': count3,
            'count4': count4,
            'count5': count5,
            'count6': count6,
            'count7': count7,
            'count8': count8,
            'count9': count9
            })
    

# 특정 계정의 채팅 내용 저장하기.
@app.route('/save_chat', methods=['POST'])
def save_chat():
    if request.method == 'POST':
        global db, cursor
        
        data = request.get_json()
        account_id = data['account_id']
        id = data['id']
        text = data['text']
        date = data['date']
        
        connectDB()
        
        sql = """INSERT INTO %s_chatTable (id, text, date) VALUES
            ('%d', '%s', '%s') 
            """ % (account_id, id, text, date)
        cursor.execute(sql)
        db.commit()
            
        return "Success"

# 특정 계정의 채팅 내용 가져오기.
@app.route('/get_chat_list', methods=['POST'])
def get_chat_list():
    if request.method == 'POST':
        global db, cursor
        
        data = request.get_json()
        account_id = data['id']
        
        connectDB()
        
        sql = 'SELECT * FROM %s_chatTable' % (account_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        id_list = []
        text_list = []
        date_list = []
        
        if str(type(result)) != "<class 'NoneType'>":
            for row in result:
                id_list.append(row[1])
                text_list.append(row[2])
                date_list.append(row[3])
                
        return jsonify({
            'id_list': id_list,
            'text_list': text_list,
            'date_list': date_list,
            })

if __name__ == '__main__':
    loadModel()
    get_data('KO')
    app.run('0.0.0.0', port = 5000)