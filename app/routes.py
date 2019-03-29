from app import app
from flask import request
from util.login import *
from util.mongoClient import *
import setting

import json

@app.route('/')
def index():
    return "Hello world！"

@app.route('/login/oauth')
def oauth():
    '''
    身份认证函数
    :return:
    '''
    access_token=getAccess_token()
    openid=request.args.get('state')
    code=request.args.get('code')
    userInfo=getUserInfo(code,access_token)
    #newUser(openid,userInfo)
    return json.dumps(userInfo)

@app.route('/login/openid')
def aquireOpenid():
    '''
    服务器返回openid和用户基本信息
    :return:
    '''
    code=request.args.get('code')
    openid=getOpenid(code)
    #userInfo=getUserInfo()
    userInfoTemp={
        'openid':openid,
#        'userInfo':userInfo,
    }
    return json.dumps(userInfoTemp)

@app.route('/publicinfo')
def bannerAndNotice():
    """
    获取首页Banner新闻和notice滚动条的信息
    :return:
    """
    return json.dumps(mongoClient.getPublicInfo())







