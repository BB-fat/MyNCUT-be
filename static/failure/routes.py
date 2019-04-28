from app import app
from flask import send_file

@app.route('/imgs/failure.png')
def img():
    return send_file('../static/failure/imgs/failure.png')