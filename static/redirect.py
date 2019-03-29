from app import app
from flask import send_file

@app.route("/static/redirect.css")
def css():
    return send_file('../static/redirect.css')

@app.route('/static/imgs/jiantou.png')
def jiantou():
    return send_file('../static/jiantou.png')

@app.route('/static/imgs/gongxi.png')
def gongxi():
    return send_file('../static/gongxi.png')

@app.route('/static/imgs/yanzheng.png')
def yanzheng():
    return send_file('../static/yanzheng.png')