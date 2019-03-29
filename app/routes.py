from app import app
from flask import request,render_template,send_file
from util.login import *
from util.mongoClient import *
import json

from static.redirect import *

@app.route('/')
def test():
    return send_file("../static/redirect.html")

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
    mongoClient().newUser(openid,userInfo)
    return "认证成功！"

@app.route('/login/code')
def getUserInfoByCode():
    '''
    服务器返回openid和用户基本信息
    :return:
    '''
    code=request.args.get('code')
    openid=getOpenid(code)
    userInfo=mongoClient().getUserInfo(openid)
    userInfoTemp={
        'openid':openid,
       'userInfo':userInfo,
    }
    return json.dumps(userInfoTemp)

@app.route("/login/openid")
def getUserInfoByOpenid():
    '''
    通过openid获取用户信息
    :return:
    '''
    openid=request.args.get('openid')
    return json.dumps(mongoClient().getUserInfo(openid))

@app.route('/publicinfo')
def getBannerAndNotice():
    """
    获取首页Banner新闻和notice滚动条的信息
    :return:
    """
    return json.dumps(mongoClient().getPublicInfo())