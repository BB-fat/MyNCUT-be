from app import app
from flask import send_file

@app.route('/publicinfo/img/1.png')
def img1():
    return send_file('../static/publicinfo/1.png')

@app.route('/publicinfo/img/2.png')
def img2():
    return send_file('../static/publicinfo/2.png')

@app.route('/publicinfo/img/3.png')
def img3():
    return send_file('../static/publicinfo/3.png')