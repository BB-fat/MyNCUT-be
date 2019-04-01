from app import app
from flask import send_file

@app.route('/publicinfo/img/1.png')
def img1():
    send_file('1.png')

@app.route('/publicinfo/img/2.png')
def img2():
    send_file('2.png')

@app.route('/publicinfo/img/3.png')
def img3():
    send_file('3.png')