from app import app
from flask import send_file

@app.route("/login/redirect.css")
def css():
    return send_file('templates/loginsuccess/redirect.css')

@app.route('/login/imgs/top.png')
def top():
    return send_file('templates/loginsuccess/imgs/top.png')