from app import app
from flask import send_file

@app.route("/login/redirect.css")
def css():
    return send_file('../static/redirect.css')

@app.route('/login/jiantou.png')
def jiantou():
    return send_file('../static/jiantou.png')

@app.route('/login/gongxi.png')
def gongxi():
    return send_file('../static/gongxi.png')

@app.route('/login/yanzheng.png')
def yanzheng():
    return send_file('../static/yanzheng.png')