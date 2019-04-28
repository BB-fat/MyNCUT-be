from app import app
from flask import send_file

@app.route('/download/imgs/failure.png')
def img():
    send_file('../static/failure/imgs/failure.png')