from app import app
from flask import request
from util.login import *
import json

@app.route('/')
def index():
    return "Hello world!"

@app.route('/login')
def login():
    AT=getAccess_token()
    openid=request.args.get('state')
    code=request.args.get('code')
    userInfo=getUserInfo(code,AT)
    return  json.dumps(userInfo)



