from flask import request,render_template
from util.login import *
from util.mongoClient import *
import json

# 登陆成功的网页路由函数
from app.templates.loginsuccess.routes import *

# 首页轮播图图片路由函数
from static.publicinfo.routes import *

@app.route('/login/')
def test():
    return render_template("loginsuccess/redirect.html",name='bbfat')

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
    return render_template("loginsuccess/redirect.html",name=userInfo['name'])

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
    通过openid获取用户基本信息
    :return:
    '''
    openid=request.args.get('openid')
    return json.dumps(mongoClient().getUserInfo(openid)['userInfo'])

@app.route('/publicinfo')
def getBannerAndNotice():
    """
    获取首页Banner新闻和notice滚动条的信息
    :return:
    """
    return json.dumps(mongoClient().getPublicInfo())