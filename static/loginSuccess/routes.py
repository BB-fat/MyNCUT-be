from app import app
from flask import send_file

@app.route("/login/redirect.css")
def css():
    return send_file('../static/loginSuccess/redirect.css')

@app.route('/login/jiantou.png')
def jiantou():
    return send_file('../static/loginSuccess/jiantou.png')

@app.route('/login/gongxi.png')
def gongxi():
    return send_file('../static/loginSuccess/gongxi.png')

@app.route('/login/yanzheng.png')
def yanzheng():
    return send_file('../static/loginSuccess/yanzheng.png')