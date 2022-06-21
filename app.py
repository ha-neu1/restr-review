from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.bitceih.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
