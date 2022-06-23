from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.ehtpe4p.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        return render_template('reviewsave.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/signup')
def signup():
    return render_template('login.html')


@app.route('/sign_in', methods=['POST'])
def signin():
    # 로그인
    return jsonify({'result': 'success'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    email_receive = request.form['email_give']
    area_receive = request.form['area_give']

    doc = {
        "id": id_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "email": email_receive,  # 프로필 이름 기본값은 아이디
        "area": area_receive  # 프로필 사진 파일 이름

    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})



@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/reviewsave')
def reviewsave():
    return render_template('reviewsave.html')    

@app.route('/show')
def show():
    return render_template("show.html")

@app.route("/reviews", methods=["get"])
def reviews_get():
    file_receive = request.form['file_give']
    title_receive = request.form['title_give']
    address_receive = request.form['address_give']
    comment_receive = request.form['comment_give']

    doc = {
        'file': file_receive,
        'title': title_receive,
        'address' : address_receive,
        'comment': comment_receive
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/reviews", methods=["GET"])
def review_get():
    review_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews':review_list})


# 포스팅 추가하기
@app.route('/reviews/save', methods=['POST'])
def save_review():
    title_receive = request.form['title_give']
    address_receive = request.form['address_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'address': address_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}'
    }

    db.reviews.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
