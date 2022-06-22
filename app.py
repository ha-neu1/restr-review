from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.bitceih.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})    
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})






@app.route('/show')
def show():
    return render_template("show.html")
@app.route('/add')
def add():
    return render_template("add.html")
@app.route('/register')
def register():
    return render_template("register.html")

@app.route("/member", methods=["get"])
def members_get():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    area_receive = request.form['area_give']
    email_receive = request.form['email_give']

    doc = {
        'id': id_receive,
        'password': password_receive,
        'area' : area_receive,
        'email': email_receive
    }

    db.member.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/reviews", methods=["get"])
def reviews_get():
    image_receive = request.form['image_give']
    shop_receive = request.form['shop_give']
    address_receive = request.form['address_give']
    comment_receive = request.form['comment_give']

    doc = {
        'image': image_receive,
        'shop': shop_receive,
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
@app.route('/')
def home():
    return render_template('reviewsave.html')


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
