from flask import Flask # Flask
from flask import request, session
import json
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import hashlib

cred = credentials.Certificate('./key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://messenger-3a47c-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})
app.secret_key = 'asdf'

@app.route('/signup',methods=['POST'])
def signup():

    params = request.get_json()
    Inputemail = hashlib.sha256(params['Inputemail'].encode()).hexdigest()
    if params['Pass1'] != params['Pass2']:
        return '비밀번호가 같지 않습니다', 400
    dir = db.reference(f'/users/{Inputemail}')
    if dir.get() != None:
        return '이메일이 이미 사용중입니다', 400
    if params['Name'].isalpha() == False:
        return '이름에 공백, 특수문자, 숫자가 포함되어있습니다', 400
    Pass = hashlib.sha256(params['Pass1'].encode()).hexdigest()
    dir.update({'Name' : params['Name'],'Pass':Pass})


    return '회원가입을 완료하였습니다', 200
           
@app.route('/login',methods=['POST'])
def login():
    params = request.get_json()
    Email = hashlib.sha256(params['Email'].encode()).hexdigest()
    Pass = hashlib.sha256(params['Pass'].encode()).hexdigest()
    dir = db.reference(f'/users/{Email}')
    finduser = dir.get()
    if finduser == None:
        return '계정을 찾지 못했습니다', 400
    if finduser['Pass'] != Pass:
        return '비밀번호가 올바르지 않습니다', 400
    
    return '로그인에 성공하였습니다', 200

@app.route('/is_session',methods=['GET'])
def is_session():
    if 'id' in session:
        return 'True'
    return 'False'
    

if __name__ == "__main__":
    app.run(debug=True)
    